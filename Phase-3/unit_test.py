import unittest
from firebase import signup_user, login_user
from dashboard import predict_hypertension_risk

class TestHealthApp(unittest.TestCase):

    def test_signup_user(self):
        success, message, uid = signup_user("test@example.com", "password123", "TestUser", 25, "Male", "O+")
        self.assertTrue(success)
        self.assertIsNotNone(uid)

    def test_login_user(self):
        success, message, uid = login_user("test@example.com", "password123")
        self.assertTrue(success)
        self.assertIsNotNone(uid)

    def test_predict_hypertension_risk(self):
        risk_level, recommendations = predict_hypertension_risk(26.5, 88, 135, 85, 40)
        self.assertIn(risk_level, [0, 1])
        self.assertIsInstance(recommendations, dict)

if __name__ == "__main__":
    unittest.main()
