import os
import sys
import logging
import traceback
from fastapi import FastAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add root directory to sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

try:
    # Try to import the real app
    from main import app
    logger.info("Successfully imported FastAPI app from main.py")
except Exception as e:
    # If import fails, create a FALLBACK app to show the error in the browser
    error_trace = traceback.format_exc()
    logger.error(f"CRITICAL: Failed to import app: {e}")
    
    app = FastAPI(title="Talenta Crash Reporter")
    
    @app.get("/")
    @app.get("/{path:path}")
    def crash_report(path: str = None):
        return {
            "status": "crash",
            "error_type": type(e).__name__,
            "error_message": str(e),
            "suggestion": "Check if you have added all Environment Variables in the Vercel Dashboard.",
            "traceback": error_trace.split("\n")
        }
