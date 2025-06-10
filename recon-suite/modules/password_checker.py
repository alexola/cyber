# re = regular expressions, helps us check if the password has certain patterns

import re 

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
  
  if re.search(r"[09]", password):
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

  return rating[strength], feedback

if __name__ == "__main__":
    pwd = input("Enter a password to check: ")
    rating, feedback = check_pwd_strength(pwd)
    print(f"Strength: {rating}")
    print("Feedback:", "; ".join (feedback))