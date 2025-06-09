from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
from datetime import datetime
import shutil

# Create the FastAPI application
app = FastAPI(title="ASMIS Backend", version="1.0.0")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".txt", ".docx", ".pdf"}

def is_valid_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

# Simple test endpoint
@app.get("/")
async def root():
    return {"message": "ASMIS Backend is running!"}

# Health check endpoint  
@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ASMIS Backend"}

@app.post("/upload-transcript")
async def upload_transcript(file: UploadFile):
    try:
        # Validate file extension
        if not is_valid_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Create timestamp prefix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "File uploaded successfully",
                "filename": safe_filename,
                "size": file.size  
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while uploading the file: {str(e)}"
        )
    finally:
        file.file.close()