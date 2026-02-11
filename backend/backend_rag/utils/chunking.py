import re
from typing import List, Dict, Any
from config.settings import settings


def chunk_text(text: str, chunk_size: int = None, overlap_size: int = None) -> List[Dict[str, Any]]:
    """
    Split text into semantic chunks with overlap
    """
    if chunk_size is None:
        chunk_size = settings.CHUNK_SIZE
    if overlap_size is None:
        overlap_size = settings.OVERLAP_SIZE
    
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    chunks = []
    current_chunk = ""
    current_chunk_size = 0
    chunk_index = 0
    
    for sentence in sentences:
        sentence_size = len(sentence.split())
        
        # If adding this sentence would exceed chunk size
        if current_chunk_size + sentence_size > chunk_size and current_chunk:
            # Save the current chunk
            chunks.append({
                "content": current_chunk.strip(),
                "chunk_index": chunk_index
            })
            
            # Start a new chunk with overlap
            overlap_sentences = get_overlap_sentences(current_chunk, overlap_size)
            current_chunk = overlap_sentences + " " + sentence
            current_chunk_size = len(current_chunk.split())
            chunk_index += 1
        else:
            # Add sentence to current chunk
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
            current_chunk_size += sentence_size
    
    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append({
            "content": current_chunk.strip(),
            "chunk_index": chunk_index
        })
    
    return chunks


def get_overlap_sentences(chunk: str, overlap_size: int) -> str:
    """
    Get the last overlap_size tokens from a chunk
    """
    words = chunk.split()
    if len(words) <= overlap_size:
        return chunk
    
    # Get the last overlap_size words
    overlap_words = words[-overlap_size:]
    return " ".join(overlap_words)


def chunk_book_content(book_content: str, book_id: str) -> List[Dict[str, Any]]:
    """
    Chunk book content with metadata
    """
    chunks = chunk_text(book_content)
    
    # Add metadata to each chunk
    for i, chunk in enumerate(chunks):
        chunk["book_id"] = book_id
        chunk["id"] = f"{book_id}_chunk_{i}"
        chunk["metadata"] = {"chunk_index": i}
    
    return chunks