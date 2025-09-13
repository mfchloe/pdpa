import PyPDF2
import os
import json
import chromadb
from openai import OpenAI
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import asyncio
from typing import Optional

# Configuration
OPENAI_API_KEY = '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'

# Initialize clients
openai_client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# FastAPI setup
app = FastAPI(title="PDPA Search API", version="1.0.0")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =====================================================
# PDF EXTRACTION FUNCTIONS
# =====================================================

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF and return as dictionary with page numbers as keys"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text_by_page = {}
            for page_num, page in enumerate(reader.pages):
                text_by_page[page_num + 1] = page.extract_text()
            return text_by_page
    except FileNotFoundError:
        logger.error(f"PDF file not found at {pdf_path}")
        return {}
    except Exception as e:
        logger.error(f"Error reading PDF {pdf_path}: {str(e)}")
        return {}

def extract_all_pdfs():
    """Extract text from all PDF files"""
    pdf_folder = os.path.join(os.path.dirname(__file__), 'pdpa_documents')
    
    # If the folder doesn't exist in current directory, try parent directory
    if not os.path.exists(pdf_folder):
        pdf_folder = os.path.join(os.path.dirname(__file__), '..', 'pdpa_documents')
    
    pdfs = {
        'statute': os.path.join(pdf_folder, 'statute.pdf'),
        'schedules': os.path.join(pdf_folder, 'schedules.pdf'), 
        'regulations': os.path.join(pdf_folder, 'regulations.pdf')
    }
    
    all_extracted_text = {}
    
    for doc_type, pdf_path in pdfs.items():
        logger.info(f"Extracting text from {doc_type}...")
        text_by_page = extract_text_from_pdf(pdf_path)
        if text_by_page:
            all_extracted_text[doc_type] = text_by_page
            logger.info(f"Extracted {len(text_by_page)} pages from {doc_type}")
        else:
            logger.warning(f"No text extracted from {doc_type}")
    
    return all_extracted_text

# =====================================================
# TEXT CHUNKING FUNCTIONS  
# =====================================================

def simple_chunk_text(text, chunk_size=500):
    """Simple text chunking by sentences and word count"""
    if not text or not text.strip():
        return []
    
    # Split by sentences (basic approach)
    sentences = text.replace('.\n', '. ').split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Check if adding this sentence would exceed chunk size
        if len(current_chunk.split()) + len(sentence.split()) <= chunk_size:
            current_chunk += sentence + ". "
        else:
            # Save current chunk if it has content
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            # Start new chunk with current sentence
            current_chunk = sentence + ". "
    
    # Don't forget the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return [chunk for chunk in chunks if len(chunk.strip()) > 20]  # Filter very short chunks

def create_chunks_from_extracted_text(extracted_texts):
    """Create chunks from extracted text with metadata"""
    source_mapping = {
        'statute': "PDPA (Main Act)",
        'schedules': "Personal Data Protection (Breach Notification) Regulations", 
        'regulations': "Regulations"
    }
    
    all_chunks = []
    
    for doc_type, text_by_page in extracted_texts.items():
        source = source_mapping.get(doc_type, doc_type)
        logger.info(f"Chunking {doc_type} ({len(text_by_page)} pages)...")
        
        for page_num, text in text_by_page.items():
            if not text or not text.strip():
                continue
                
            chunks = simple_chunk_text(text)
            
            for i, chunk in enumerate(chunks):
                chunk_data = {
                    'text': chunk,
                    'metadata': {
                        'section': f"Page {page_num}, Section {i+1}",
                        'source': source,
                        'page': page_num,
                        'chunk_id': f"{doc_type}_{page_num}_{i+1}"
                    }
                }
                all_chunks.append(chunk_data)
        
        logger.info(f"Created chunks for {doc_type}")
    
    logger.info(f"Total chunks created: {len(all_chunks)}")
    return all_chunks

# =====================================================
# EMBEDDING FUNCTIONS
# =====================================================

def embed_text(text):
    """Generate embeddings using OpenAI"""
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {str(e)}")
        return None

