from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from app.struct_evaluator import decode_xrd
from app.recommender import recommend_structures

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
def analyze_xrd(
    xrd_pattern: str = Form(...),
    notes: str = Form(""),
    language: str = Form("english")
):
    decoded = decode_xrd(xrd_pattern, notes, language)
    recommendation = recommend_structures(decoded["structure"], notes, language)
    return {
        "structure": decoded,
        "recommendation": recommendation
    }