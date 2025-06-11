import pdfplumber
import PyPDF2
import docx
import os

def extract_text(file_path):
    """
    Extract text from a .pdf or .docx file.
    Returns: Extracted text as a string, or empty string on failure.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return ""
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == ".pdf":
            try:
                with pdfplumber.open(file_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
                    if text:
                        return text
                    print("Warning: No text extracted with pdfplumber. Trying PyPDF2...")
            except Exception as e:
                print(f"pdfplumber failed: {e}. Falling back to PyPDF2...")
            
            try:
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
                    if not text:
                        print("Error: No text extracted. Ensure the PDF is text-based.")
                    return text
            except Exception as e:
                print(f"PyPDF2 failed: {e}")
                return ""
        
        elif file_ext == ".docx":
            doc = docx.Document(file_path)
            text = ""
            for para in doc.paragraphs:
                if para.text.strip():
                    text += para.text + "\n"
            return text
        else:
            print(f"Error: Unsupported file type {file_ext}. Use .pdf or .docx")
            return ""
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""