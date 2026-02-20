import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from vectorstore import load_vectorstore

load_dotenv()

def setup_qa_chain():
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("GITHUB_TOKEN"),
        base_url="https://models.inference.ai.azure.com"
    )
    
    prompt_template = """
    You are a strict and professional legal assistant.
    Use the following pieces of retrieved context from a contract to answer the user's question. 
    If you cannot find the answer in the provided context, clearly state: "I'm sorry, but this information is not available in the provided document." 
    Do not hallucinate or make up any information.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:
    """
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    return llm, prompt

def ask_question(query: str):
    try:
        db = load_vectorstore()
    except FileNotFoundError as e:
        return str(e), []

    docs = db.similarity_search(query, k=3)
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])
    
    llm, prompt = setup_qa_chain()
    
    formatted_prompt = prompt.format(context=context_text, question=query)
    
    response = llm.invoke(formatted_prompt)
    
    sources = [{"page": doc.metadata.get("page", "Unknown"), "content": doc.page_content[:150]} for doc in docs]
    
    return response.content, sources

if __name__ == "__main__":
    if not os.getenv("GITHUB_TOKEN"):
        print("Please set your GITHUB_TOKEN in your .env file to test the LLM.")
    else:
        test_query = "What is the termination clause?"
        print(f"Asking: {test_query}\n")
        
        answer, citation_sources = ask_question(test_query)
        
        print("--- Answer ---")
        print(answer)
        print("\n--- Sources ---")
        for i, source in enumerate(citation_sources):
            print(f"Source {i+1} (Page {source['page']}): {source['content']}...")