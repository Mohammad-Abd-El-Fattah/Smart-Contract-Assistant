import gradio as gr
import os
from ingest import process_document
from vectorstore import create_vectorstore
from retriever import ask_question

def handle_upload(file):
    if file is None:
        return "Please upload a document first."
    
    try:
        chunks = process_document(file.name)
        if not chunks:
            return "Failed to extract text from the document. The PDF might be scanned or empty."
        
        create_vectorstore(chunks)
        return "✅ Document processed and knowledge base updated successfully! You can now go to the Chat tab."
    except Exception as e:
        return f"❌ Error processing file: {e}"

def handle_chat(message, history):
    answer, sources = ask_question(message)
    
    response = answer + "\n\n### 🔍 Sources:\n"
    for i, source in enumerate(sources):
        response += f"- **Source {i+1} (Page {source['page']}):** {source['content']}...\n"
        
    return response

with gr.Blocks(title="Smart Contract Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📜 Smart Contract Summary & Q&A Assistant")
    gr.Markdown("Upload your contract (PDF) and ask questions. The AI will answer based **ONLY** on the uploaded document.")
    
    with gr.Tab("1. Upload Document"):
        file_input = gr.File(label="Upload Contract (PDF)", file_types=[".pdf"])
        upload_button = gr.Button("Process Document", variant="primary")
        upload_status = gr.Textbox(label="System Status", interactive=False)
        
        upload_button.click(fn=handle_upload, inputs=file_input, outputs=upload_status)
        
    with gr.Tab("2. Chat with Contract"):
        chat_interface = gr.ChatInterface(
            fn=handle_chat,
            examples=["What is the termination clause?", "What is the total payment amount?", "What is the duration of this contract?"],
            title="Ask your contract anything!"
        )

if __name__ == "__main__":
    print("Starting Web Server...")
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)