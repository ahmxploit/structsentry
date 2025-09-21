# StructSentry — Structural Data Inspector (Modernized for Python 3.13)

**StructSentry** inspects structured data (JSON, YAML, CSV) for schema issues, suspicious values, and data-quality anomalies. This modernized release targets **Python 3.13**, adds robust type safety, Pydantic v2 models, an async FastAPI backend, and a Streamlit front-end for instant exploration.

---

## Highlights
- Schema validation using **Pydantic v2** and custom heuristics.  
- Quick scanning endpoints: `/health`, `/scan-raw`, `/scan-file`, `/chat` (optional Gemini).  
- Streamlit UI for upload, preview, validation reports, and AI-assisted remediation suggestions.  
- Docker-ready, fully tested with **pytest**.  
- Optional Gemini integration for natural-language remediation suggestions.

---

## Quick start (dev)
```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# In another terminal:
streamlit run ui/streamlit_app.py
```

## API
- `GET /health` — readiness check.  
- `POST /scan` — multipart form with files or inline text (JSON/YAML/CSV). Returns structured findings.  
- `POST /chat` — ask AI to summarize findings or propose fixes (Gemini API optional).

## Project layout
```
structsentry_py313/
├─ app/               # backend (FastAPI)
├─ ui/                # Streamlit UI
├─ tests/             # pytest tests
├─ requirements.txt
├─ Dockerfile
└─ README.md
```

---

## License
MIT. Use, modify, distribute.
