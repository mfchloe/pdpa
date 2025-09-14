import chromadb
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI API and ChromaDB client
openai.api_key = os.getenv("API_KEY")
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def embed_query(query):
    """Generate embedding for search query"""
    try:
        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=query
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating query embedding: {str(e)}")
        return None

def search_documents(query, top_k=5):
    """Search for relevant documents"""
    try:
        # Get collection
        collection = chroma_client.get_collection("PDPA")
        
        # Generate query embedding
        query_embedding = embed_query(query)
        if query_embedding is None:
            return {"results": []}
        
        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "section": results['metadatas'][0][i]['section'],
                    "text": results['documents'][0][i],
                    "source": results['metadatas'][0][i]['source'],
                    "similarity_score": 1 - results['distances'][0][i] if results['distances'] else None
                })
        
        return {"results": formatted_results}
    
    except Exception as e:
        print(f"Error during search: {str(e)}")
        return {"results": [], "error": str(e)}

if __name__ == "__main__":
    query = "What are the breach notification requirements?"
    results = search_documents(query)
    
    print("Search Results:")
    for res in results['results']:
        print(f"Section: {res['section']}")
        print(f"Source: {res['source']}")
        print(f"Text: {res['text'][:200]}...")
        print(f"Similarity: {res['similarity_score']:.3f}" if res['similarity_score'] else "")
        print("-" * 50)
