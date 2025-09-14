import openai
import os
import json
from openai import OpenAI

# Initialize OpenAI client (updated API)
openai.api_key = os.getenv("API_KEY")

def load_text_by_section(filename):
    """Load text file and parse it back into section dictionary"""
    text_by_section = {}
    try:
        with open(filename, "r", encoding='utf-8') as f:
            content = f.read()
        
        # Parse the saved format back into dictionary
        sections = content.split("Section ")[1:]  # Skip empty first element
        for section_content in sections:
            lines = section_content.split('\n', 1)
            section = lines[0].replace(':', '').strip()
            text = lines[1] if len(lines) > 1 else ""
            text_by_section[section] = text.strip()
        
        return text_by_section
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
            'file': "statute_text_by_section.txt",
            'source': "PDPA (Main Act)",
            'output': "statute_chunks_with_metadata.json"
        },
        'schedules': {
            'file': "schedules_text_by_section.txt", 
            'source': "Personal Data Protection (Breach Notification) Regulations",
            'output': "schedules_chunks_with_metadata.json"
        },
        'regulations': {
            'file': "regulations_text_by_section.txt",
            'source': "Regulations", 
            'output': "regulations_chunks_with_metadata.json"
        }
    }
    
    all_chunks = []
    
    for doc_type, doc_info in documents.items():
        print(f"Chunking {doc_type}...")
        text_by_section = load_text_by_section(doc_info['file'])
        
        doc_chunks = []
        for section, text in text_by_section.items():
            if text.strip():  # Only process non-empty sections
                chunks = simple_chunk_text(text)
                for i, chunk in enumerate(chunks):
                    chunk_data = {
                        'text': chunk,
                        'metadata': {
                            'section': section,
                            'source': doc_info['source'],
                            'chunk_id': f"{doc_type}_{section}_{i+1}"
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
