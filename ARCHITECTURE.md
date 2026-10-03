# 📐 System Architecture: Funobotz Personalized STEM Chatbot

## 1. System Overview

```
                                  +------------------------------------+
                                  |     CLIENT / WIDGET / STORE        |
                                  | (Web Dashboard / <funobotz-tutor>) |
                                  +-----------------+------------------+
                                                    |
                                                    v HTTP REST API
                                  +------------------------------------+
                                  |        FASTAPI BACKEND CORE        |
                                  |            (app/main.py)           |
                                  +-----------------+------------------+
                                                    |
         +------------------------+-----------------+------------------------+
         |                        |                 |                        |
         v                        v                 v                        v
+------------------+     +------------------+  +------------------+    +-------------------+
| ACCESS CONTROL   |     | KNOWLEDGE BASE   |  | PERSONALIZATION  |    | ROUTER ENGINE     |
| (data/customers) |     | (data/characters)|  | (Age, Level 0-2) |    | (Ambiguity Match) |
+--------+---------+     +--------+---------+  +--------+---------+    +---------+---------+
         |                        |                 |                        |
         +------------------------+-----------------+------------------------+
                                                    |
                                                    v
                                  +------------------------------------+
                                  |    GROUNDED AI RESPONSE ENGINE     |
                                  |       (app/ai_generator.py)        |
                                  +------------------------------------+
```

---

## 2. Component Specifications

### 2.1 Access Control Engine (`app/access_control.py`)
- Reads synthetic hackathon customer access dataset (`data/customers.json`).
- Maps Customer IDs (`FZ-HACK-001` through `005`) to owned product SKUs.
- **Backend Enforcement**: Validates every incoming chat request on the server side.
- **Graceful Limitation**: If an unowned character kit is requested (e.g., `FZ-HACK-005` requesting Quacky), product build guides are locked while general ungrounded STEM principles remain accessible.

### 2.2 Knowledge Base Engine (`app/knowledge_base.py`)
- Manages 12 character JSON files (`data/characters/*.json`).
- Character Statuses:
  - `mapped`: Full STEM facts and concept mappings (Petalo, Quacky, Tolly, Tiko).
  - `behaviour_only`: Expression & story interaction facts (Emoti, Mimo, Kuttybot).
  - `pending`: Unreleased official roster members (Kutty Omni, Wavy, Chicky, Omni, Cuby).
- **Strict Refusal Protocol**: Detects questions asking for non-approved character attributes (e.g. favorite food, favorite color, backstory) and returns a grounded notice stating official content does not contain that information.

### 2.3 Personalization Engine (`app/personalization.py`)
- Adaptations:
  - **Age Banding**: Age 8 (playful analogies), Age 9-10 (cause and effect), Age 11-12 (technical STEM terminology).
  - **Starting Knowledge**: Beginner (Level 0), Intermediate (Level 1), Advanced (Level 2).
  - **Dynamic Escalation**: Detects phrases like *"I already know this"* or *"too easy"* and automatically increments `current_level` and conceptual depth.
  - **Mid-Session Shifting**: Dynamically updates active interest and topic without destroying conversation history.

### 2.4 Router Engine (`app/router.py`)
- Detects ambiguous questions (*"Why does it move?"*) when explicit context is missing.
- Returns `clarification_needed: True` with candidate options based on owned products.
- Routes multi-character concepts (e.g., circuits apply to Quacky, Tiko, Tolly).

### 2.5 Grounded AI Generator (`app/ai_generator.py`)
- Generates structured response payloads (`answer`, `concept`, `difficulty`, `check_question`, `options`, `correct_option`).
- Uses verified facts from approved JSON files.
