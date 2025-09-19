from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class DocumentChunkMetadata(BaseModel):
    """
    Metadata associated with each document chunk.
    This provides rich context for downstream tasks like RAG.
    """
    document_id: str
    doc_title: str
    authors: List[str]
    language: str
    section_type: str
    page_number: int
    source_reference: Optional[str] = None
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None

class DocumentChunk(BaseModel):
    """
    Represents a single chunk of a parsed document.
    """
    chunk_id: str # A unique ID for this specific chunk (e.g., "doc1_chunk5")
    text: str
    metadata: DocumentChunkMetadata
    doi: Optional[str] = None

class ParsedDocument(BaseModel):
    """
    Represents a full parsed document, ready for export.
    This is what we'll serialize to the final JSONL format.
    """
    document_id: str
    doc_title: str
    authors: List[str]
    language: str
    chunks: List[DocumentChunk]
    metadata: Dict[str, Any] # For any additional, top-level document metadata
    
    # We'll use this to ensure the final output format is consistent
    def to_jsonl_records(self) -> List[Dict[str, Any]]:
        """
        Converts the parsed document into a list of JSONL-ready dictionaries.
        """
        records = []
        for chunk in self.chunks:
            record = {
                "id": chunk.chunk_id,
                "text": chunk.text,
                "metadata": {
                    "doc_title": self.doc_title,
                    "authors": self.authors,
                    "doi": self.metadata.get("doi"),
                    "section_type": chunk.metadata.section_type,
                    "page_number": chunk.metadata.page_number,
                    "language": self.language
                },
                "source_reference": chunk.metadata.source_reference
            }
            records.append(record)
        return records