# **📜 Smart Contract Summary & Q\&A Assistant**

An AI-powered legal assistant that uses **RAG (Retrieval-Augmented Generation)** to analyze PDF contracts. It allows users to upload documents and ask specific questions, providing grounded answers with direct source citations from the text.

## **🚀 Features**

* **PDF Ingestion:** Uses PyMuPDF for fast and accurate text extraction.  
* **Intelligent Chunking:** Implements RecursiveCharacterTextSplitter to preserve legal context.  
* **Vector Database:** Uses FAISS and HuggingFace embeddings for high-speed semantic search.  
* **LLM Integration:** Powered by **GitHub Models (GPT-4o-mini)** for high-quality, free-tier AI processing.  
* **Strict Guardrails:** Prompt engineering ensures the AI only answers based on the provided document (no hallucinations).  
* **Interactive UI:** A modern web interface built with Gradio.

## **🛠️ Tech Stack**

* **Language:** Python 3.12+  
* **Orchestration:** LangChain  
* **Frontend:** Gradio  
* **Database:** FAISS (Facebook AI Similarity Search)  
* **AI Model:** GPT-4o-mini (via GitHub Models API)

## **📋 Prerequisites**

* A GitHub account with a **Personal Access Token (PAT)**.  
* Python installed on your system.

## **⚙️ Installation & Setup**

1. **Clone the repository:**  
   git clone \[https://github.com/yourusername/smart-contract-assistant.git\](https://github.com/yourusername/smart-contract-assistant.git)  
   cd smart-contract-assistant

2. **Set up Environment Variables:**  
   Create a .env file in the root directory:  
   GITHUB\_TOKEN="your\_github\_pat\_here"

3. **Install Dependencies:**  
   pip install \-r requirements.txt \--user

## **🏃 How to Run**

1. **Navigate to the app directory:**  
   cd app

2. **Launch the Web UI:**  
   python ui.py

3. **Usage:**  
   * Go to the **Upload** tab and select your PDF.  
   * Click **Process Document**.  
   * Switch to the **Chat** tab and start asking questions\!

## **📂 Project Structure**

* app/ingest.py: Document loading and text splitting logic.  
* app/vectorstore.py: Embedding generation and FAISS database management.  
* app/retriever.py: RAG logic and LLM connection settings.  
* app/ui.py: Gradio web interface and server logic.  
* data/: Directory for input PDF files.  
* faiss\_index/: Local storage for the generated vector database.