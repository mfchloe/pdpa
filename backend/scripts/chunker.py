# chunker.py
import openai
import os
import json
from openai import OpenAI

# Initialize OpenAI client (updated API)
openai.api_key = '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'

def load_text_by_page(filename):
    """Load text file and parse it back into page dictionary"""
    text_by_page = {}
    try:
        with open(filename, "r", encoding='utf-8') as f:
            content = f.read()
        
        # Parse the saved format back into dictionary
        pages = content.split("Page ")[1:]  # Skip empty first element
        for page_content in pages:
            lines = page_content.split('\n', 1)
            page_num = int(lines[0].replace(':', ''))
            text = lines[1] if len(lines) > 1 else ""
            text_by_page[page_num] = text.strip()
        
        return text_by_page
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return {}

def simple_chunk_text(text, chunk_size=500):
    """Simple text chunking by sentences and word count"""
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) <= chunk_size:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return [chunk for chunk in chunks if chunk.strip()]

def chunk_documents():
    """Chunk all documents and save with metadata"""
    documents = {
        'statute': {
            'file': "statute_text_by_page.txt",
            'source': "PDPA (Main Act)",
            'output': "statute_chunks_with_metadata.json"
        },
        'schedules': {
            'file': "schedules_text_by_page.txt", 
            'source': "Personal Data Protection (Breach Notification) Regulations",
            'output': "schedules_chunks_with_metadata.json"
        },
        'regulations': {
            'file': "regulations_text_by_page.txt",
            'source': "Regulations", 
            'output': "regulations_chunks_with_metadata.json"
        }
    }
    
    all_chunks = []
    
    for doc_type, doc_info in documents.items():
        print(f"Chunking {doc_type}...")
        text_by_page = load_text_by_page(doc_info['file'])
        
        doc_chunks = []
        for page_num, text in text_by_page.items():
            if text.strip():  # Only process non-empty pages
                chunks = simple_chunk_text(text)
                for i, chunk in enumerate(chunks):
                    chunk_data = {
                        'text': chunk,
                        'metadata': {
                            'section': f"Page {page_num}, Chunk {i+1}",
                            'source': doc_info['source'],
                            'page': page_num,
                            'chunk_id': f"{doc_type}_{page_num}_{i+1}"
                        }
                    }
                    doc_chunks.append(chunk_data)
                    all_chunks.append(chunk_data)
        
        # Save individual document chunks
        with open(doc_info['output'], 'w', encoding='utf-8') as f:
            json.dump(doc_chunks, f, indent=2, ensure_ascii=False)
        
        print(f"Created {len(doc_chunks)} chunks for {doc_type}")
    
    # Save all chunks together
    with open('all_chunks_with_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    
    print(f"Total chunks created: {len(all_chunks)}")
    return all_chunks

if __name__ == "__main__":
    chunk_documents()