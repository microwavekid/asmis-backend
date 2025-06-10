from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
from datetime import datetime
import shutil
from dotenv import load_dotenv
from app.meeting_intelligence import MeetingIntelligenceAgent
from app.action_items_agent import ActionItemsAgent
import anthropic
import logging

# Load environment variables
load_dotenv()

# Create the FastAPI application
app = FastAPI(title="ASMIS Backend", version="1.0.0")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {".txt", ".docx", ".pdf"}

# Initialize agents
try:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    meeting_agent = MeetingIntelligenceAgent(api_key=api_key)
    action_items_agent = ActionItemsAgent(api_key=api_key)
except Exception as e:
    raise RuntimeError(f"Failed to initialize agents: {str(e)}")

logger = logging.getLogger(__name__)

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

@app.post("/analyze-transcript")
async def analyze_transcript(file: UploadFile):
    try:
        # Validate file extension
        if not is_valid_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Read file content
        content = await file.read()
        try:
            transcript_text = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File must be a valid UTF-8 text file"
            )
        
        # Analyze transcript
        try:
            logger.info("Starting MEDDPIC analysis")
            meddpic_analysis = await meeting_agent.extract_meddpic(transcript_text)
            logger.info("MEDDPIC analysis completed successfully")
            
            logger.info("Starting action items analysis")
            action_items_analysis = await action_items_agent.extract_action_items(transcript_text)
            logger.info("Action items analysis completed successfully")
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Transcript analyzed successfully",
                    "filename": file.filename,
                    "meddpic_analysis": meddpic_analysis,
                    "action_items_analysis": action_items_analysis
                }
            )
        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Anthropic API error: {str(e)}"
            )
        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze transcript: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the file: {str(e)}"
        )
    finally:
        await file.close()