from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .schemas import (
    QARequest,
    ExplainRequest,
    TextRequest,
    LearningPathRequest,
)

from .services import (
    answer_question,
    explain_topic,
    summarize,
    generate_quiz,
    learning_recommendations,
)


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="EduGenie - Gemini 3.8 Flash",
    version="1.0.0",
    description="AI-powered educational assistant using Google Gemini 3.8 Flash.",
)


# --------------------------------------------------
# Static files
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


# --------------------------------------------------
# Templates
# --------------------------------------------------

templates = Jinja2Templates(
    directory=TEMPLATES_DIR
)


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie",
        "model": "gemini-3.8-flash",
    }


# --------------------------------------------------
# Q&A
# --------------------------------------------------

@app.post("/qa")
async def qa(request: QARequest):
    try:
        answer = answer_question(request)

        return {
            "answer": answer
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# --------------------------------------------------
# Explain topic
# --------------------------------------------------

@app.post("/explain")
async def explain(request: ExplainRequest):
    try:
        explanation = explain_topic(request)

        return {
            "explanation": explanation
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# --------------------------------------------------
# Summarize
# --------------------------------------------------

@app.post("/summarize")
async def summarize_text(request: TextRequest):
    try:
        summary = summarize(request)

        return {
            "summary": summary
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# --------------------------------------------------
# Quiz
# --------------------------------------------------

@app.post("/quiz")
async def quiz(request: TextRequest):
    try:
        return generate_quiz(request)

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# --------------------------------------------------
# Learning recommendations
# --------------------------------------------------

@app.post("/learn/recommendations")
async def recommendations(request: LearningPathRequest):
    try:
        return learning_recommendations(request)

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )