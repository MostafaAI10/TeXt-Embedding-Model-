from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import logging

logger = logging.getLogger("app")

async def global_exception_handler(request: Request, exc: Exception):
    
    logger.error("Unhandled exception", exc_info=exc)
    print("\n--- ERROR TRACEBACK ---")
    traceback.print_exc()
    print("--- END TRACEBACK ---\n")
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": exc.__class__.__name__,
            "message": "An unexpected error occurred."
        },
    )
