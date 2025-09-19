import hashlib
from langdetect import detect
from typing import Optional

def get_file_hash(file_path: str) -> str:
    """Generates a SHA256 hash for a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def detect_language(text: str) -> Optional[str]:
    """Detects the language of a given text."""
    try:
        return detect(text)
    except:
        return None