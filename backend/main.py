from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import re

app = FastAPI(title="AI Exam Answer Explainer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class AnswerInput(BaseModel):
    question: str
    answer: str
    total_marks: int

class FeedbackResponse(BaseModel):
    score: int
    confidence_level: str
    mistakes: List[str]
    explanation: str
    how_to_improve: str
    correct_answer: List[str]

# ---------- AI Helpers ----------
def extract_keywords(text: str):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z ]", "", text)
    return list(set([w for w in text.split() if len(w) > 4]))

def expected_depth(marks: int):
    if marks <= 2:
        return "definition and key term"
    elif marks <= 5:
        return "brief explanation with 2–3 points"
    elif marks <= 8:
        return "detailed explanation with reasoning"
    else:
        return "in-depth explanation with examples and structure"

# ---------- Routes ----------
@app.get("/")
def home():
    return {"status": "AI Exam Answer Explainer running 🚀"}

@app.post("/analyze", response_model=FeedbackResponse)
def analyze(data: AnswerInput):

    question_concepts = extract_keywords(data.question)
    answer_text = data.answer.lower()

    matched = [c for c in question_concepts if c in answer_text]
    missing = [c for c in question_concepts if c not in answer_text]

    coverage = len(matched) / max(len(question_concepts), 1)
    score = int(coverage * data.total_marks)

    if score >= 0.75 * data.total_marks:
        confidence = "High Understanding"
    elif score >= 0.4 * data.total_marks:
        confidence = "Moderate Understanding"
    else:
        confidence = "Low Understanding"

    mistakes = []
    if missing:
        mistakes.append(
            f"Missing key concepts expected for a {data.total_marks}-mark answer: {', '.join(missing)}"
        )
    else:
        mistakes.append("All expected concepts are covered.")

    explanation = (
        "The AI evaluates the answer based on the depth expected for the "
        "marks allocated and checks whether key concepts are clearly explained, "
        "similar to a human examiner."
    )

    how_to_improve = (
        f"For a {data.total_marks}-mark question, the answer should show "
        f"{expected_depth(data.total_marks)}. Focus on clearly explaining "
        "each expected concept."
    )

    # ✅ Correct Answer (Expected Structure)
    correct_answer = [
        f"Clear introduction / definition related to the question",
        f"Explanation showing {expected_depth(data.total_marks)}",
        f"Coverage of key concepts: {', '.join(question_concepts)}",
        "Logical structure and clarity"
    ]

    return FeedbackResponse(
        score=score,
        confidence_level=confidence,
        mistakes=mistakes,
        explanation=explanation,
        how_to_improve=how_to_improve,
        correct_answer=correct_answer
    )
