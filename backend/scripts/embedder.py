# embedder.py
import json
import chromadb
from openai import OpenAI
import uuid

# Initialize clients
openai.api_key = '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'
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def embed_text(text):
    """Generate embeddings using OpenAI"""
    try:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        return None

def embed_documents():
    """Load chunks and create embeddings in ChromaDB"""
    try:
        # Load all chunks
        with open('all_chunks_with_metadata.json', 'r', encoding='utf-8') as f:
            all_chunks = json.load(f)
        
        print(f"Loading {len(all_chunks)} chunks...")
        
        # Create or get collection
        try:
            collection = chroma_client.get_collection("PDPA")
            print("Found existing PDPA collection")
        except:
            collection = chroma_client.create_collection("PDPA")
            print("Created new PDPA collection")
        
        # Prepare data for ChromaDB
        documents = []
        metadatas = []
        ids = []
        embeddings = []
        
        for i, chunk_data in enumerate(all_chunks):
            text = chunk_data['text']
            metadata = chunk_data['metadata']
            
            # Generate embedding
            embedding = embed_text(text)
            if embedding is None:
                continue
                
            documents.append(text)
            metadatas.append(metadata)
            ids.append(str(uuid.uuid4()))
            embeddings.append(embedding)
            
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(all_chunks)} chunks")
        
        # Add to collection in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
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
            print(f"Added batch {i//batch_size + 1}")
        
        print(f"Successfully embedded {len(documents)} documents")
        
        # Verify collection
        count = collection.count()
        print(f"Collection now contains {count} documents")
        
    except FileNotFoundError:
        print("Error: all_chunks_with_metadata.json not found. Run chunker.py first.")
    except Exception as e:
        print(f"Error during embedding: {str(e)}")

if __name__ == "__main__":
    embed_documents()