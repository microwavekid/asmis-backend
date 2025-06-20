from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
from datetime import datetime
import shutil
from dotenv import load_dotenv
from app.agents.meddpic_orchestrator import MEDDPICOrchestrator, SourceType
from app.agents.stakeholder_intelligence_agent import StakeholderIntelligenceAgent
import anthropic
import logging

# Load environment variables
load_dotenv()

# Create the FastAPI application
app = FastAPI(title="ASMIS Backend", version="1.0.0")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# File type to source type mapping
FILE_TYPE_MAPPING = {
    ".txt": SourceType.TRANSCRIPT,
    ".docx": SourceType.REQUIREMENTS_DOC,
    ".pdf": SourceType.REQUIREMENTS_DOC
}

# Initialize orchestrator
try:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
    orchestrator = MEDDPICOrchestrator(
        api_key=api_key,
        config={
            "enable_caching": True,
            "enable_metrics": True,
            "cache_ttl_minutes": 60,
            "extract_action_items": True
        }
    )
except Exception as e:
    raise RuntimeError(f"Failed to initialize orchestrator: {str(e)}")

# Initialize stakeholder intelligence agent
try:
    stakeholder_agent = StakeholderIntelligenceAgent(api_key=api_key)
except Exception as e:
    raise RuntimeError(f"Failed to initialize stakeholder agent: {str(e)}")

logger = logging.getLogger(__name__)

def is_valid_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return os.path.splitext(filename)[1].lower() in FILE_TYPE_MAPPING

def get_source_type(filename: str) -> SourceType:
    """Get the appropriate source type for a file."""
    ext = os.path.splitext(filename)[1].lower()
    return FILE_TYPE_MAPPING.get(ext)

# Simple test endpoint
@app.get("/")
async def root():
    return {"message": "ASMIS Backend is running!"}

# Health check endpoint  
@app.get("/health")
async def health():
    """Get the health status of the orchestrator and its agents."""
    try:
        health_status = await orchestrator.health_check()
        return JSONResponse(
            status_code=200,
            content=health_status
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Health check failed: {str(e)}"
        )

@app.get("/metrics")
async def get_metrics():
    """Get the current performance metrics."""
    try:
        metrics = orchestrator.get_metrics()
        if not metrics:
            raise HTTPException(
                status_code=404,
                detail="Metrics collection is not enabled"
            )
        return JSONResponse(
            status_code=200,
            content=metrics
        )
    except Exception as e:
        logger.error(f"Failed to get metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get metrics: {str(e)}"
        )

@app.post("/analyze-content")
async def analyze_content(file: UploadFile):
    """
    Analyze content from various file types using the appropriate agent.
    Supports transcripts, requirements documents, and other content types.
    """
    try:
        # Validate file extension
        if not is_valid_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(FILE_TYPE_MAPPING.keys())}"
            )
        
        # Read file content
        content = await file.read()
        try:
            text_content = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File must be a valid UTF-8 text file"
            )
        
        # Generate unique source ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        source_id = f"{get_source_type(file.filename).value}_{timestamp}"
        
        # Analyze content using orchestrator
        try:
            logger.info(f"Starting content analysis for {file.filename}")
            analysis_result = await orchestrator.analyze_content(
                content=text_content,
                source_type=get_source_type(file.filename).value,
                source_id=source_id,
                metadata={
                    "filename": file.filename,
                    "size": file.size,
                    "upload_timestamp": timestamp
                }
            )
            logger.info("Content analysis completed successfully")
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Content analyzed successfully",
                    "filename": file.filename,
                    "source_type": get_source_type(file.filename).value,
                    "analysis_result": analysis_result
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
                detail=f"Failed to analyze content: {str(e)}"
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

@app.post("/clear-cache")
async def clear_cache():
    """Clear the orchestrator's analysis cache."""
    try:
        orchestrator.clear_cache()
        return JSONResponse(
            status_code=200,
            content={"message": "Cache cleared successfully"}
        )
    except Exception as e:
        logger.error(f"Failed to clear cache: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear cache: {str(e)}"
        )

@app.post("/analyze-stakeholders")
async def analyze_stakeholders(file: UploadFile):
    """
    Analyze stakeholders from a sales meeting transcript.
    """
    try:
        # Validate file extension
        if not is_valid_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(FILE_TYPE_MAPPING.keys())}"
            )
        
        # Read file content
        content = await file.read()
        try:
            text_content = content.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File must be a valid UTF-8 text file"
            )
        
        # Analyze stakeholders
        try:
            logger.info(f"Starting stakeholder analysis for {file.filename}")
            analysis_result = await stakeholder_agent.analyze_stakeholders(
                transcript=text_content
            )
            logger.info("Stakeholder analysis completed successfully")
            
            return JSONResponse(
                status_code=200,
                content={
                    "message": "Stakeholder analysis completed successfully",
                    "filename": file.filename,
                    "analysis_result": analysis_result
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
                detail=f"Failed to analyze stakeholders: {str(e)}"
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