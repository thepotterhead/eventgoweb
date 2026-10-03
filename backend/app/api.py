import os
import uuid
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from .models import (
    LearnerProfile,
    ChatRequest,
    ChatResponse,
    LearningCheckRequest,
    LearningCheckResponse,
    CustomerInfoResponse,
    ScenarioPresetRequest
)
from .access_control import AccessControlEngine
from .knowledge_base import KnowledgeBaseEngine
from .personalization import PersonalizationEngine
from .router import RouterEngine
from .ai_generator import GroundedAIGenerator
from .database import save_learner, log_chat_message, log_quiz_answer

# Locate data directory relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

access_engine = AccessControlEngine(DATA_DIR)
kb_engine = KnowledgeBaseEngine(DATA_DIR)
router_engine = RouterEngine(kb_engine, access_engine)
ai_generator = GroundedAIGenerator(kb_engine, access_engine)

api_router = APIRouter(prefix="/api")

# In-memory session state store
sessions_db: Dict[str, Dict[str, Any]] = {}

@api_router.post("/session")
def create_or_get_session(profile: Optional[LearnerProfile] = None):
    session_id = f"sess_{uuid.uuid4().hex[:8]}"
    if not profile:
        profile = LearnerProfile()
    
    sessions_db[session_id] = {
        "session_id": session_id,
        "profile": profile,
        "message_history": [],
        "score": 0
    }

    try:
        save_learner(
            learner_id=profile.learner_id,
            name=profile.name,
            age=profile.age,
            customer_id=profile.customer_id,
            starting_knowledge=profile.starting_knowledge or 'Beginner',
            active_character=profile.active_character,
            total_xp=0
        )
    except Exception:
        pass
    return {
        "session_id": session_id,
        "profile": profile,
        "accessible_products": access_engine.get_accessible_products(profile.customer_id),
        "accessible_characters": access_engine.get_accessible_characters(profile.customer_id)
    }

@api_router.get("/customer/{customer_id}", response_model=CustomerInfoResponse)
def get_customer_info(customer_id: str):
    cust = access_engine.get_customer(customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail="Customer ID not found in hackathon database")
    
    acc_chars = access_engine.get_accessible_characters(customer_id)
    return CustomerInfoResponse(
        customer_id=cust["customer_id"],
        customer_name=cust["customer_name"],
        purchased_products=cust["purchased_products"],
        accessible_characters=acc_chars
    )

@api_router.get("/characters")
def list_characters():
    return kb_engine.get_all_characters()

@api_router.get("/knowledge/{character_id}")
def get_character_knowledge(character_id: str):
    char = kb_engine.get_character(character_id.lower())
    if not char:
        raise HTTPException(status_code=404, detail=f"Character '{character_id}' not found in official roster.")
    return char

@api_router.post("/learner/select-age")
def select_learner_age(age: int, customer_id: str = "FZ-HACK-001"):
    profile = PersonalizationEngine.get_profile_by_age(age, customer_id)
    return profile

@api_router.post("/learner/update")
def update_learner_profile(session_id: str, profile: LearnerProfile):
    if session_id not in sessions_db:
        sessions_db[session_id] = {
            "session_id": session_id,
            "profile": profile,
            "message_history": [],
            "score": 0
        }
    else:
        sessions_db[session_id]["profile"] = profile
        
    return {
        "session_id": session_id,
        "profile": profile,
        "accessible_products": access_engine.get_accessible_products(profile.customer_id),
        "accessible_characters": access_engine.get_accessible_characters(profile.customer_id)
    }

@api_router.post("/chat", response_model=ChatResponse)
def process_chat(req: ChatRequest):
    # Ensure session exists
    session_id = req.session_id
    if session_id not in sessions_db:
        profile = req.learner_profile or LearnerProfile(customer_id=req.customer_id)
        sessions_db[session_id] = {
            "session_id": session_id,
            "profile": profile,
            "message_history": [],
            "score": 0
        }
    
    session = sessions_db[session_id]
    profile: LearnerProfile = session["profile"]

    # Sync Customer ID if updated in request
    if req.customer_id and req.customer_id != profile.customer_id:
        profile.customer_id = req.customer_id

    # 1. Personalization Engine Adaptability
    updated_profile, escalation_triggered, interest_changed, new_topic = PersonalizationEngine.adapt_profile(profile, req.message)
    session["profile"] = updated_profile

    # 2. Check for Unsupported Fact Queries (Scenario 5)
    target_char_candidate = req.requested_character or profile.active_character
    unsupported_notice = kb_engine.check_unsupported_query(req.message, target_char_candidate)

    # 3. Router Engine
    route_result = router_engine.route_request(
        message=req.message,
        customer_id=profile.customer_id,
        current_topic=profile.current_topic,
        current_character=profile.active_character,
        requested_character=req.requested_character
    )

    active_char = route_result["character_id"]
    active_topic = route_result["concept"]
    profile.active_character = active_char
    profile.current_topic = active_topic

    # 4. Access Control Engine
    access_info = access_engine.check_access(profile.customer_id, active_char)

    # 5. Generate Grounded AI Response
    response = ai_generator.generate_response(
        session_id=session_id,
        message=req.message,
        customer_id=profile.customer_id,
        profile=profile,
        character_id=active_char,
        concept=active_topic,
        access_info=access_info,
        clarification_info=route_result,
        unsupported_notice=unsupported_notice,
        escalation_triggered=escalation_triggered,
        api_key=req.api_key
    )

    # Record message history
    session["message_history"].append({"role": "user", "content": req.message})
    session["message_history"].append({"role": "assistant", "content": response.answer})

    try:
        log_chat_message(session_id, "user", req.message, active_char)
        log_chat_message(session_id, "bot", response.answer, active_char)
    except Exception:
        pass

    return response

