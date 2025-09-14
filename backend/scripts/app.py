from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .search import search_documents

# Initialize FastAPI app
app = FastAPI()

# Define the input request model
class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search(request: SearchRequest):
    query = request.query
    
    if not query:
        raise HTTPException(status_code=400, detail="No query provided")
    
    # Call search_documents function
    results = search_documents(query)
    
    if "error" in results:
        raise HTTPException(status_code=500, detail=results["error"])
    
    return results

# If running with Uvicorn (for production)
# uvicorn app:app --reload
