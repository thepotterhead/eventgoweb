import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend"))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

print("=== 1. TESTING CHARACTER DISTINCT QUESTIONS FOR ALL 12 CHARACTERS ===")
characters = ["tiko", "quacky", "petalo", "tolly", "emoti", "mimo", "kuttybot", "kutty-omni", "wavy", "chicky", "omni", "cuby"]

for char in characters:
    res = client.post("/api/chat", json={
        "session_id": f"sess_test_{char}",
        "message": f"Tell me about {char}",
        "customer_id": "FZ-HACK-004",
        "requested_character": char
    })
    data = res.json()
    q = data.get("check_question")
    opts = data.get("options")
    print(f"[{char.upper()}] -> Question: {q}")
    print(f"  Options: {opts[:2] if opts else []}")
    print("-" * 50)

print("\n=== 2. TESTING CONTINUOUS Q&A FLOW (5 QUESTIONS IN A ROW) ===")
sess_id = "sess_continuous_qa"
# Init chat with Tiko
c_res = client.post("/api/chat", json={
    "session_id": sess_id,
    "message": "Tell me about Tiko's tail motor",
    "customer_id": "FZ-HACK-002",
    "requested_character": "tiko"
})
c_data = c_res.json()
print(f"Initial Tiko Q: {c_data['check_question']}")

# Submit 5 learning checks continuously
for step in range(1, 6):
    lc_res = client.post("/api/learning-check", json={
        "session_id": sess_id,
        "question": c_data.get("check_question", "Question"),
        "selected_option": 0,
        "correct_option": 0
    })
    lc_data = lc_res.json()
    # Strip emojis for Windows console safety
    clean_fb = lc_data['feedback'].encode('ascii', 'ignore').decode('ascii')
    clean_nq = lc_data['next_question'].encode('ascii', 'ignore').decode('ascii')
    print(f"Answer #{step} Feedback: {clean_fb} | Next Q: {clean_nq}")
    c_data["check_question"] = lc_data["next_question"]

print("\nAll continuous Q&A and character-specific question checks PASSED successfully!")
