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
You are a materials science AI.

Given the following XRD pattern data and notes, output the result in JSON format like:

{
  "structure": "FCC / BCC / HCP / amorphous / layered / unknown",
  "confidence": "High / Medium / Low",
  "justification": "Explain why the structure was selected based on peaks or known references"
}

XRD Pattern:
{pattern}

Notes:
{notes}

Respond only in JSON format in {language}.
""")

    chain = prompt | get_llm()
    return chain.invoke({
        "pattern": pattern,
        "notes": notes,
        "language": language
    })