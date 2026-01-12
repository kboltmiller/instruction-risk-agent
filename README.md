Instruction Risk Agent
Instruction Risk Agent is a lightweight AI microservice that analyzes technical or procedural instructions and flags potential comprehension, safety, and execution risks—especially for non-expert users.
It is designed to be called by:
•	Other AI agents
•	Support systems
•	Documentation pipelines
•	Human-facing tools that want a “second look” at instructions before delivery
This project is an early pilot focused on clarity, risk detection, and explainability.
________________________________________
What This Agent Does
Given a block of instructions (e.g. “reset your Wi-Fi password”), the agent:
•	Identifies risk factors such as:
o	Cognitive overload
o	Missing prerequisites
o	Ambiguous steps
o	UI navigation assumptions
o	Potential for irreversible actions
•	Assigns a risk score (low / medium / high)
•	Returns human-readable reasoning explaining why the instruction may be risky
•	Optionally suggests risk-reduction improvements
The goal is not to replace documentation or human judgment, but to surface hidden failure modes before harm, confusion, or support escalation occurs.
________________________________________
Why This Exists
AI systems and humans often assume instructions are “clear enough.”
In reality:
•	Users vary widely in technical literacy
•	Interfaces change faster than instructions
•	Small misunderstandings can cause outsized frustration or harm
This agent focuses on the instruction itself, not the user — making it broadly applicable across populations, tools, and domains.
________________________________________
API Overview
Base URL
/analyze
Method
POST
Request Body
{
  "instruction_text": "Go to your GFiber account page and reset your Wi-Fi password."
}
Example Response
{
  "risk_level": "medium",
  "risk_score": 0.42,
  "risk_factors": [
    "Assumes the user knows what a GFiber account is",
    "No guidance provided if the user cannot sign in",
    "No warning about devices disconnecting immediately"
  ],
  "explanation": "The instruction relies on prior account access and omits recovery paths, which may confuse or block some users."
}
________________________________________
Current Status
•	✅ FastAPI service live (pilot)
•	✅ Heuristic-based risk detection
•	🔜 x402 payment gating
•	🔜 Expanded heuristics + transparency
•	🔜 Audio / read-aloud support for accessibility
This is an experimental project and will evolve.
________________________________________
Intended Use Cases
•	AI agents validating instructions before sharing with users
•	Tech support platforms reducing preventable confusion
•	Accessibility-focused tooling
•	Documentation review pipelines
•	Senior-friendly or low-literacy product flows
________________________________________
Explicit Non-Goals
This agent does not:
•	Provide medical, legal, or emergency advice
•	Replace professional judgment
•	Guarantee safety or correctness of instructions
•	Interact directly with user accounts or devices
________________________________________
Disclaimer
This service provides informational analysis only.
It does not execute instructions, verify factual accuracy, or assume responsibility for outcomes resulting from instruction use.
Use of this service does not create a professional, fiduciary, or advisory relationship.
________________________________________
Tech Stack
•	Python
•	FastAPI
•	Pydantic
•	Uvicorn
Designed to be:
•	Lightweight
•	Composable
•	Easy to call from other systems
________________________________________
Future Plans
•	x402 micro-payment support
•	Domain-specific risk profiles
•	Confidence and uncertainty signaling
•	Instruction comparison and regression detection
•	Audio-first output modes
________________________________________
License
MIT License 