@api_router.post("/learning-check", response_model=LearningCheckResponse)
def submit_learning_check(req: LearningCheckRequest):
    session = sessions_db.get(req.session_id)
    is_correct = (req.selected_option == req.correct_option)
    
    score_delta = 10 if is_correct else 0
    new_level = 0
    active_char = "quacky"
    
    if session:
        session["score"] = session.get("score", 0) + score_delta
        prof: LearnerProfile = session["profile"]
        if is_correct and prof.current_level < 2:
            pass
        new_level = prof.current_level
        active_char = prof.active_character or "quacky"
        session["question_counter"] = session.get("question_counter", 0) + 1
        q_count = session["question_counter"]
    else:
        q_count = 1

    feedback = "🌟 Outstanding! You nailed the STEM concept!" if is_correct else "Good try! Keep exploring to master this STEM concept!"

    # Generate the NEXT continuous question for the active character!
    next_q, next_opts, next_correct = ai_generator._generate_check_question(active_char, new_level, q_count)

    return LearningCheckResponse(
        is_correct=is_correct,
        feedback=feedback,
        score_delta=score_delta,
        new_level=new_level,
        next_question=next_q,
        next_options=next_opts,
        next_correct_option=next_correct
    )

@api_router.post("/demo/scenario")
def trigger_demo_scenario(req: ScenarioPresetRequest):
    """
    Helper endpoint for judges to instantly configure any of the 8 required hackathon evaluation scenarios!
    """
    sid = req.scenario_id
    session_id = f"demo_sess_scenario_{sid}"

    if sid == 1:
        # Scenario 1: FZ-HACK-002 + Tiko & Motors
        prof = LearnerProfile(
            learner_id="L-02",
            name="Judge Tester",
            age=11,
            interest="motors",
            starting_knowledge="Intermediate",
            current_level=1,
            current_topic="motors",
            active_character="tiko",
            customer_id="FZ-HACK-002"
        )
        msg = "Tell me about Tiko and how its tail motor works."

    elif sid == 2:
        # Scenario 2: FZ-HACK-001 + Start motors -> Change to light
        prof = LearnerProfile(
            learner_id="L-01",
            name="Judge Tester",
            age=8,
            interest="motors",
            starting_knowledge="Beginner",
            current_level=0,
            current_topic="motors",
            active_character="quacky",
            customer_id="FZ-HACK-001"
        )
        msg = "Actually I want to learn about light with Petalo!"

    elif sid == 3:
        # Scenario 3: FZ-HACK-005 (No valid product)
        prof = LearnerProfile(
            learner_id="L-05",
            name="Judge Tester",
            age=10,
            interest="motors",
            starting_knowledge="Beginner",
            current_level=0,
            current_topic="motors",
            active_character="quacky",
            customer_id="FZ-HACK-005"
        )
        msg = "How do I build Quacky's motor circuit?"

    elif sid == 4:
        # Scenario 4: Question: 'Why does it move?' (Unclear request)
        prof = LearnerProfile(
            learner_id="L-03",
            name="Judge Tester",
            age=9,
            interest="motors",
            starting_knowledge="Beginner",
            current_level=0,
            current_topic="motors",
            active_character="quacky",
            customer_id="FZ-HACK-004"
        )
        msg = "Why does it move?"

    elif sid == 5:
        # Scenario 5: Unsupported fact request
        prof = LearnerProfile(
            learner_id="L-01",
            name="Judge Tester",
            age=8,
            interest="motors",
            starting_knowledge="Beginner",
            current_level=0,
            current_topic="motors",
            active_character="tiko",
            customer_id="FZ-HACK-002"
        )
        msg = "What is Tiko's favorite food?"

    elif sid == 6:
        # Scenario 6: Learner says 'I already know this.'
        prof = LearnerProfile(
            learner_id="L-04",
            name="Judge Tester",
            age=12,
            interest="motors",
            starting_knowledge="Beginner",
            current_level=0,
            current_topic="motors",
            active_character="tiko",
            customer_id="FZ-HACK-002"
        )
        msg = "I already know this."

    elif sid == 7:
        # Scenario 7: Judge selects official unreleased or different character (e.g., Cuby / Emoti)
        prof = LearnerProfile(
            learner_id="L-05",
            name="Judge Tester",
            age=10,
            interest="stories",
            starting_knowledge="Beginner",
            current_level=0,
            current_topic="behavior",
            active_character="cuby",
            customer_id="FZ-HACK-004"
        )
        msg = "Tell me about Cuby!"

    elif sid == 8:
        # Scenario 8: FZ-HACK-004 (Multi-product customer: Quacky + Tiko + Tolly)
        prof = LearnerProfile(
            learner_id="L-04",
            name="Judge Tester",
            age=12,
            interest="electronics",
            starting_knowledge="Intermediate",
            current_level=1,
            current_topic="circuits",
            active_character="tolly",
            customer_id="FZ-HACK-004"
        )
        msg = "How do Tolly's timer circuits compare with Quacky's BO motor circuit?"

    else:
        prof = LearnerProfile()
        msg = "Hello!"

    # Save session
    sessions_db[session_id] = {
        "session_id": session_id,
        "profile": prof,
        "message_history": [],
        "score": 0
    }

    # Execute chat call for scenario
    chat_req = ChatRequest(
        session_id=session_id,
        message=msg,
        customer_id=prof.customer_id,
        learner_profile=prof,
        requested_character=None
    )
    res = process_chat(chat_req)

    return {
        "scenario_id": sid,
        "session_id": session_id,
        "profile": prof,
        "request_message": msg,
        "response": res
    }
