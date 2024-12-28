import re

def validate_password(password):
    """
    Validates password requirements:
    - At least 8 characters
    - Contains uppercase letter
    - Contains lowercase letter
    - Contains number
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
        
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
        
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
        
    return True, "Password is valid"

def validate_email(email):
    """Validates email format"""
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return False, "Invalid email format"
    return True, "Email is valid"

def validate_contact(contact):
    """Validates contact number format"""
    if not re.match(r'^\d{10}$', contact):
        return False, "Contact number must be 10 digits"
    return True, "Contact number is valid"