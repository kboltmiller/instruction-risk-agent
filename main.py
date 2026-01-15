# Instruction Risk Agent
# v0.3.0 - Enhanced heuristics for senior-friendly instruction analysis

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
# Risk Level Definitions
# -----------------------------

RISK_LEVELS = {
    "low": {
        "description": "Instructions are relatively clear with minor comprehension risks.",
        "recommendation": "Generally safe to use, though minor improvements could help clarity."
    },
    "medium": {
        "description": "Instructions contain elements that may confuse or overwhelm some users.",
        "recommendation": "Review and consider adding clarification, reassurance, or simplified steps."
    },
    "high": {
        "description": "Instructions have significant potential to cause user confusion, anxiety, or harmful outcomes.",
        "recommendation": "Strongly recommend revision before sharing with end users, especially non-technical populations."
    }
}

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
                 missing_safeguards: List[str],
                 mitigation_considerations: List[str],
                 risk_level_explanation: str):
        self.risk_level = risk_level
        self.confidence = confidence
        self.identified_risks = identified_risks
        self.missing_safeguards = missing_safeguards
        self.mitigation_considerations = mitigation_considerations
        self.risk_level_explanation = risk_level_explanation


# -----------------------------
# Core Evaluation Logic (v0.3.0)
# -----------------------------

