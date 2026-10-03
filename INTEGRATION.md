# 🔌 Integration Guide: Funobotz Store & Learning Ecosystem

This document explains how the **Funobotz STEM Companion Chatbot** is embedded into the Funobotz Store or external learning platforms.

---

## 1. Embeddable Widget Overview

The frontend deliverable includes `<funobotz-tutor>`, a standalone, framework-agnostic Web Component bundled in `widget.js`.

### 1.1 Web Component Embed Snippet
Add this HTML snippet before the closing `</body>` tag on any page of `store.funobotz.com`:

```html
<!-- Load Funobotz Tutor Widget Script -->
<script src="http://localhost:8000/widget.js"></script>

<!-- Custom Element Container -->
<funobotz-tutor 
  data-api-url="http://127.0.0.1:8000/api"
  data-customer-id="FZ-HACK-004"
  data-learner-age="10"
  data-character="tiko"
  data-theme="dark">
</funobotz-tutor>
```

---

## 2. Configurable Attributes

| Attribute | Type | Default | Description |
|---|---|---|---|
| `data-api-url` | `string` | `http://127.0.0.1:8000/api` | Base URL of the FastAPI backend service. |
| `data-customer-id` | `string` | `FZ-HACK-001` | Logged-in customer ID for product access checks. |
| `data-learner-age` | `number` | `10` | Learner age for explanation adaptation. |
| `data-character` | `string` | `quacky` | Default companion character ID. |
| `data-theme` | `string` | `dark` | Visual theme mode (`dark` or `light`). |

---

## 3. REST API Interface Specification

### `POST /api/session`
Initializes a new learner session.
- **Request Body**:
```json
{
  "learner_id": "L-WIDGET",
  "name": "Store Visitor",
  "age": 10,
  "customer_id": "FZ-HACK-004",
  "active_character": "tiko"
}
```

### `POST /api/chat`
Main conversational endpoint enforcing access control, grounding, and personalization.
- **Request Body**:
```json
{
  "session_id": "sess_123456",
  "message": "How does Tiko's tail motor work?",
  "customer_id": "FZ-HACK-004",
  "requested_character": "tiko"
}
```
- **Response Payload**:
```json
{
  "session_id": "sess_123456",
  "answer": "Tiko is a scorpio bot whose motor creates up-and-down thread-based tail movement...",
  "concept": "motors",
  "difficulty": "Intermediate",
  "check_question": "What energy transformation occurs in Tiko's motor circuit?",
  "options": ["Electrical energy to mechanical motion", "Heat to sound", "Light to motion"],
  "correct_option": 0,
  "next_step": "Answer the check question!",
  "active_character": "tiko",
  "active_topic": "motors",
  "access_granted": true
}
```
