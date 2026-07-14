from fastapi import FastAPI
from fastapi import UploadFile, File, HTTPException
import os
from file_validator import validate_upload
import shutil
import uuid



app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return{
        "message": "Boolmind cv parser"
        }

@app.post("/parse")
async def parse(file: UploadFile = File(...)):
    
    extension = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    
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

    return {
        "status": "success",
        "message": "File uploaded successfully.",
        "file_path": file_path
    }



