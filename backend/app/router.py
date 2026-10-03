from typing import Dict, List, Any, Optional, Tuple

class RouterEngine:
    def __init__(self, knowledge_engine, access_engine):
        self.kb = knowledge_engine
        self.access = access_engine

    def is_ambiguous_query(self, message: str) -> bool:
        ambiguous_phrases = [
            "why does it move",
            "why is it moving",
            "how does it move",
            "why does it work",
            "how does it work",
            "what makes it go"
        ]
        msg_lower = message.lower().strip()
        cleaned = "".join(c for c in msg_lower if c.isalnum() or c.isspace())
        
        for phrase in ambiguous_phrases:
            if phrase in cleaned:
                return True
        return False

    def route_request(
        self,
        message: str,
        customer_id: str,
        current_topic: str,
        current_character: str,
        requested_character: Optional[str] = None
    ) -> Dict[str, Any]:
        accessible_chars = self.access.get_accessible_characters(customer_id)
        msg_lower = message.lower()

        # 1. Check for explicit character mention in the message text
        if "tiko" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "tiko", "concept": "motors"}
        elif "quacky" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "quacky", "concept": "motors"}
        elif "tolly" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "tolly", "concept": "circuits"}
        elif "petalo" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "petalo", "concept": "light"}
        elif "emoti" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "emoti", "concept": "behavior"}
        elif "mimo" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "mimo", "concept": "behavior"}
        elif "kuttybot" in msg_lower or "kutty bot" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "kuttybot", "concept": "speech"}
        elif "kutty omni" in msg_lower or "kutty-omni" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "kutty-omni", "concept": "pending"}
        elif "wavy" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "wavy", "concept": "pending"}
        elif "chicky" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "chicky", "concept": "pending"}
        elif "cuby" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "cuby", "concept": "pending"}
        elif "omni" in msg_lower:
            return {"clarification_needed": False, "clarification_options": None, "character_id": "omni", "concept": "pending"}

        # 2. Check ambiguous question rule (Scenario 4)
        if self.is_ambiguous_query(message):
            relevant_options = []
            if "tiko" in accessible_chars or len(accessible_chars) == 0:
                relevant_options.append("Tiko (Scorpio Bot up-and-down thread tail motion)")
            if "quacky" in accessible_chars or len(accessible_chars) == 0:
                relevant_options.append("Quacky (Movable Duck Bot powered by BO motor)")
            if "petalo" in accessible_chars:
                relevant_options.append("Petalo (Light-Up Discovery Friend)")

            return {
                "clarification_needed": True,
                "clarification_options": relevant_options,
                "character_id": current_character,
                "concept": current_topic
            }

        # 3. Explicit requested_character in API payload (e.g. from UI roster selection)
        target_char = requested_character or current_character
        if target_char and target_char.lower() in [c.lower() for c in self.kb.characters.keys()]:
            return {
                "clarification_needed": False,
                "clarification_options": None,
                "character_id": target_char.lower(),
                "concept": current_topic
            }

        return {"clarification_needed": False, "clarification_options": None, "character_id": current_character, "concept": current_topic}
