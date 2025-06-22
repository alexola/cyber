import unittest
from password_checker import check_pwd_strength

class TestsPasswordChecker(unittest.TestCase):
    def test_extremely_weak_password(self):
        password = "12345"
        rating, feedback, entropy = check_pwd_strength(password)
        print(password, rating, entropy)
        self.assertEqual(rating, "Very Weak")
        self.assertLess(entropy, 30)

    def test_very_weak_password(self):
        password = "password"
        rating, feedback, entropy = check_pwd_strength(password)
        print(password, rating, entropy)
        self.assertEqual(rating, "Weak")
        self.assertGreaterEqual(entropy, 30)
        self.assertLess(entropy, 40)

    def test_moderate_password(self):
        password = "Password"
        rating, feedback, entropy = check_pwd_strength(password)
        print(password, rating, entropy)
        self.assertEqual(rating, "Moderate")
        self.assertGreaterEqual(entropy, 40)
        self.assertLess(entropy, 50)

    def test_strong_password(self):
        password = "Password1!"
        rating, feedback, entropy = check_pwd_strength(password)
        print(password, rating, entropy)
        self.assertEqual(rating, "Very Strong")  # <-- Change here
        self.assertGreaterEqual(entropy, 60)
        self.assertLess(entropy, 70)

    def test_very_strong_password(self):
        password = "P@ssw0rd123!$"
        rating, feedback, entropy = check_pwd_strength(password)
        print(password, rating, entropy)
        self.assertEqual(rating, "Very Strong")
        self.assertGreaterEqual(entropy, 70)

if __name__ == "__main__":
    unittest.main()