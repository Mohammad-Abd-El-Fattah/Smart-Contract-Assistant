import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_document(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at path: {file_path}")

    try:
        print(f"Reading file: {file_path} ...")
        
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()
        
        print(f"Successfully read {len(documents)} pages.")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        
        print("Splitting text into chunks...")
        
        chunks = text_splitter.split_documents(documents)
        
        print(f"File split into {len(chunks)} text chunks.")
        
        return chunks

    except Exception as e:
        print(f"An error occurred while processing the document: {e}")
        return []

if __name__ == "__main__":
    test_pdf_path = "../data/sample_contract.pdf"
    
    os.makedirs("../data", exist_ok=True)
    
    if os.path.exists(test_pdf_path):
        test_chunks = process_document(test_pdf_path)
        
        if test_chunks:
            print("\n--- Sample of the first text chunk ---")
            print(test_chunks[0].page_content)
            
            print("\n--- Metadata ---")
            print(test_chunks[0].metadata)
    else:
        print("Please place a file named 'sample_contract.pdf' in the 'data' folder to test the code.")