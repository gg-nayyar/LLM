import ollama
# import os
import chromadb
from dotenv import load_dotenv

load_dotenv()
# api_key = os.environ.get("API_KEY")

# if not api_key:
#     raise ValueError("API_KEY is missing. Please set it in the .env file.")

# client = openai.OpenAI(api_key=api_key)

chroma_client = chromadb.PersistentClient(path='./db')
collection = chroma_client.get_or_create_collection('legal_docs')

def query_database(query_text: str):
    results = collection.query(
        query_texts=[query_text],
        n_results=1
    )
    return results["documents"][0] if results["documents"] else None
def generate_answer(query_text: str):
    relevant_text = query_database(query_text)
    if not relevant_text:
        return "❌ No relevant legal documents found. Please refine your query."

    prompt = f"""
    You are a legal expert. Answer the following question using the provided legal text:
    
    Legal Text:
    {relevant_text}

    Question:
    {query_text}

    Answer:
    """

    # try:
    response = ollama.chat(
        model="llama2",
        messages=[{"role": "system", "content": prompt}],
    )
    return response["message"]["content"]
    # except openai.RateLimitError:
    #     return "API quota exceeded. Please check your OpenAI plan and billing details."
if __name__ == "__main__":
    user_query = "what is indian constitution?"
    response = generate_answer(user_query)
    print("🤖 AI Answer:", response)
