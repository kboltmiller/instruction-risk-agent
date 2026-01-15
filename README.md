# Instruction Risk Agent

**Version 0.3.0**

Instruction Risk Agent is a lightweight AI microservice that analyzes technical or procedural instructions and flags potential comprehension, safety, and execution risks—especially for non-expert users.

It is designed to be called by:
- Other AI agents
- Support systems
- Documentation pipelines
- Human-facing tools that want a "second look" at instructions before delivery

This project is an early pilot focused on clarity, risk detection, and explainability, with particular emphasis on senior-friendly design.

---

## Who This Is For

Instruction Risk Agent is intended for developers, product teams, and AI system builders who generate or deliver instructions to end users. It is especially useful in contexts where small misunderstandings can lead to outsized frustration, support burden, or user harm. 

**Key audiences:**
- Tech support platforms reducing preventable confusion
- Senior care and accessibility-focused products
- Documentation teams needing automated quality checks
- AI agents that generate instructions for end users

Rather than rewriting instructions, the agent provides a structured second look—highlighting where clarity, reassurance, or safeguards may be missing.

---

## What This Agent Does

Given a block of instructions (e.g., "reset your Wi-Fi password"), the agent:

### Identifies Risk Factors
- **Cognitive overload** - Too many steps at once
- **Missing prerequisites** - Assumed prior knowledge
- **Ambiguous steps** - Vague timing or unclear actions
- **UI navigation assumptions** - Device-specific menus
- **Destructive actions** - Potential for irreversible harm
- **Technical jargon** - Terms unfamiliar to non-experts
- **Conditional logic** - Complex if/then branching
- **Visual dependencies** - Reliance on icons or colors
- **Timed physical actions** - "Press and hold for X seconds"
- **Critical domains** - Health, financial, or sensitive contexts
- **Device assumptions** - Platform-specific interactions
- **Alarming language** - Security warnings without context

### Returns Structured Analysis
- **Risk level** (low / medium / high) with plain-language explanation
- **Confidence score** indicating certainty of assessment
- **Identified risks** with specific step-level detail
- **Missing safeguards** (e.g., lack of confirmation or recovery paths)
- **Mitigation considerations** suggesting where clarification may help

The goal is not to replace documentation or human judgment, but to surface hidden failure modes before harm, confusion, or support escalation occurs.

---

## Why This Exists

AI systems and humans often assume instructions are "clear enough."

In reality:
- Users vary widely in technical literacy
- Interfaces change faster than instructions
- Small misunderstandings can cause outsized frustration or harm
- Seniors and non-technical users face unique comprehension challenges

This agent focuses on the instruction itself, not the user—making it broadly applicable across populations, tools, and domains.

---

## API Overview

### Endpoints

#### `POST /evaluate`
Analyze instructions for potential risks.

**Request Body:**
```json
{
  "instructions": "Go to your GFiber account page and reset your Wi-Fi password."
}
```

**Example Response:**
```json
{
  "risk_level": "high",
  "confidence": 0.85,
  "risk_level_explanation": "Instructions have significant potential to cause user confusion, anxiety, or harmful outcomes.",
  "identified_risks": [
    {
      "step": "account assumption",
      "risk": "Assumes the user knows what an account is and which credentials to use."
    },
    {
      "step": "destructive language",
      "risk": "Language suggests irreversible changes and may cause fear or hesitation."
    }
  ],
  "missing_safeguards": [
    "No success or failure confirmation described"
  ],
  "mitigation_considerations": [
    "Consider clarifying what account is being referenced and what credentials are needed.",
    "Consider reassuring users about what will and will not be affected by this action.",
    "Consider explaining how users will know whether the action succeeded or failed."
  ]
}
```

#### `GET /risk-levels`
Get documentation about risk level meanings.

**Response:**
```json
[
  {
    "level": "low",
    "description": "Instructions are relatively clear with minor comprehension risks.",
    "recommendation": "Generally safe to use, though minor improvements could help clarity."
  },
  {
    "level": "medium",
    "description": "Instructions contain elements that may confuse or overwhelm some users.",
    "recommendation": "Review and consider adding clarification, reassurance, or simplified steps."
  },
  {
    "level": "high",
    "description": "Instructions have significant potential to cause user confusion, anxiety, or harmful outcomes.",
    "recommendation": "Strongly recommend revision before sharing with end users, especially non-technical populations."
  }
]
```

