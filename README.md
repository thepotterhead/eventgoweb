# 🤖 Funobotz Personalized STEM Learning Chatbot

> **Official Hackathon Submission** | Progressive-Disclosure Hackathon (PBM 2)

An intelligent, grounded, deployable STEM learning chatbot that transforms Funobotz paper robotics characters (Tiko, Tolly, Petalo, Quacky, Emoti, Mimo, Kuttybot, Kutty Omni, Wavy, Chicky, Omni, Cuby) into personalized educational companions.

---

## 🌟 Key Features

1. **Strict Knowledge Grounding**:
   - Built on official Funobotz character knowledge (Resource Packs 1, 2, and 3).
   - Never fabricates character facts (e.g., favorite food, backstory, or unreleased character specs).

2. **Multi-Dimensional Personalization**:
   - **Learner Age**: Adapts vocabulary, tone, and sentence complexity (Age 8 vs 9-10 vs 11-12).
   - **Starting Knowledge**: Beginner (Level 0), Intermediate (Level 1), Advanced (Level 2).
   - **Escalation Intent**: Dynamically increases difficulty when a learner says *"I already know this"*.
   - **Mid-Session Interest Shifting**: Shifts seamlessly from motors to light without resetting session context.

3. **Backend Access-Control Layer**:
   - Enforces product ownership permissions for synthetic accounts (`FZ-HACK-001` through `005`).
   - Restricts product-specific build help for unowned kits while keeping general STEM principles open.

4. **Contextual Ambiguity Router**:
   - Detects vague questions like *"Why does it move?"* and prompts concise character choices (e.g. Tiko vs Quacky).

5. **Official 12-Character Roster Support**:
   - Complete schema support for all 12 roster members (`mapped`, `behaviour_only`, and `pending`).

6. **Embeddable Chatbot Widget**:
   - Web Component (`<funobotz-tutor>`) and `/demo/embed.html` integration demo page.

7. **Judge Demo Panel**:
   - Built-in 8-scenario evaluation toolbar for instant compliance verification.

---

## 🚀 Quick Start (Running Locally)

### Step 1: Clone / Navigate to Directory
```bash
cd C:\Users\User\.gemini\antigravity\scratch\funobotz-chatbot
```

### Step 2: Start the Full-Stack Server
```bash
# Windows PowerShell
.\backend\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Step 3: Open in Browser
- **Main Web Application & Judge Dashboard**: `http://127.0.0.1:8000/`
- **Embeddable Store Widget Demo**: `http://127.0.0.1:8000/demo/embed.html`
- **REST API Documentation**: `http://127.0.0.1:8000/docs`

---

## 🧪 Running Automated Scenario Tests

Run all 8 hackathon evaluation scenario unit tests:

```bash
.\backend\venv\Scripts\python.exe backend/test_scenarios.py
```

Expected output:
```
Ran 8 tests in 0.108s
OK
```

---

## 📁 Repository Structure

```
funobotz-chatbot/
├── data/
│   ├── customers.json          # Synthetic customer access dataset (FZ-HACK-001 to 005)
│   ├── products.json           # Funobotz kit products catalog
│   ├── concepts.json           # STEM concept mappings across characters
│   └── characters/             # 12 official character knowledge files
├── backend/
│   ├── requirements.txt        # Python backend dependencies
│   ├── test_scenarios.py       # Automated test suite for 8 scenarios
│   └── app/
│       ├── main.py             # FastAPI entrypoint & static mounts
│       ├── api.py              # REST API endpoints
│       ├── models.py           # Pydantic data models
│       ├── access_control.py   # Product access enforcement engine
│       ├── knowledge_base.py   # Grounded facts & refusal engine
│       ├── personalization.py  # Age & knowledge depth adaptation
│       ├── router.py           # Character matcher & ambiguity detector
│       ├── ai_generator.py     # Grounded response generator
│       └── static/index.html   # Main web application UI
├── frontend/
│   └── public/
│       ├── widget.js           # Embeddable Web Component script
│       └── demo/embed.html     # Store integration demo page
├── README.md
├── ARCHITECTURE.md
├── DEMO_SCRIPT.md
├── INTEGRATION.md
├── TEST_PLAN.md
└── FINAL_COMPLIANCE_REPORT.md
```
