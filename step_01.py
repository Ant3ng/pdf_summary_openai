import sys
import PyPDF2

# Step 1: Convert the PDF file into a text file using a Python script
def convert_pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        return text


if __name__ == "__main__":
    print(sys.argv[1])
    text = convert_pdf_to_text(sys.argv[1])
    print(text)
