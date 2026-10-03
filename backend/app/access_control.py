import json
import os
from typing import Dict, List, Any, Optional

class AccessControlEngine:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.customers = self._load_json("customers.json")
        self.products = self._load_json("products.json")

    def _load_json(self, filename: str) -> Dict[str, Any]:
        path = os.path.join(self.data_dir, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        return self.customers.get(customer_id)

    def get_accessible_products(self, customer_id: str) -> List[str]:
        cust = self.get_customer(customer_id)
        if not cust:
            return []
        return cust.get("purchased_products", [])

    def get_accessible_characters(self, customer_id: str) -> List[str]:
        products = self.get_accessible_products(customer_id)
        characters = []
        for prod_id in products:
            prod_info = self.products.get(prod_id, {})
            char_id = prod_info.get("character_id")
            if char_id:
                characters.append(char_id)
        return characters

    def check_access(self, customer_id: str, character_id: str) -> Dict[str, Any]:
        """
        Validates whether customer_id has valid access for product-specific assistance for character_id.
        """
        accessible_chars = self.get_accessible_characters(customer_id)
        
        # If character is mapped to a product (e.g. tiko, petalo, quacky, tolly)
        # customer MUST own that product to get product-specific assistance.
        is_product_character = character_id in ["tiko", "petalo", "quacky", "tolly"]
        
        if is_product_character and character_id not in accessible_chars:
            char_name = character_id.capitalize()
            return {
                "granted": False,
                "notice": f"Access Notice: Customer ID '{customer_id}' does not hold a active license/purchase for {char_name}. Product-specific hardware assistance is restricted to verified owners. You can still ask general STEM questions!",
                "accessible_characters": accessible_chars
            }
        
        return {
            "granted": True,
            "notice": None,
            "accessible_characters": accessible_chars
        }
