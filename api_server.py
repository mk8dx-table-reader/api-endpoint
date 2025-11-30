"""
FastAPI Web API for MK8DX Table Reader

This API provides endpoints to upload game screenshots and extract
player names and scores using the mk8dx_table_reader package.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from typing import Optional, List
import logging
import warnings

# Import the Fullreader from your package
from mk8dx_table_reader.fullreader import Fullreader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VERSION = "1.1.1"

# Create FastAPI app
app = FastAPI(
    title="MK8DX Table Reader API",
    description="API for extracting player names and scores from Mario Kart 8 Deluxe screenshots",
    version=VERSION,
)

# Add CORS middleware to allow requests from web browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Fullreader (loaded once at startup)
fullreader = None


@app.on_event("startup")
async def startup_event():
    """Initialize the Fullreader model on server startup"""
    global fullreader
    logger.info("Loading MK8DX Table Reader models...")
    try:
        fullreader = Fullreader()
        logger.info("Models loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        raise

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "MK8DX Table Reader API is running",
        "version": VERSION,
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {"status": "healthy", "models_loaded": fullreader is not None}


@app.post("/api/v1/read-table")
async def read_table(file: UploadFile = File(...), score_error_exceptions: bool = False):
    """
    Upload an image and extract player names and scores

    Parameters:
    - file: Image file (PNG, JPG, JPEG)
    - teams: Team mode (default: "FFA")

    Returns:
    - JSON with player names and scores
    """

    # Validate file type
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="File must be an image (PNG, JPG, JPEG)"
        )

    try:
        # Read the uploaded file
        contents = await file.read()

        # Convert to PIL Image
        image = Image.open(io.BytesIO(contents))

        logger.info(f"Processing image: {file.filename}")

        # Process the image using Fullreader
        list_warnings = []
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = fullreader.fullOCR(image, score_error_exceptions=score_error_exceptions)
            for warning in w:
                list_warnings.append(str(warning.message))
        

        if result is None:
            raise HTTPException(
                status_code=422,
                detail="No table detected in the image. Please ensure the image contains a valid MK8DX results table.",
            )

        player_names, player_scores = result

        # Format the response
        players = []
        for i, (name, score) in enumerate(zip(player_names, player_scores)):
            players.append({"position": i + 1, "name": name, "score": score})

        return {
            "success": True,
            "warnings": list_warnings if 'list_warnings' in locals() else False,
            "table_detected": True,
            "player_count": len(players),
            "players": players,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    # Run the server
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (disable in production)
        log_level="info",
    )
