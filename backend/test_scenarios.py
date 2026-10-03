import os
import sys
import unittest
from fastapi.testclient import TestClient

# Ensure backend path is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

client = TestClient(app)

class TestFunobotzScenarios(unittest.TestCase):

    def test_scenario_1_tiko_motors(self):
        """SCENARIO 1: FZ-HACK-002 User asks about Tiko and motors."""
        response = client.post("/api/demo/scenario", json={"scenario_id": 1})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["response"]["active_character"], "tiko")
        self.assertTrue(data["response"]["access_granted"])
        self.assertIn("thread", data["response"]["answer"].lower())

    def test_scenario_2_changing_interests(self):
        """SCENARIO 2: FZ-HACK-001 Start with motors, change to light."""
        response = client.post("/api/demo/scenario", json={"scenario_id": 2})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["response"]["active_character"], "petalo")
        self.assertEqual(data["response"]["active_topic"], "light")

    def test_scenario_3_no_product_access(self):
        """SCENARIO 3: FZ-HACK-005 No valid purchased product."""
        response = client.post("/api/demo/scenario", json={"scenario_id": 3})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["response"]["access_granted"])
        self.assertIsNotNone(data["response"]["access_notice"])

    def test_scenario_4_unclear_question(self):
        """SCENARIO 4: User asks 'Why does it move?' without context."""
        response = client.post("/api/demo/scenario", json={"scenario_id": 4})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["response"]["clarification_needed"])
        self.assertGreater(len(data["response"]["clarification_options"]), 0)

    def test_scenario_5_unsupported_fact(self):
        """SCENARIO 5: User asks 'What is Tiko's favorite food?'."""
        response = client.post("/api/demo/scenario", json={"scenario_id": 5})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNotNone(data["response"]["unsupported_fact_notice"])
        self.assertIn("favorite food", data["response"]["answer"].lower())

    def test_scenario_6_escalation_intent(self):
        """SCENARIO 6: Learner says 'I already know this.'"""
        response = client.post("/api/demo/scenario", json={"scenario_id": 6})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["response"]["escalation_triggered"])
        self.assertEqual(data["response"]["difficulty"], "Intermediate")

    def test_scenario_7_unreleased_character(self):
        """SCENARIO 7: Judge selects official unreleased character (Cuby)."""
        response = client.post("/api/demo/scenario", json={"scenario_id": 7})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["response"]["active_character"], "cuby")
        self.assertIn("pending release", data["response"]["answer"].lower())

    def test_scenario_8_multi_product_customer(self):
        """SCENARIO 8: Multi-product customer FZ-HACK-004 (Quacky + Tiko + Tolly)."""
        response = client.post("/api/demo/scenario", json={"scenario_id": 8})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["response"]["access_granted"])
        cust_res = client.get("/api/customer/FZ-HACK-004")
        self.assertEqual(cust_res.status_code, 200)
        cust_data = cust_res.json()
        self.assertIn("quacky", cust_data["accessible_characters"])
        self.assertIn("tiko", cust_data["accessible_characters"])
        self.assertIn("tolly", cust_data["accessible_characters"])

if __name__ == "__main__":
    unittest.main()
