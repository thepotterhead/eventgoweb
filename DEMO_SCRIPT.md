# 🎬 Hackathon Demonstration Script (3-5 Minutes)

> **Project**: Funobotz Personalized STEM Learning Chatbot
> **Target Audience**: Hackathon Evaluation Judges

---

## ⏱️ Timeline & Step-by-Step Demonstration

### 0:00 - 0:45 | Introduction & Architecture Overview
- **Action**: Open `http://127.0.0.1:8000/` in browser.
- **Script**:
  > *"Welcome judges! We built a personalized STEM learning chatbot for Funobotz paper robotics companions. Rather than a generic ChatGPT clone, our system uses Funobotz characters grounded strictly in approved knowledge to teach STEM concepts tailored to learner age, interests, starting knowledge, and product access."*

### 0:45 - 1:30 | Scenario 1 & Grounded Knowledge (Tiko Tail Motion)
- **Action**: Click **Scenario 1 Button** on the Judge Demo Panel.
- **Observe**: Customer `FZ-HACK-002` + Tiko & Motors loaded.
- **Script**:
  > *"Scenario 1 tests grounded character learning. With customer FZ-HACK-002, the chatbot activates Tiko and uses approved facts about up-and-down thread-based tail motion, explaining electrical energy conversion to thread tension."*

### 1:30 - 2:15 | Scenario 2 & Dynamic Interest Shifting (Motors -> Light)
- **Action**: Click **Scenario 2 Button**.
- **Observe**: Customer `FZ-HACK-001` starts with motors (Quacky), then learner says: *"Actually I want to learn about light with Petalo!"*
- **Script**:
  > *"Scenario 2 demonstrates mid-session adaptation. The session instantly shifts from Quacky motor learning to Petalo light discovery without losing context."*

### 2:15 - 3:00 | Scenario 3 & Access Control Layer
- **Action**: Click **Scenario 3 Button**.
- **Observe**: Customer `FZ-HACK-005` (No purchased products) attempts to ask about Quacky.
- **Script**:
  > *"Scenario 3 demonstrates product access control. Customer FZ-HACK-005 holds no valid product license. The backend safely locks product-specific hardware guides while keeping general STEM energy concepts open."*

### 3:00 - 3:45 | Scenario 4 & 5 (Ambiguity & Grounding Refusal)
- **Action**: Click **Scenario 4 Button**, then **Scenario 5 Button**.
- **Script**:
  > *"Scenario 4 handles vague queries: when a learner asks 'Why does it move?', the chatbot asks for concise clarification between Tiko and Quacky. Scenario 5 tests grounding: when asked 'What is Tiko's favorite food?', the system explicitly refuses to fabricate unapproved facts."*

### 3:45 - 4:30 | Scenario 6 & Escalation ("I already know this")
- **Action**: Click **Scenario 6 Button**.
- **Observe**: Difficulty escalates from Beginner to Intermediate with technical motor torque explanations.
- **Script**:
  > *"In Scenario 6, when a learner says 'I already know this', the personalization engine automatically escalates conceptual depth rather than repeating basic definitions."*

### 4:30 - 5:00 | Store Embeddable Widget & Conclusion
- **Action**: Click **Widget View** button to open `http://127.0.0.1:8000/demo/embed.html`.
- **Script**:
  > *"Finally, the system features `<funobotz-tutor>`, a standalone embeddable widget that integrates directly into the Funobotz Store catalog. Thank you!"*
