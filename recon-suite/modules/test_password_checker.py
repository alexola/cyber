from password_checker import check_pwd_strength

# Example passwords to test
passwords = [
    "password",
    "Password1",
    "Passwo¬#d1!",
    "pass",
    "P@ssw0rd123"
]

for pwd in passwords:
    rating, feedback = check_pwd_strength(pwd)
    print(f"Password: {pwd}")
    print(f"Strength: {rating}")
    print("Feedback:", feedback)
    print("-" * 30)