def create_embeddings_and_store(chunks):
    """Create embeddings and store in ChromaDB"""
    try:
        # Create or get collection
        try:
            # Try to delete existing collection to start fresh
            try:
                chroma_client.delete_collection("PDPA")
                logger.info("Deleted existing PDPA collection")
            except:
                pass
            
            collection = chroma_client.create_collection("PDPA")
            logger.info("Created new PDPA collection")
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            return False
        
        logger.info(f"Processing {len(chunks)} chunks...")
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        embeddings = []
        
        for i, chunk_data in enumerate(chunks):
            text = chunk_data['text']
            metadata = chunk_data['metadata']
            
            # Generate embedding
            embedding = embed_text(text)
            if embedding is None:
                logger.warning(f"Failed to create embedding for chunk {i}")
                continue
                
            documents.append(text)
            metadatas.append(metadata)
            ids.append(str(uuid.uuid4()))
            embeddings.append(embedding)
            
            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1}/{len(chunks)} chunks")
        
        if not documents:
            logger.error("No valid embeddings created")
            return False
        
        # Add to collection in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            try:
                batch_docs = documents[i:i+batch_size]
                batch_metadata = metadatas[i:i+batch_size]
                batch_ids = ids[i:i+batch_size]
                batch_embeddings = embeddings[i:i+batch_size]
                
                collection.add(
                    documents=batch_docs,
                    metadatas=batch_metadata,
                    ids=batch_ids,
                    embeddings=batch_embeddings
                )
                logger.info(f"Added batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
            except Exception as e:
                logger.error(f"Error adding batch {i//batch_size + 1}: {str(e)}")
        
        # Verify collection
        count = collection.count()
        logger.info(f"Successfully stored {count} documents in ChromaDB")
        return count > 0
        
    except Exception as e:
        logger.error(f"Error during embedding process: {str(e)}")
        return False

# =====================================================
# SEARCH FUNCTIONS
# =====================================================

def embed_query(query):
    """Generate embedding for search query"""
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=query
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating query embedding: {str(e)}")
        return None

def search_documents(query, top_k=5):
    """Search for relevant documents"""
    try:
        # Get collection
        collection = chroma_client.get_collection("PDPA")
        
        # Generate query embedding
        query_embedding = embed_query(query)
        if query_embedding is None:
            return {"results": [], "error": "Failed to generate query embedding"}
        
        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results to match expected output
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "section": results['metadatas'][0][i]['section'],
                    "text": results['documents'][0][i],
                    "source": results['metadatas'][0][i]['source'],
                    "page": results['metadatas'][0][i]['page']
                })
        
        return {"results": formatted_results}
    
    except Exception as e:
        logger.error(f"Error during search: {str(e)}")
        return {"results": [], "error": str(e)}

# =====================================================
# INITIALIZATION FUNCTION
# =====================================================

def initialize_system():
    """Initialize the entire system - extract, chunk, embed"""
    logger.info("Starting system initialization...")
    
    # Step 1: Extract text from PDFs
    logger.info("Step 1: Extracting text from PDFs...")
    extracted_texts = extract_all_pdfs()
    if not extracted_texts:
        logger.error("No text extracted from PDFs. Please check your PDF files.")
        return False
    
    # Step 2: Create chunks
    logger.info("Step 2: Creating text chunks...")
    chunks = create_chunks_from_extracted_text(extracted_texts)
    if not chunks:
        logger.error("No chunks created from extracted text.")
        return False
    
    # Step 3: Create embeddings and store
    logger.info("Step 3: Creating embeddings and storing in database...")
    success = create_embeddings_and_store(chunks)
    if not success:
        logger.error("Failed to create embeddings and store in database.")
        return False
    
    logger.info("System initialization completed successfully!")
    return True

# =====================================================
# API ENDPOINTS
# =====================================================

class SearchQuery(BaseModel):
    scenario_text: str
    top_k: Optional[int] = 5

@app.on_event("startup")
async def startup_event():
    """Initialize the system when the API starts"""
    # Check if collection exists
    try:
        collection = chroma_client.get_collection("PDPA")
        count = collection.count()
        if count > 0:
            logger.info(f"Found existing PDPA collection with {count} documents")
            return
    except:
        pass
    
    # If no collection or empty collection, initialize
    logger.info("No existing collection found. Initializing system...")
    success = initialize_system()
    if not success:
        logger.error("Failed to initialize system!")

@app.post("/search_statute")
async def search_statute(query: SearchQuery):
    """Search the PDPA statute based on scenario description"""
    try:
        logger.info(f"Received query: {query.scenario_text[:100]}...")
        
        # Check if collection exists
        try:
            collection = chroma_client.get_collection("PDPA")
            if collection.count() == 0:
                raise HTTPException(status_code=503, detail="System not initialized. Please wait and try again.")
        except:
            raise HTTPException(status_code=503, detail="Database not ready. Please wait for initialization to complete.")
        
        # Search documents
        results = search_documents(query.scenario_text, top_k=query.top_k)
        
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        
        return results
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def status():
    """Check API and database status"""
    try:
        collection = chroma_client.get_collection("PDPA")
        count = collection.count()
        return {
            "status": "API is running!",
            "collection_exists": True,
            "document_count": count,
            "ready": count > 0
        }
    except:
        return {
            "status": "API is running!",
            "collection_exists": False,
            "document_count": 0,
            "ready": False
        }

@app.post("/initialize")
async def initialize_endpoint():
    """Manually trigger system initialization"""
    try:
        logger.info("Manual initialization triggered")
        success = initialize_system()
        if success:
            return {"message": "System initialized successfully"}
        else:
            raise HTTPException(status_code=500, detail="Initialization failed")
    except Exception as e:
        logger.error(f"Initialization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PDPA Search API", 
        "docs": "/docs",
        "endpoints": {
            "search": "/search_statute",
            "status": "/status",
            "initialize": "/initialize"
        }
    }

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)