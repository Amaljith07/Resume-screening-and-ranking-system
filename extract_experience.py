import re

def extract_email(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    match = re.search(email_pattern, text)
    return match.group() if match else "Not Found"

def extract_phone(text):
    phone_pattern = r'\+?\d[\d -]{8,12}\d'
    match = re.search(phone_pattern, text)
    return match.group() if match else "Not Found"

def extract_experience(text):
    experience_pattern = r'(\d+\.?\d*)\s*\+?\s*(years?|yrs?)'
    match = re.search(experience_pattern, text, re.IGNORECASE)

    if match:
        return float(match.group(1))   # supports 3.5 years also
    else:
        return 0

    if match:
        return int(match.group(1))   # return only number
    else:
        return 0
def extract_name(text):
    lines = text.split("\n")
    for line in lines:
        if len(line.strip()) > 2 and len(line.strip()) < 40:
            if "email" not in line.lower() and "phone" not in line.lower():
                return line.strip()
    return "Unknown"
  

