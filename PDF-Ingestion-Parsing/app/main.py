import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from typing import List, Dict, Any

from app.core.parser import PDFParser

# Initialize FastAPI app
app = FastAPI(
    title="PDF Ingestion & Parsing API",
    description="API for ingesting, parsing, and chunking PDFs into training-ready JSONL format.",
    version="1.0.0"
)

# Configure CORS to allow communication from our local Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, this would be a specific URL like "http://localhost:8501"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for a simple health check
@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Parser API! Use /docs to see the API endpoints."}

@app.post("/api/docs/upload", response_model=List[Dict[str, Any]])
async def upload_pdf(file: UploadFile = File(...)):
    """
    Handles PDF upload, parsing, and returns structured data.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_file_path = tmp.name
    
    parser = None
    try:
        # Process the PDF using our custom parser
        parser = PDFParser(file_path=temp_file_path)
        parsed_doc = parser.process()
        
        if parsed_doc:
            # Convert the parsed data to the JSONL format
            jsonl_records = parsed_doc.to_jsonl_records()
            return jsonl_records
        else:
            raise HTTPException(status_code=500, detail="Failed to process the PDF document.")

    except Exception as e:
        # Catch any exceptions during processing and return a 500 error
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")

    finally:
        # **CRITICAL FIX**: Explicitly close the fitz document object before unlinking the file
        if parser and parser.doc:
            parser.doc.close()
        
        # Clean up the temporary file
        os.unlink(temp_file_path)