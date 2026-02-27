import PyPDF2

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":
    pdf_path = "Final_Project_With_Depression_Levels (1).pdf"
    text = extract_text_from_pdf(pdf_path)
    
    with open("thesis_content.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Extracted {len(text)} characters from the PDF")
    print("\nFirst 2000 characters:\n")
    print(text[:2000])
