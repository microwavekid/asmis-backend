from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
import shutil
from dotenv import load_dotenv
from app.agents.meddpic_orchestrator import MEDDPICCOrchestrator, SourceType
from app.routers import task_router
from app.routers.router_config import get_deals_router, get_router_mode, get_auth_mode
from app.api import smart_capture
from app.database.connection import async_db_manager, db_manager
import anthropic
import logging

# Load environment variables
load_dotenv()

# Create the FastAPI application
app = FastAPI(
    title="ASMIS Backend", 
    version="1.0.0",
    description="ASMIS - AI Sales Intelligence System"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
# Authentication router (only if JWT auth is enabled)
if get_auth_mode() == "JWT":
    from app.routers.auth import router as auth_router
    app.include_router(auth_router)

# Use configurable deals router (stub or real based on environment)
deals_router = get_deals_router()
app.include_router(deals_router)
app.include_router(smart_capture.router)
app.include_router(task_router)

# Log which modes are active
logger = logging.getLogger(__name__)
logger.info(f"Using {get_router_mode()} routers for deals API")
logger.info(f"Using {get_auth_mode()} authentication mode")


@app.on_event("startup")
async def startup_event():
    """Initialize database connections on startup."""
    try:
        # Initialize both sync and async database managers
        db_manager.initialize()
        async_db_manager.initialize()
        logger.info("Database connections initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown."""
    try:
        # Close both sync and async database managers
        db_manager.close()
        await async_db_manager.close()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {e}")

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
    orchestrator = MEDDPICCOrchestrator(
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