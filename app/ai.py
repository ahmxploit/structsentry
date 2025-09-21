from __future__ import annotations
import os
from typing import Optional
def summarize(prompt: str, context: Optional[str] = None) -> str:
    key = os.getenv('GEMINI_API_KEY', '').strip()
    if not key:
        base = (context or '')[:4000]
        return f'AI not configured. Prompt:\n{prompt}\n\nContext:\n{base}'
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        full = f"You are StructSentry assistant. Prompt: {prompt}\nContext:\n{context or ''}\nProvide concise remediation steps."
        resp = model.generate_content(full)
        return (resp.text or '').strip() or 'No response.'
    except Exception as e:
        return f'AI error: {e}'
