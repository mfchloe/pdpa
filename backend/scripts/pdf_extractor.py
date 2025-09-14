import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF and return as dictionary with section numbers as keys"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text_by_section = {}
            section = None
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                lines = text.split('\n')
                for line in lines:
                    # Detect section headings in the format S1, S2, S3...
                    if line.strip().startswith('S'):
                        section = line.strip()  # Assign current section heading
                    if section:
                        if section not in text_by_section:
                            text_by_section[section] = ""
                        text_by_section[section] += line.strip() + " "
            return text_by_section
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
        output_file = f"{doc_type}_text_by_section.txt"
        with open(output_file, "w", encoding='utf-8') as f:
            for section, text in extracted_texts[doc_type].items():
                f.write(f"Section {section}:\n{text}\n\n")
        print(f"Saved {len(extracted_texts[doc_type])} sections to {output_file}")
    
    return extracted_texts

if __name__ == "__main__":
    save_text_from_pdfs()
