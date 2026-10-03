from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LearnerProfile(BaseModel):
    learner_id: str = "L-DEFAULT"
    name: str = "Learner"
    age: int = 10
    interest: str = "motors"
    starting_knowledge: str = "Beginner"  # Beginner, Intermediate, Advanced
    current_level: int = 0               # 0: Beginner, 1: Intermediate, 2: Advanced
    current_topic: str = "motors"
    active_character: str = "quacky"
    customer_id: str = "FZ-HACK-001"

class ChatRequest(BaseModel):
    session_id: str
    message: str
    customer_id: str = "FZ-HACK-001"
    learner_profile: Optional[LearnerProfile] = None
    requested_character: Optional[str] = None
    api_key: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    concept: str
    difficulty: str  # Beginner, Intermediate, Advanced
    check_question: Optional[str] = None
    options: Optional[List[str]] = None
    correct_option: Optional[int] = None
    next_step: Optional[str] = None
    active_character: str
    active_topic: str
    access_granted: bool = True
    access_notice: Optional[str] = None
    escalation_triggered: bool = False
    clarification_needed: bool = False
    clarification_options: Optional[List[str]] = None
    unsupported_fact_notice: Optional[str] = None

class LearningCheckRequest(BaseModel):
    session_id: str
    question: str
    selected_option: int
    correct_option: int

class LearningCheckResponse(BaseModel):
    is_correct: bool
    feedback: str
    score_delta: int
    new_level: int
    next_question: Optional[str] = None
    next_options: Optional[List[str]] = None
    next_correct_option: Optional[int] = None

class CustomerInfoResponse(BaseModel):
    customer_id: str
    customer_name: str
    purchased_products: List[str]
    accessible_characters: List[str]

class ScenarioPresetRequest(BaseModel):
    scenario_id: int  # 1 to 8
