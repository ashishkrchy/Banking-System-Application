from datetime import datetime
import re
import random


class User:
    def __init__(self, db):
        self.db = db
   
    def generate_account_number(self):
        while True:
            acc_num = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            self.db.cursor.execute('SELECT COUNT(*) FROM users WHERE account_number = %s', (acc_num,))
            if self.db.cursor.fetchone()[0] == 0:
                return acc_num
    
    def validate_input(self, email, password, contact):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return False, "Invalid email format"
            
        if len(password) < 8 or not re.search(r'[A-Z]', password) or \
           not re.search(r'[a-z]', password) or not re.search(r'\d', password):
            return False, "Password must be at least 8 characters with upper, lower case and numbers"
            
        if not re.match(r'^\d{10}$', contact):
            return False, "Contact number must be 10 digits"
            
        return True, "Validation successful"
    
    def create_user(self, name, dob, city, password, initial_balance, contact, email, address):
        is_valid, message = self.validate_input(email, password, contact)
        if not is_valid:
            return message
            
        if initial_balance < 2000:
            return "Initial balance must be at least 2000"
            
        account_number = self.generate_account_number()
        
        try:
            sql = '''INSERT INTO users 
                    (account_number, name, dob, city, password, balance, 
                    contact_number, email, address, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            values = (account_number, name, dob, city, password, initial_balance,
                     contact, email, address, True)
            self.db.cursor.execute(sql, values)
            self.db.conn.commit()
            return f"User created successfully. Account number: {account_number}"
        except Exception as e:
            self.db.conn.rollback()
            return f"Error creating user: {str(e)}"