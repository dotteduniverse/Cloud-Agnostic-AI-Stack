import os
import tempfile
from src.storage import get_storage_client
from src.ai_interface import get_ai_client

class RAGPipeline:
    def __init__(self):
        self.storage = get_storage_client()
        self.ai = get_ai_client()

    def index_document(self, local_path: str, doc_id: str):
        """Upload a document to cloud storage."""
        self.storage.upload_file(local_path, f"documents/{doc_id}")

    def retrieve(self, query: str) -> str:
        """Simple retrieval: list all docs and return the content of the first (for demo)."""
        # In a real scenario you'd use vector search; this is just a placeholder.
        files = self.storage.list_files(prefix="documents/")
        if not files:
            return "No documents found."
        # Download the first document
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            self.storage.download_file(files[0], tmp.name)
            with open(tmp.name, "r") as f:
                content = f.read()
        return content[:2000]  # limit

    def answer(self, question: str) -> str:
        context = self.retrieve(question)
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        return self.ai.generate(prompt)