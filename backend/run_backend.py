import sys
import os
from dotenv import load_dotenv
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load env
load_dotenv(os.path.join(BASE_DIR, "backend_rag", ".env"))

# Add backend_rag to path
sys.path.insert(0, os.path.join(BASE_DIR, "backend_rag"))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8005,
        reload=True
    )
