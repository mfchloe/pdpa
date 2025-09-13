# pdf_extractor.py
import PyPDF2
import os

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
        print(f"Error: PDF file not found at {pdf_path}")
        return {}
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {str(e)}")
        return {}

def save_text_from_pdfs():
    """Extract and save text from PDFs"""
    pdf_folder = os.path.join(os.path.dirname(__file__), '..', 'pdpa_documents')
    
    pdfs = {
        'statute': os.path.join(pdf_folder, 'statute.pdf'),
        'schedules': os.path.join(pdf_folder, 'schedules.pdf'),
        'regulations': os.path.join(pdf_folder, 'regulations.pdf')
    }
    
    extracted_texts = {}
    
    for doc_type, pdf_path in pdfs.items():
        print(f"Processing {doc_type}...")
        extracted_texts[doc_type] = extract_text_from_pdf(pdf_path)
        
        # Save to file with proper format
        output_file = f"{doc_type}_text_by_page.txt"
        with open(output_file, "w", encoding='utf-8') as f:
            for page_num, text in extracted_texts[doc_type].items():
                f.write(f"Page {page_num}:\n{text}\n\n")
        print(f"Saved {len(extracted_texts[doc_type])} pages to {output_file}")
    
    return extracted_texts

if __name__ == "__main__":
    save_text_from_pdfs()