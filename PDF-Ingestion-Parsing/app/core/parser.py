# app/core/parser.py

import fitz  # PyMuPDF
import re
import os
import uuid
from typing import List, Dict, Any

# Corrected import from paddleocr
from paddleocr import PaddleOCR
from PIL import Image
from io import BytesIO

from app.core.models import ParsedDocument, DocumentChunk, DocumentChunkMetadata
from app.core.utils import detect_language

# Heuristic patterns for section titles (academic papers)
SECTION_PATTERNS = {
    "abstract": re.compile(r"^\s*abstract\s*$", re.IGNORECASE),
    "introduction": re.compile(r"^\s*1\.?\s*introduction\s*$", re.IGNORECASE),
    "related_work": re.compile(r"^\s*\d\.?\s*related\s+work\s*$", re.IGNORECASE),
    "methods": re.compile(r"^\s*\d\.?\s*methods\s*$", re.IGNORECASE),
    "results": re.compile(r"^\s*\d\.?\s*results\s*$", re.IGNORECASE),  # This is the corrected line
    "conclusion": re.compile(r"^\s*\d\.?\s*conclusion\s*$", re.IGNORECASE),
    "references": re.compile(r"^\s*references\s*$", re.IGNORECASE),
    # Add more patterns as needed
}

def clean_text(text: str) -> str:
    """Removes common PDF artifacts and cleans text."""
    # Remove headers, footers, and page numbers (simple heuristic)
    text = re.sub(r'\s*Page\s+\d+\s*|\s*\d+\s*/\s*\d+\s*', '', text, flags=re.IGNORECASE)
    # Normalize multiple newlines to a single one
    text = re.sub(r'[\r\n]+', '\n', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

class PDFParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.doc = fitz.open(self.file_path)
        self.doc_id = str(uuid.uuid4())
        self.text_content = ""
        self.pages_data: List[Dict] = []
        # Initialize PaddleOCR once for the entire class instance
        self.ocr_engine = PaddleOCR(use_angle_cls=True, lang="en")

    def _extract_text_with_pypdf(self) -> str:
        """Extracts text using PyMuPDF."""
        full_text = ""
        self.pages_data = []

        for page_num, page in enumerate(self.doc):
            text = page.get_text("text")
            full_text += text + "\n"
            
            # Store page data for later use
            self.pages_data.append({"page_number": page_num + 1, "text": text})

        return full_text

    def _extract_text_with_ocr(self) -> str:
        """Applies OCR as a fallback using PaddleOCR."""
        full_text = ""
        self.pages_data = []

        for page_num, page in enumerate(self.doc):
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # The result is a list of lists. We need to extract the text.
            ocr_result = self.ocr_engine.ocr(img, cls=True)
            
            page_text = ""
            if ocr_result and ocr_result[0] is not None:
                # The first element is the text, the second is the confidence score
                texts = [line[1][0] for line in ocr_result[0]]
                page_text = " ".join(texts)
                
            full_text += page_text + "\n"
            self.pages_data.append({"page_number": page_num + 1, "text": page_text})

        return full_text

    def _parse_structure_and_chunk(self) -> List[DocumentChunk]:
        """Identifies sections and chunks the text with metadata."""
        chunks: List[DocumentChunk] = []
        current_section = "unknown"
        current_chunk_text = ""
        chunk_id_counter = 0

        # Heuristically parse document-level metadata
        doc_title = "Untitled Document"
        authors = ["Unknown Author"]
        # Simple heuristic: try to get title/authors from first page
        first_page_text = self.pages_data[0]["text"]
        lines = first_page_text.split('\n')
        # A more robust solution would use a dedicated NLP model
        if lines:
            doc_title = lines[0].strip() if lines[0].strip() else "Untitled Document"
            # Attempt to find common author patterns (not robust)
            for line in lines[1:]:
                if '@' in line:
                    authors = [line.strip()] # Simplistic, but a start

        # Process page by page, line by line
        for page_data in self.pages_data:
            text = page_data["text"]
            lines = text.split('\n')
            
            for line_num, line in enumerate(lines):
                # Check for new section based on patterns
                for section_name, pattern in SECTION_PATTERNS.items():
                    if pattern.search(line):
                        current_section = section_name
                        if current_chunk_text:
                            # Finalize the previous chunk before starting a new section
                            chunk_id = f"{self.doc_id}_chunk{chunk_id_counter}"
                            metadata = DocumentChunkMetadata(
                                document_id=self.doc_id,
                                doc_title=doc_title,
                                authors=authors,
                                language=self.language,
                                section_type=current_section,
                                page_number=page_data["page_number"]
                            )
                            chunks.append(DocumentChunk(chunk_id=chunk_id, text=current_chunk_text, metadata=metadata))
                            current_chunk_text = ""
                            chunk_id_counter += 1
                        break
                
                # Append line to current chunk
                cleaned_line = clean_text(line)
                if cleaned_line:
                    current_chunk_text += " " + cleaned_line

                # Chunking logic (simple token-based check)
                if len(current_chunk_text.split()) >= 500:
                    chunk_id = f"{self.doc_id}_chunk{chunk_id_counter}"
                    metadata = DocumentChunkMetadata(
                        document_id=self.doc_id,
                        doc_title=doc_title,
                        authors=authors,
                        language=self.language,
                        section_type=current_section,
                        page_number=page_data["page_number"]
                    )
                    chunks.append(DocumentChunk(chunk_id=chunk_id, text=current_chunk_text, metadata=metadata))
                    current_chunk_text = ""
                    chunk_id_counter += 1
        
        # Add the last remaining chunk
        if current_chunk_text:
            chunk_id = f"{self.doc_id}_chunk{chunk_id_counter}"
            metadata = DocumentChunkMetadata(
                document_id=self.doc_id,
                doc_title=doc_title,
                authors=authors,
                language=self.language,
                section_type=current_section,
                page_number=self.pages_data[-1]["page_number"]
            )
            chunks.append(DocumentChunk(chunk_id=chunk_id, text=current_chunk_text, metadata=metadata))
            
        return chunks

    def process(self) -> ParsedDocument:
        """Main processing function to orchestrate the pipeline."""
        try:
            # First, try to extract text normally
            self.text_content = self._extract_text_with_pypdf()
            
            # Simple check if extraction failed, or if text is too short
            if not self.text_content.strip() or len(self.text_content.strip()) < 100:
                print("PyMuPDF extraction failed or returned too little text. Applying OCR fallback.")
                self.text_content = self._extract_text_with_ocr()

            self.language = detect_language(self.text_content)
            
            chunks = self._parse_structure_and_chunk()

            # Placeholder for top-level metadata
            doc_metadata = {"doi": None}

            # A simplistic way to find DOI (not robust)
            doi_match = re.search(r'doi:\s*(\S+)', self.text_content, re.IGNORECASE)
            if doi_match:
                doc_metadata["doi"] = doi_match.group(1).rstrip('.')
            
            # Find the title and authors from the first chunk's metadata
            if chunks:
                doc_title = chunks[0].metadata.doc_title
                authors = chunks[0].metadata.authors
            else:
                doc_title = "Untitled Document"
                authors = ["Unknown Author"]
            
            # Create the final ParsedDocument object
            parsed_doc = ParsedDocument(
                document_id=self.doc_id,
                doc_title=doc_title,
                authors=authors,
                language=self.language,
                chunks=chunks,
                metadata=doc_metadata
            )
            
            return parsed_doc

        except Exception as e:
            print(f"Error processing document {self.file_path}: {e}")
            return None