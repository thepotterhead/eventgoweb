import re
from typing import Dict, Any, Tuple, Optional
from .models import LearnerProfile

class PersonalizationEngine:
    @staticmethod
    def get_profile_by_age(age: int, customer_id: str = "FZ-HACK-001") -> LearnerProfile:
        """
        Maps learner age to official synthetic learner profiles (Resource Pack 2):
        - L-01 (Age 8): Interested in light and colorful builds; first-time STEM learner.
        - L-03 (Age 9): Enjoys stories and characters; needs simple explanations.
        - L-05 (Age 10): No stated STEM preference; explores via open-ended questions.
        - L-02 (Age 11): Interested in movement and machines; understands basic battery connections.
        - L-04 (Age 12+): Interested in electronics; understands simple circuits, wants deeper explanation.
        """
        if age <= 8:
            return LearnerProfile(
                learner_id="L-01",
                name="Spark Learner",
                age=8,
                interest="light",
                starting_knowledge="Beginner",
                current_level=0,
                current_topic="light",
                active_character="petalo",
                customer_id=customer_id
            )
        elif age == 9:
            return LearnerProfile(
                learner_id="L-03",
                name="Story Discoverer",
                age=9,
                interest="stories",
                starting_knowledge="Beginner",
                current_level=0,
                current_topic="stories",
                active_character="quacky",
                customer_id=customer_id
            )
        elif age == 10:
            return LearnerProfile(
                learner_id="L-05",
                name="Open Inquirer",
                age=10,
                interest="open-ended",
                starting_knowledge="Beginner",
                current_level=0,
                current_topic="motors",
                active_character="quacky",
                customer_id=customer_id
            )
        elif age == 11:
            return LearnerProfile(
                learner_id="L-02",
                name="Motion Explorer",
                age=11,
                interest="motors",
                starting_knowledge="Intermediate",
                current_level=1,
                current_topic="motors",
                active_character="tiko",
                customer_id=customer_id
            )
        else: # 12+
            return LearnerProfile(
                learner_id="L-04",
                name="Circuit Master",
                age=12,
                interest="electronics",
                starting_knowledge="Advanced",
                current_level=2,
                current_topic="circuits",
                active_character="tolly",
                customer_id=customer_id
            )

    @staticmethod
    def detect_age_in_message(message: str) -> Optional[int]:
        """
        Detects if the learner states their age in message, e.g. 'I am 8', 'I am 11 years old', '8 years old'.
        """
        msg_lower = message.lower()
        match = re.search(r"\b(i am|i'm|age)\s*(\d{1,2})\b", msg_lower)
        if match:
            try:
                return int(match.group(2))
            except ValueError:
                pass

        match_years = re.search(r"\b(\d{1,2})\s*(years|yr|yrs)?\s*old\b", msg_lower)
        if match_years:
            try:
                return int(match_years.group(1))
            except ValueError:
                pass

        return None

    @staticmethod
    def detect_escalation_intent(message: str) -> bool:
        patterns = [
            r"i (already|know) (this|that|how)",
            r"i (already )?know",
            r"too easy",
            r"boring",
            r"already understand",
            r"give me (something )?(harder|deeper|more advanced)",
            r"next level"
        ]
        msg_lower = message.lower()
        return any(re.search(p, msg_lower) for p in patterns)

    @staticmethod
    def detect_interest_change(message: str) -> Tuple[bool, str]:
        msg_lower = message.lower()
        if "light" in msg_lower or "led" in msg_lower:
            return True, "light"
        elif "motor" in msg_lower or "movement" in msg_lower or "tail" in msg_lower:
            return True, "motors"
        elif "circuit" in msg_lower or "timer" in msg_lower or "sequenc" in msg_lower:
            return True, "circuits"
        return False, ""

    @staticmethod
    def adapt_profile(profile: LearnerProfile, message: str) -> Tuple[LearnerProfile, bool, bool, str]:
        escalation_triggered = False
        interest_changed = False
        new_topic = ""

        # Check if age stated in message
        detected_age = PersonalizationEngine.detect_age_in_message(message)
        if detected_age and detected_age != profile.age:
            # Re-map profile to age preset
            synthetic = PersonalizationEngine.get_profile_by_age(detected_age, profile.customer_id)
            profile.age = synthetic.age
            profile.learner_id = synthetic.learner_id
            profile.name = synthetic.name
            profile.interest = synthetic.interest
            profile.starting_knowledge = synthetic.starting_knowledge
            profile.current_level = synthetic.current_level
            profile.current_topic = synthetic.current_topic
            profile.active_character = synthetic.active_character

        # Check escalation
        if PersonalizationEngine.detect_escalation_intent(message):
            escalation_triggered = True
            if profile.current_level < 2:
                profile.current_level += 1
                if profile.current_level == 1:
                    profile.starting_knowledge = "Intermediate"
                elif profile.current_level >= 2:
                    profile.starting_knowledge = "Advanced"

        # Check interest change
        changed, topic = PersonalizationEngine.detect_interest_change(message)
        if changed and topic != profile.current_topic:
            interest_changed = True
            new_topic = topic
            profile.interest = topic
            profile.current_topic = topic

        return profile, escalation_triggered, interest_changed, new_topic

    @staticmethod
    def get_difficulty_label(level: int) -> str:
        if level == 0:
            return "Beginner"
        elif level == 1:
            return "Intermediate"
        else:
            return "Advanced"
