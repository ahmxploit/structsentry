import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3,
        google_api_key=os.getenv("GEMINI_API_KEY"),
        model_kwargs={"stream": False}
    )

def recommend_structures(structure: str, notes: str, language: str):
    prompt = ChatPromptTemplate.from_template("""
You are an AI assistant trained in materials science.

Given the identified structure type: {structure}, return:

1. Three candidate materials (e.g., metals or alloys)
2. Suggested processing techniques (e.g., annealing, sintering)
3. Typical applications

Be concise and format the result clearly for a technical audience. Use the notes below if relevant.

Structure: {structure}
Notes: {notes}
Language: {language}
""")

    chain = prompt | get_llm()
    return chain.invoke({
        "structure": structure,
        "notes": notes,
        "language": language
    })