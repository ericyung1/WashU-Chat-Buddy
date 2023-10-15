import PyPDF2
import os

def extract_text_from_pdf(pdf_file: str) -> str:
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfReader(pdf)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)

        return ''.join(pdf_text)

def convert_pdfs_to_txt(pdf_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, pdf_file)
            txt_file = os.path.splitext(pdf_file)[0] + '.txt'
            txt_path = os.path.join(output_dir, txt_file)

            pdf_text = extract_text_from_pdf(pdf_path)

            with open(txt_path, 'w', encoding='utf-8') as txt:
                txt.write(pdf_text)

if __name__ == '__main__':
    pdf_dir = '/Users/danielahmadi/Desktop/Chatgptproject/course evals pdf'  # Replace with the path to your PDF directory
    output_dir = '/Users/danielahmadi/Desktop/Chatgptproject/course evals txt'  # Replace with the path to your output directory
    convert_pdfs_to_txt(pdf_dir, output_dir)