#### `GET /health`
Health check endpoint.

---

## Current Status

✅ FastAPI service live (pilot)  
✅ 15+ heuristic-based risk detection patterns  
✅ Risk level explanations included in responses  
✅ Senior-friendly design focus  
✅ Mitigation considerations surfaced (non-prescriptive)  
🔜 x402 payment gating  
🔜 Domain-specific risk profiles  
🔜 Audio / read-aloud support for accessibility  

This is an experimental project and will evolve based on real-world testing.

---

## Intended Use Cases

- AI agents validating instructions before sharing with users
- Tech support platforms reducing preventable confusion
- Senior care and assisted living technology
- Accessibility-focused tooling
- Documentation review pipelines
- Low-literacy or non-technical product flows
- Health and medication reminder systems
- Financial services customer support

---

## Risk Detection Capabilities (v0.3.0)

The agent currently detects:

### Comprehension Risks
- Technical jargon without explanation
- Conditional logic (if/then statements)
- Cognitive overload from too many steps
- Vague timing or duration references
- Visual dependencies (icons, colors, blinking lights)

### Safety Risks
- Destructive language (delete, erase, reset)
- Critical domain contexts (health, financial)
- Alarming security warnings without context
- Missing recovery or undo paths

### Execution Risks
- Account or credential assumptions
- Settings navigation complexity
- Device or platform-specific interactions
- Timed physical actions
- Text entry challenges
- Missing success/failure confirmation

---

## Explicit Non-Goals

This agent does **not**:
- Provide medical, legal, or emergency advice
- Replace professional judgment
- Guarantee safety or correctness of instructions
- Rewrite instructions or enforce specific wording
- Interact directly with user accounts or devices
- Make decisions about whether to use instructions

---

## Disclaimer

This service provides **informational analysis only**.

It does not execute instructions, verify factual accuracy, or assume responsibility for outcomes resulting from instruction use. Use of this service does not create a professional, fiduciary, or advisory relationship.

Users should apply human judgment and domain expertise when evaluating and acting on the agent's recommendations.

---

## Tech Stack

- **Python** - Core language
- **FastAPI** - Web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

Designed to be:
- Lightweight and fast
- Composable with other systems
- Easy to call from AI agents or pipelines
- Deployable anywhere Python runs

---

## Future Plans

### Near-term
- x402 micro-payment support for sustainable operation
- Expanded heuristics based on real-world testing
- Confidence and uncertainty signaling improvements

### Medium-term
- Domain-specific risk profiles (health, finance, IoT)
- Instruction comparison and regression detection
- Multi-language support

### Long-term
- Audio-first output modes for accessibility
- Integration with popular documentation platforms
- Machine learning-enhanced risk detection

---

## Getting Started

### Try It Live

**API Endpoint:** `https://instruction-risk-agent.onrender.com`

**Interactive Documentation:** `https://instruction-risk-agent.onrender.com/docs`

Test the API directly in your browser using the interactive Swagger UI.

### Example Usage

```bash
curl -X POST https://instruction-risk-agent.onrender.com/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Open the app, tap the plus sign, enter your medication name, select the time, and enable notifications."
  }'
```

---

## Contributing

This is currently a solo learning project, but feedback and suggestions are welcome! 

If you're using this API and encounter instructions that are incorrectly classified, please share examples—they help improve the heuristics.

---

## License

MIT License

---

## Version History

### v0.3.0 (Current)
- Added 8 new heuristic detection patterns
- Enhanced risk scoring with weighted severity
- Added risk level explanations to API responses
- New `/risk-levels` documentation endpoint
- Improved detection for senior-friendly design

### v0.2.0
- Added cognitive load detection
- Enhanced API documentation
- Improved mitigation considerations

### v0.1.0
- Initial release
- Basic heuristic framework
- FastAPI implementation
- Core risk detection capabilities

---

**Live API:** [instruction-risk-agent.onrender.com](https://instruction-risk-agent.onrender.com)  
**Documentation:** [instruction-risk-agent.onrender.com/docs](https://instruction-risk-agent.onrender.com/docs)  
**GitHub:** [github.com/kboltmiller/instruction-risk-agent](https://github.com/kboltmiller/instruction-risk-agent)
