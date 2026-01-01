from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.controllers import entries, search
from app.errors import global_exception_handler

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Text Vector Search (PDF)")


app.add_exception_handler(Exception, global_exception_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(entries.router, prefix="/api")
app.include_router(search.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Text Vector Search API. Open /docs for interactive API."}

@app.get("/health")
def health():
    return {"status": "ok"}
