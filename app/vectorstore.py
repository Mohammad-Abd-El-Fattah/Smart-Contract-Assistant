import os
import sys
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DB_PATH = "../faiss_index"

def create_vectorstore(chunks):
    print("Loading embeddings model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Converting text to vectors and saving to FAISS...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    vectorstore.save_local(DB_PATH)
    print(f"Vector store successfully saved to: {DB_PATH}")
    
    return vectorstore

def load_vectorstore():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Vector store not found. Please upload and process a document first.")
        
    print("Loading vector store for retrieval...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    
    print("Vector store loaded successfully. Ready for queries.")
    return vectorstore

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from ingest import process_document
        
        test_pdf = "../data/sample_contract.pdf"
        
        if os.path.exists(test_pdf):
            print("\n--- 1. Document Reading Phase ---")
            chunks = process_document(test_pdf)
            
            if chunks:
                print("\n--- 2. Embedding & Vector Storage Phase ---")
                create_vectorstore(chunks)
                
                print("\n--- 3. Retrieval Test ---")
                db = load_vectorstore()
                
                query = "What is the term of this contract?"
                
                results = db.similarity_search(query, k=2) 
                
                print(f"\n🔍 Search results for: '{query}'")
                for i, res in enumerate(results):
                    print(f"\n--- Result {i+1} ---")
                    print(f"Text: {res.page_content[:200]}...")
                    print(f"Source: Page {res.metadata.get('page', 'Unknown')}")
        else:
            print("Please place a file named 'sample_contract.pdf' in the 'data' folder to test the code.")
            
    except Exception as e:
        print(f"An error occurred during testing: {e}")