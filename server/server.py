from fastapi import FastAPI
from fastapi import UploadFile, File, HTTPException
import os
from parser.parser import column_boxes, parse_cv,form_json

from parser.final_json_quality import calculate_quality_score
from parser.file_validator import validate_upload
import shutil
import uuid
import fitz
from docling.document_converter import DocumentConverter


from parser.docling_parser import cv_parse_docling
from parser.llm import process_resume


app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return{
        "message": "Boolmind cv parser"
        }


def parsing(filepath,converter):
    doc =fitz.open(filepath)

    multi_column=True
    parser=""
    for page_num, page in enumerate(doc,start=1):
        columns = column_boxes(page,footer_margin=5,header_margin=50)
        if len(columns)<=1:
            multi_column=False
            
            break

    if multi_column==True:
        result=cv_parse_docling(filepath,converter)
        parser="docling"
        print("docling1 bcz multi column")
    else:
        result=parse_cv(filepath)
        parser="custom"
        print("custom1")

    return result,parser
    

def should_run_custom_parser(resume: dict) -> bool:
    """
    Returns True if the custom parser should be executed.

    Conditions:
    - A required section is missing.
    - A required section is empty.
    - A required section contains only empty strings / empty values.
    """

    required_sections = [
        "education",
        "experience",
        "projects",
        "skills",
    ]

    def has_meaningful_data(value):
        if value is None:
            return False

        if isinstance(value, str):
            return value.strip() != ""

        if isinstance(value, list):
            if len(value) == 0:
                return False
            return any(has_meaningful_data(item) for item in value)

        if isinstance(value, dict):
            if len(value) == 0:
                return False
            return any(has_meaningful_data(v) for v in value.values())

        return True

    for section in required_sections:
        if section not in resume:
            return True

        if not has_meaningful_data(resume[section]):
            return True

    return False


@app.post("/parse")
async def parse(file: UploadFile = File(...)):
    
    extension = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4()}{extension}"
    converter = DocumentConverter()
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    outputpath="result5"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        await file.close()

    #
    valid, message = validate_upload(file_path)

    if not valid:
        
        os.remove(file_path)

        raise HTTPException(
            status_code=400,
            detail=message
        )
    result,type = parsing(file_path,converter)
    alternative_flow=should_run_custom_parser(result)
    #alternative_flow=False
    print("alternative: ",alternative_flow)
    if alternative_flow==True:
        if type=="docling":
            result=parse_cv(file_path)
            print("custom2")
        else:
            result=cv_parse_docling(file_path,converter)
            print("docling2")

    final_result=process_resume(result)
    form_json(final_result,file_path,outputpath)
    return {
        "status": "success",
        "message": "File uploaded successfully.",
        "file_path": file_path
    }



