import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.2,
        google_api_key=os.getenv("GEMINI_API_KEY"),
        model_kwargs={"stream": False}
    )

def decode_xrd(pattern: str, notes: str, language: str):
    prompt = ChatPromptTemplate.from_template("""
You are a material science agent. Analyze the given XRD pattern and output the following in JSON:

{{
  "structure": "e.g. FCC / BCC / HCP / amorphous / layered",
  "confidence": "High / Medium / Low",
  "justification": "Why this structure fits the pattern"
}}

XRD Pattern:
{pattern}

Notes:
{notes}

Language: {language}
""")

    chain = prompt | get_llm()
    return chain.invoke({"pattern": pattern, "notes": notes, "language": language})