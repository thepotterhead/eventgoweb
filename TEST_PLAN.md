# 🧪 Test Plan: Funobotz Personalized STEM Chatbot

This test plan maps each hackathon evaluation scenario to automated backend unit tests (`backend/test_scenarios.py`) and manual verification steps.

---

## 📋 Hackathon Evaluation Test Matrix

| Test ID | Hackathon Requirement | Input / Setup | Expected Outcome | Verification Status |
|---|---|---|---|---|
| **TP-01** | **Scenario 1**: Grounded Learning | `FZ-HACK-002` asking about Tiko & motors. | Answers using official Tiko up-and-down thread tail facts. | ✅ PASSED (Automated & UI) |
| **TP-02** | **Scenario 2**: Mid-Session Interest Shift | `FZ-HACK-001` starts motors, switches to light. | Session shifts from Quacky to Petalo light discovery. | ✅ PASSED (Automated & UI) |
| **TP-03** | **Scenario 3**: Access Control Handling | `FZ-HACK-005` (No valid purchased kit). | Product build guide locked; general STEM open. | ✅ PASSED (Automated & UI) |
| **TP-04** | **Scenario 4**: Ambiguous Request | Question: *"Why does it move?"* | Prompts concise clarification (Tiko vs Quacky). | ✅ PASSED (Automated & UI) |
| **TP-05** | **Scenario 5**: Strict Grounding Refusal | Question: *"What is Tiko's favorite food?"* | States official content does not contain that fact. | ✅ PASSED (Automated & UI) |
| **TP-06** | **Scenario 6**: Escalation ("I already know this") | Learner states: *"I already know this."* | Increments level and deepens physics/motor explanations. | ✅ PASSED (Automated & UI) |
| **TP-07** | **Scenario 7**: 12-Character Roster Support | Judge selects Cuby or pending character. | Routes safely without breaking or inventing facts. | ✅ PASSED (Automated & UI) |
| **TP-08** | **Scenario 8**: Multi-Product Access | Customer `FZ-HACK-004` (Quacky + Tiko + Tolly). | Grants full multi-product access simultaneously. | ✅ PASSED (Automated & UI) |

---

## 🏃 Execution Commands

### 1. Automated Unit Test Execution
```bash
.\backend\venv\Scripts\python.exe backend/test_scenarios.py
```

### 2. Manual UI Verification
1. Launch backend on `http://127.0.0.1:8000/`.
2. Click scenario buttons 1 through 8 in the **Judge Demo Panel**.
3. Inspect response bubbles, badges, options, and mini challenge feedback.
