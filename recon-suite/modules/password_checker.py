import string #-> access common character set like letters, digits, and punctuation
import math # -> calculating the entropy of the password
import re  # -> regular expressions, helps us check if the password has certain patterns

def check_pwd_strength(password):
  if not isinstance(password, str):
    raise ValueError("Password must be a string.")
  strength = 0
  feedback = []

  if len(password) >= 8:
    strength += 1
  else:
    feedback.append('Your password should be at least 8 characters long.')

  if re.search(r"[A-Z]", password):
    strength += 1
  else:
    feedback.append('You forgot to add at least one uppercase letter.')
  
  if re.search(r"[a-z]", password):
    strength += 1
  else:
    feedback.append('It is important to keep at least one lowercase letter in your password.')
  
  if re.search(r"[0-9]", password):
    strength +=1
  else:
    feedback.append('Numbers are important in the password , at least one.')
  
  if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
    strength += 1
  else:
    feedback.append('Special characters are cool , let use one minimum')

  #Table for rating how strong the password is

  rating = {
    5: "Very Strong",
    4: "Strong",
    3: "Moderate",
    2: "Weak",
    1: "Very Weak",
    0: "Extremely Weak"
  }
  entropy = estimate_entropy(password) #Estimate the entropy of the password
  return rating[strength], feedback, entropy

def estimate_entropy(password):
    # Calculate the entropy of the password
    charset = 0
    if any(c.islower() for c in password):
        charset += 26 # a-z lowercase letters
    if any(c.isupper() for c in password):
        charset += 26 # A-Z uppercase letters
    if any(c.isdigit() for c in password):
        charset += 10 # 0-9 digits
    if any(c in "!@#$%^&*()-_=+[]{}|;:',.<>?/" for c in password):
        charset += 32 # Common special characters
    if any(c.isspace() for c in password):
        charset += 1 # White space characters

    if charset == 0 or len(password) == 0:
        return 0 # avoid division by zero

    # Calculate entropy
    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)

if __name__ == "__main__":
    pwd = input("Enter a password to check: ")
    rating, feedback, entropy = check_pwd_strength(pwd)

    print(f"Strength: {rating}")
    print("Feedback:", "; ".join (feedback))

    # Show entropy how strong the password is based on bits
    print(f"Estimated Entropy: {entropy} bits")
    if entropy < 40:
        print(f"Entropy Rating: Weak ❌")
    elif 40 <= entropy < 60:
        print(f"Entropy Rating: Moderate ⚠️")
    else:
        print(f"Entropy Rating: Strong ✅")