def evaluate_instructions(text: str) -> EvaluationResult:
    """
    Heuristic-based evaluator for instruction comprehension risk.
    Framework-independent and fully testable.
    
    v0.3.0: Enhanced heuristics targeting senior-friendly design
    """

    risks: List[IdentifiedRisk] = []
    safeguards: List[str] = []
    mitigations: List[str] = []
    risk_score = 0  # Track severity for better risk level calculation

    lowered = text.lower()

    # ===== EXISTING HEURISTICS (v0.1.0 - v0.2.0) =====

    # Account/credential complexity
    if any(term in lowered for term in ["account", "sign in", "log in"]):
        risks.append(
            IdentifiedRisk(
                step="account assumption",
                risk="Assumes the user knows what an account is and which credentials to use."
            )
        )
        mitigations.append(
            "Consider clarifying what account is being referenced and what credentials are needed."
        )
        risk_score += 1

    # Navigation complexity
    if "settings" in lowered:
        risks.append(
            IdentifiedRisk(
                step="settings navigation",
                risk="Settings menus vary by device and may be difficult to navigate."
            )
        )
        mitigations.append(
            "Consider acknowledging that menu names or locations may vary by device."
        )
        risk_score += 1

    # Destructive action risk (enhanced in v0.3.0)
    destructive_terms = ["reset", "factory", "delete", "erase", "remove", "lose", "gone", "permanently"]
    if any(term in lowered for term in destructive_terms):
        risks.append(
            IdentifiedRisk(
                step="destructive language",
                risk="Language suggests irreversible changes and may cause fear or hesitation."
            )
        )
        mitigations.append(
            "Consider reassuring users about what will and will not be affected by this action."
        )
        # Higher weight for destructive actions
        risk_score += 2

    # Text entry challenges
    if "password" in lowered:
        risks.append(
            IdentifiedRisk(
                step="text entry",
                risk="Password entry is error-prone, especially with remotes or on-screen keyboards."
            )
        )
        mitigations.append(
            "Consider noting that text entry may be challenging and errors are common."
        )
        risk_score += 1

    # Missing recovery paths
    if "select" in lowered and not any(t in lowered for t in ["back", "cancel", "undo"]):
        safeguards.append("No recovery path provided for mistaken selections")
        mitigations.append(
            "Consider indicating whether users can reverse or cancel this action if needed."
        )
        risk_score += 1

    # Missing confirmation feedback
    if not any(t in lowered for t in ["success", "connected", "failed", "error", "complete", "done"]):
        safeguards.append("No success or failure confirmation described")
        mitigations.append(
            "Consider explaining how users will know whether the action succeeded or failed."
        )
        risk_score += 1

    # Cognitive overload detection (v0.2.0)
    step_count = text.count('.') + text.count('\n') + text.count(',') // 2
    if step_count > 5:
        risks.append(
            IdentifiedRisk(
                step="cognitive load",
                risk="Multiple steps may overwhelm users, especially those with limited technical experience."
            )
        )
        mitigations.append(
            "Consider breaking instructions into smaller, numbered steps or providing visual aids."
        )
        risk_score += 2

    # ===== NEW HEURISTICS (v0.3.0) =====

    # 1. Technical Jargon Detection
    jargon_terms = ["firmware", "admin", "router", "bandwidth", "ssid", "modem", "cache", 
                    "browser", "driver", "protocol", "ip address", "dns", "gateway"]
    found_jargon = [term for term in jargon_terms if term in lowered]
    if found_jargon:
        risks.append(
            IdentifiedRisk(
                step="technical jargon",
                risk=f"Contains technical terms that may not be familiar to all users."
            )
        )
        mitigations.append(
            "Consider explaining technical terms in plain language or providing a glossary."
        )
        risk_score += 2

    # 2. Conditional Logic Detection
    conditional_phrases = ["if you", "if the", "otherwise", "in case", "depending on", 
                          "when you see", "should you"]
    if any(phrase in lowered for phrase in conditional_phrases):
        risks.append(
            IdentifiedRisk(
                step="conditional logic",
                risk="Contains if/then logic that users may miss or misinterpret."
            )
        )
        mitigations.append(
            "Consider simplifying branching paths or highlighting the condition clearly."
        )
        risk_score += 2

    # 3. Vague Timing/Duration
    vague_time = ["a few", "several", "a moment", "shortly", "soon", "a while", 
                  "briefly", "quickly"]
    if any(phrase in lowered for phrase in vague_time):
        risks.append(
            IdentifiedRisk(
                step="vague timing",
                risk="Uses ambiguous time references that may confuse users about how long to wait."
            )
        )
        mitigations.append(
            "Consider providing specific timeframes (e.g., '2-3 minutes' instead of 'a few minutes')."
        )
        risk_score += 1

    # 4. Visual Dependency
    visual_terms = ["icon", "button", "see the", "look for", "appears", "blinks", 
                   "led", "light", "color", "blue", "green", "red"]
    if any(term in lowered for term in visual_terms):
        risks.append(
            IdentifiedRisk(
                step="visual dependency",
                risk="Relies on visual cues that may not be visible to all users or may change over time."
            )
        )
        mitigations.append(
            "Consider providing text labels or alternative ways to identify elements."
        )
        risk_score += 1

    # 5. Timed Physical Actions
    if any(phrase in lowered for phrase in ["press and hold", "hold for", "hold until", 
                                            "for # seconds", "wait # seconds"]):
        risks.append(
            IdentifiedRisk(
                step="timed action",
                risk="Requires precise timing or sustained physical action that may be challenging."
            )
        )
        mitigations.append(
            "Consider noting that the timing doesn't need to be exact or providing alternative methods."
        )
        risk_score += 1

    # 6. Critical Domain Detection
    critical_terms = ["medication", "medicine", "health", "medical", "doctor", 
                     "financial", "bank", "payment", "money", "credit card"]
    if any(term in lowered for term in critical_terms):
        risks.append(
            IdentifiedRisk(
                step="critical domain",
                risk="Instructions involve sensitive domains (health, finance) where errors have serious consequences."
            )
        )
        mitigations.append(
            "Consider adding extra confirmation steps and clearer error prevention for this critical task."
        )
        risk_score += 3

    # 7. Platform/Device Assumptions
    platform_specific = {
        "swipe": "touchscreen",
        "tap": "touchscreen", 
        "click": "mouse/trackpad",
        "right-click": "mouse",
        "scroll": "specific input method"
    }
    assumed_platforms = [action for action, device in platform_specific.items() if action in lowered]
    if assumed_platforms:
        risks.append(
            IdentifiedRisk(
                step="device assumption",
                risk=f"Assumes specific input methods that may not match the user's device."
            )
        )
        mitigations.append(
            "Consider acknowledging that interaction methods may vary by device type."
        )
        risk_score += 1

    # 8. Security Warning Language
    if any(term in lowered for term in ["warning", "alert", "security", "unsafe", "risk"]):
        risks.append(
            IdentifiedRisk(
                step="alarming language",
                risk="Contains security or warning language that may cause anxiety without proper context."
            )
        )
        mitigations.append(
            "Consider explaining why the warning appears and reassuring users about safe next steps."
        )
        risk_score += 2

    # ===== RISK LEVEL CALCULATION =====
    # Enhanced scoring system based on severity
    if risk_score >= 6 or len(risks) >= 4:
        risk_level = "high"
        confidence = 0.85
    elif risk_score >= 3 or len(risks) >= 2:
        risk_level = "medium"
        confidence = 0.78
    else:
        risk_level = "low"
        confidence = 0.70

    # Get explanation for the assigned risk level
    risk_level_explanation = RISK_LEVELS[risk_level]["description"]

    return EvaluationResult(
        risk_level=risk_level,
        confidence=confidence,
        identified_risks=risks,
        missing_safeguards=safeguards,
        mitigation_considerations=mitigations,
        risk_level_explanation=risk_level_explanation
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
        title="Instruction Risk Agent",
        description="Analyzes technical or procedural instructions and flags potential comprehension, safety, and execution risks.",
        version="0.3.0",
    )

    class InstructionRequest(BaseModel):
        instructions: str = Field(..., description="Instructions to evaluate for potential risks")

    class IdentifiedRiskModel(BaseModel):
        step: Optional[str]
        risk: str

    class EvaluationResponse(BaseModel):
        risk_level: str
        confidence: float
        identified_risks: List[IdentifiedRiskModel]
        missing_safeguards: List[str]
        mitigation_considerations: List[str]
        risk_level_explanation: str

    class RiskLevelInfo(BaseModel):
        level: str
        description: str
        recommendation: str

    @app.post("/evaluate", response_model=EvaluationResponse)
    async def evaluate(request: InstructionRequest):
        """
        Evaluate instructions for comprehension, safety, and execution risks.
        
        Returns structured analysis including:
        - Risk level (low/medium/high) with explanation
        - Confidence score
        - Identified risk factors
        - Missing safeguards
        - Mitigation considerations
        """
        if not request.instructions.strip():
            raise HTTPException(status_code=400, detail="Instructions cannot be empty")

        result = evaluate_instructions(request.instructions)

        return EvaluationResponse(
            risk_level=result.risk_level,
            confidence=result.confidence,
            identified_risks=[IdentifiedRiskModel(**r.dict()) for r in result.identified_risks],
            missing_safeguards=result.missing_safeguards,
            mitigation_considerations=result.mitigation_considerations,
            risk_level_explanation=result.risk_level_explanation
        )

    @app.get("/risk-levels", response_model=List[RiskLevelInfo])
    async def get_risk_levels():
        """
        Get documentation about risk level meanings.
        
        Returns definitions and recommendations for low, medium, and high risk levels.
        """
        return [
            RiskLevelInfo(
                level=level,
                description=info["description"],
                recommendation=info["recommendation"]
            )
            for level, info in RISK_LEVELS.items()
        ]

    @app.get("/health")
    async def health():
        """Health check endpoint"""
        return {"status": "ok", "version": "0.3.0"}


# -----------------------------
# Basic Tests (always runnable)
# -----------------------------

if __name__ == "__main__":
    # Test case from original development
    text = "Go to settings and reset your Wi-Fi password."
    result = evaluate_instructions(text)

    assert result.risk_level in {"low", "medium", "high"}
    assert len(result.identified_risks) >= 2
    assert isinstance(result.missing_safeguards, list)
    assert isinstance(result.mitigation_considerations, list)
    assert result.risk_level_explanation is not None

    print("Local evaluation test passed.")
    print("Risk level:", result.risk_level)
    print("Explanation:", result.risk_level_explanation)

    for r in result.identified_risks:
        print("-", r.step, ":", r.risk)

    print("\nMitigation considerations:")
    for m in result.mitigation_considerations:
        print("-", m)
