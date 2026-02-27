import unittest
from fastapi.testclient import TestClient

from app.main import app


class AcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def verify(self, title: str):
        resp = self.client.post("/verify", json={"title": title})
        self.assertEqual(resp.status_code, 200)
        return resp.json()

    def test_disallowed_word_rejected(self):
        data = self.verify("Crime Daily Chronicle")
        rules = {v["rule"] for v in data["violations"]}
        self.assertIn("disallowed_word", rules)
        self.assertLessEqual(data["verification_probability"], 0.1)

    def test_combination_rejected(self):
        data = self.verify("Hindu Indian Express")
        rules = {v["rule"] for v in data["violations"]}
        self.assertIn("combination", rules)
        self.assertLessEqual(data["verification_probability"], 0.1)

    def test_spelling_variation_detected(self):
        data = self.verify("Namascar")
        rules = {v["rule"] for v in data["violations"]}
        self.assertTrue("spelling_variation" in rules or "phonetic_similarity" in rules)

    def test_probability_is_bounded_by_similarity(self):
        data = self.verify("Morning Herald")
        self.assertLessEqual(data["verification_probability"], 1.0 - data["similarity_score"] + 1e-9)

    def test_application_tracking(self):
        payload = {"title": "Sunrise Dispatch", "user_email": "acceptance@example.com"}
        resp = self.client.post("/application", json=payload)
        self.assertEqual(resp.status_code, 200)
        app_data = resp.json()
        self.assertIn(app_data["status"], {"approved", "rejected"})

        get_resp = self.client.get("/applications/acceptance@example.com")
        self.assertEqual(get_resp.status_code, 200)
        apps = get_resp.json()["applications"]
        self.assertTrue(any(a["submitted_title"] == "Sunrise Dispatch" for a in apps))


if __name__ == "__main__":
    unittest.main()
