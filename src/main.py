import os
from src.rag_pipeline import RAGPipeline

def main():
    # Create a sample document if it doesn't exist
    sample_doc = "sample.txt"
    if not os.path.exists(sample_doc):
        with open(sample_doc, "w") as f:
            f.write("This is a sample document about cloud-agnostic AI.\n")
            f.write("We can run on AWS or Azure with the same code.\n")

    pipeline = RAGPipeline()
    print("Indexing document...")
    pipeline.index_document(sample_doc, "sample")

    print("Asking a question...")
    answer = pipeline.answer("What is this document about?")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()