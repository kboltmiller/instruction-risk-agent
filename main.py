# Instruction Comprehension Risk Agent
# Python skeleton (FastAPI when available, pure-Python fallback)

"""
NOTE ABOUT ENVIRONMENTS
----------------------
Some sandboxed or restricted Python environments do NOT include SSL support.
FastAPI (via Starlette → AnyIO) imports the standard `ssl` module at import time.

If `ssl` is unavailable, importing FastAPI will raise:
    ModuleNotFoundError: No module named 'ssl'

To make this file runnable everywhere (including learning sandboxes), we:
- Gracefully fall back to a non-API mode if FastAPI cannot be imported
- Keep all core logic testable without FastAPI

In real deployments (Render, local Python, Docker), SSL *will* be available
and the FastAPI app will load normally.
"""

from typing import List, Optional

# -----------------------------
# Core Data Models (framework-agnostic)
# -----------------------------

class IdentifiedRisk:
    def __init__(self, step: Optional[str], risk: str):
        self.step = step
        self.risk = risk

    def dict(self):
        return {"step": self.step, "risk": self.risk}


class EvaluationResult:
    def __init__(self, risk_level: str, confidence: float,
                 identified_risks: List[IdentifiedRisk],
                 missing_safeguards: List[str]):
        self.risk_level = risk_level
        self.confidence = confidence
        self.identified_risks = identified_risks
        self.missing_safeguards = missing_safeguards


# -----------------------------
# Core Evaluation Logic (v1)
# -----------------------------

def evaluate_instructions(text: str) -> EvaluationResult:
    """
    Heuristic-based evaluator for instruction comprehension risk.
    Framework-independent and fully testable.
    """

    risks: List[IdentifiedRisk] = []
    safeguards: List[str] = []

    lowered = text.lower()

    if any(term in lowered for term in ["account", "sign in", "log in"]):
        risks.append(
            IdentifiedRisk(
                step="account assumption",
                risk="Assumes the user knows what an account is and which credentials to use."
            )
        )

    if "settings" in lowered:
        risks.append(
            IdentifiedRisk(
                step="settings navigation",
                risk="Settings menus vary by device and may be difficult to navigate."
            )
        )

    if any(term in lowered for term in ["reset", "factory", "delete", "erase"]):
        risks.append(
            IdentifiedRisk(
                step="destructive language",
                risk="Language suggests irreversible changes and may cause fear or hesitation."
            )
        )

    if "password" in lowered:
        risks.append(
            IdentifiedRisk(
                step="text entry",
                risk="Password entry is error-prone, especially with remotes or on-screen keyboards."
            )
        )

    if "select" in lowered and not any(t in lowered for t in ["back", "cancel", "undo"]):
        safeguards.append("No recovery path provided for mistaken selections")

    if not any(t in lowered for t in ["success", "connected", "failed", "error"]):
        safeguards.append("No success or failure confirmation described")

    if len(risks) >= 3:
        risk_level = "high"
        confidence = 0.82
    elif len(risks) == 2:
        risk_level = "medium"
        confidence = 0.75
    else:
        risk_level = "low"
        confidence = 0.65

    return EvaluationResult(
        risk_level=risk_level,
        confidence=confidence,
        identified_risks=risks,
        missing_safeguards=safeguards,
    )


# -----------------------------
# FastAPI Layer (optional)
# -----------------------------

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field

    FASTAPI_AVAILABLE = True
except ModuleNotFoundError:
    FASTAPI_AVAILABLE = False


if FASTAPI_AVAILABLE:

    app = FastAPI(
        title="Instruction Comprehension Risk Agent",
        description="Evaluates written instructions for potential comprehension risks.",
        version="0.1.0",
    )

    class InstructionRequest(BaseModel):
        instructions: str = Field(..., description="Instructions to evaluate")

    class IdentifiedRiskModel(BaseModel):
        step: Optional[str]
        risk: str

    class EvaluationResponse(BaseModel):
        risk_level: str
        confidence: float
        identified_risks: List[IdentifiedRiskModel]
        missing_safeguards: List[str]

    @app.post("/evaluate", response_model=EvaluationResponse)
    async def evaluate(request: InstructionRequest):
        if not request.instructions.strip():
            raise HTTPException(status_code=400, detail="Instructions cannot be empty")

        result = evaluate_instructions(request.instructions)

        return EvaluationResponse(
            risk_level=result.risk_level,
            confidence=result.confidence,
            identified_risks=[IdentifiedRiskModel(**r.dict()) for r in result.identified_risks],
            missing_safeguards=result.missing_safeguards,
        )

    @app.get("/health")
    async def health():
        return {"status": "ok"}


# -----------------------------
# Basic Tests (always runnable)
# -----------------------------

if __name__ == "__main__":
    # Simple sanity tests without FastAPI

    text = "Go to settings and reset your Wi-Fi password."
    result = evaluate_instructions(text)

    assert result.risk_level in {"low", "medium", "high"}
    assert len(result.identified_risks) >= 2
    assert isinstance(result.missing_safeguards, list)

    print("Local evaluation test passed.")
    print("Risk level:", result.risk_level)
    for r in result.identified_risks:
        print("-", r.step, ":", r.risk)
