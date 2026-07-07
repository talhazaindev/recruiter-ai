from parser.parser import parse_cv

import subprocess
import os


def docx_to_pdf(docx_path):

    output_dir = os.path.dirname(os.path.abspath(docx_path))
    soffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"

    subprocess.run([
        soffice_path,
        "--headless",
        "--convert-to", "pdf",
        docx_path,
        "--outdir", output_dir
    ], check=True)

    pdf_name = os.path.splitext(os.path.basename(docx_path))[0] + ".pdf"
    return os.path.join(output_dir, pdf_name)

def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return "pdf"
    elif ext == ".docx":
        return "docx"
    elif ext == ".doc":
        return "doc"
    else:
        return None

file_path = "cvs_test/cv3_v5.pdf"  # Replace with the actual path to your CV file
file_type = get_file_type(file_path)

if file_type == "docx":
    pdf_path = docx_to_pdf(file_path)
    cv_text=parse_cv(pdf_path)
else:
    cv_text = parse_cv(file_path)

""" for i in range(1, 22):
    file_path = f"cvs/cvs/cv{i}.pdf"
    
    # Check if file exists before processing
    if os.path.exists(file_path):
        file_type = get_file_type(file_path)
        
        if file_type == "docx":
            pdf_path = docx_to_pdf(file_path)
            cv_text = parse_cv(pdf_path)
        else:
            cv_text = parse_cv(file_path)
        
        print(f"Processed cv{i}.pdf")
    else:
        print(f"File not found: {file_path}")
 """