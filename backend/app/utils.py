import re
import json
from typing import List
from langchain.text_splitter import NLTKTextSplitter

# Helper function to clean text by removing extra spaces and newlines
def clean_text(text: str) -> str:
    # Normalize multiple newlines and spaces
    text = re.sub(r'\s{2,}', ' ', text)
    text = text.strip()
    return text

# Helper function to mark sections in the text
def mark_sections(text: str) -> str:
    # Insert double newlines before all-caps or heading-like lines
    text = re.sub(r"(?<!\n)\n(?=[A-Z][^\n]{2,50}\n)", r"\n\n", text)
    return text

# Helper function to chunk text into smaller segments
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100):
    splitter = NLTKTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap, separator="\n\n")
    clean_text_out = mark_sections(text)
    clean_text_out = clean_text(clean_text_out)
    return splitter.split_text(clean_text_out)
