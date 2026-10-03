import json
import os
import re
from typing import Dict, List, Any, Optional

class KnowledgeBaseEngine:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.characters_dir = os.path.join(data_dir, "characters")
        self.characters: Dict[str, Dict[str, Any]] = {}
        self.concepts: Dict[str, Dict[str, Any]] = {}
        self._load_characters()
        self._load_concepts()

    def _load_characters(self):
        if os.path.exists(self.characters_dir):
            for file_name in os.listdir(self.characters_dir):
                if file_name.endswith(".json"):
                    filepath = os.path.join(self.characters_dir, file_name)
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.characters[data["id"]] = data

    def _load_concepts(self):
        filepath = os.path.join(self.data_dir, "concepts.json")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                self.concepts = json.load(f)

    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        return self.characters.get(character_id)

    def get_all_characters(self) -> List[Dict[str, Any]]:
        return list(self.characters.values())

    def get_verified_facts(self, character_id: str) -> List[str]:
        char = self.get_character(character_id)
        if char:
            return char.get("verified_facts", [])
        return []

    def check_unsupported_query(self, message: str, character_id: str) -> Optional[str]:
        """
        Detects if the user is asking for arbitrary non-STEM / unapproved facts about a character
        (e.g., favorite food, favorite color, age, backstory, home, family, superpowers, etc.)
        that are absent from approved content.
        """
        unsupported_keywords = [
            "favorite food", "favorite color", "favourite food", "favourite color",
            "what does he eat", "what does she eat", "food", "birthday", "where does it live",
            "parents", "mother", "father", "best friend", "hobbies", "hobby", "pet",
            "superpower", "weapon", "backstory", "origin story", "secret identity"
        ]
        
        msg_lower = message.lower()
        for kw in unsupported_keywords:
            if kw in msg_lower:
                char_name = character_id.capitalize()
                return (
                    f"Notice: Official Funobotz learning content for {char_name} does not contain information about "
                    f"'{kw}'. I stick strictly to approved STEM concepts and verified robotics facts!"
                )
        return None
