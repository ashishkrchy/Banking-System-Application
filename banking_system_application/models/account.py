from datetime import datetime
from decimal import Decimal


class Account:
    def __init__(self, db):
        self.db = db

    def login(self, account_number, password):
        sql = '''SELECT * FROM users 
                 WHERE account_number = %s AND password = %s AND is_active = TRUE'''
        self.db.cursor.execute(sql, (account_number, password))
        return self.db.cursor.fetchone()

    def get_balance(self, account_number):
        self.db.cursor.execute('SELECT balance FROM users WHERE account_number = %s', 
                                (account_number,))
        result = self.db.cursor.fetchone()
        return Decimal(result[0]) if result else None

    def get_transactions(self, account_number):
        sql = '''SELECT transaction_type, amount, timestamp 
                 FROM transactions WHERE account_number = %s 
                 ORDER BY timestamp DESC'''
        self.db.cursor.execute(sql, (account_number,))
        return self.db.cursor.fetchall()

    def update_balance(self, account_number, amount, transaction_type, external_transaction=False):
        amount = Decimal(amount)

        # Get current balance
        current_balance = self.get_balance(account_number)
        if current_balance is None:
            return False, "Account not found"

        # Check for sufficient balance in case of debit
        if transaction_type == 'debit' and current_balance < amount:
            return False, "Insufficient balance"

        # Calculate new balance
        new_balance = current_balance + amount if transaction_type == 'credit' else current_balance - amount

        try:
            if not external_transaction and not self.db.conn.autocommit:
                self.db.conn.autocommit = True  # Enable autocommit for independent operations

            # Update user balance
            sql_update = 'UPDATE users SET balance = %s WHERE account_number = %s'
            self.db.cursor.execute(sql_update, (new_balance, account_number))

            # Record transaction
            sql_transaction = '''INSERT INTO transactions 
                                (account_number, transaction_type, amount, timestamp) 
                                VALUES (%s, %s, %s, %s)'''
            self.db.cursor.execute(sql_transaction, 
                                (account_number, transaction_type, amount, datetime.now()))

            if not external_transaction and not self.db.conn.autocommit:
                self.db.conn.commit()  # Commit only if autocommit is disabled

            return True, f"Transaction successful. New balance: {new_balance}"

        except Exception as e:
            if not external_transaction and not self.db.conn.autocommit:
                self.db.conn.rollback()
            return False, f"Transaction failed: {str(e)}"


    def transfer_amount(self, from_account, to_account, amount):
        if from_account == to_account:
            return "Cannot transfer to the same account"

        amount = Decimal(amount)

        try:
            if not self.db.conn.autocommit:
                self.db.conn.start_transaction()

            # Check if recipient exists
            self.db.cursor.execute('SELECT COUNT(*) FROM users WHERE account_number = %s', 
                                    (to_account,))
            if self.db.cursor.fetchone()[0] == 0:
                if not self.db.conn.autocommit:
                    self.db.conn.rollback()
                return "Recipient account does not exist"

            # Perform debit
            debit_status, debit_message = self.update_balance(from_account, amount, 'debit', external_transaction=True)
            if not debit_status:
                if not self.db.conn.autocommit:
                    self.db.conn.rollback()
                return debit_message

            # Perform credit
            credit_status, credit_message = self.update_balance(to_account, amount, 'credit', external_transaction=True)
            if not credit_status:
                if not self.db.conn.autocommit:
                    self.db.conn.rollback()
                return credit_message

            if not self.db.conn.autocommit:
                self.db.conn.commit()
            return "Transfer successful"

        except Exception as e:
            if not self.db.conn.autocommit:
                self.db.conn.rollback()
            return f"Transfer failed: {str(e)}"

    def update_profile(self, account_number, city=None, contact=None, email=None, address=None):
        try:
            updates = []
            values = []

            if city:
                updates.append('city = %s')
                values.append(city)
            if contact:
                updates.append('contact_number = %s')
                values.append(contact)
            if email:
                updates.append('email = %s')
                values.append(email)
            if address:
                updates.append('address = %s')
                values.append(address)

            if not updates:
                return "No updates provided"

            values.append(account_number)
            sql = f'''UPDATE users SET {', '.join(updates)} 
                      WHERE account_number = %s'''

            self.db.cursor.execute(sql, values)
            self.db.conn.commit()
            return "Profile updated successfully"

        except Exception as e:
            self.db.conn.rollback()
            return f"Update failed: {str(e)}"

    def change_password(self, account_number, old_password, new_password):
        try:
            # Verify old password
            sql_verify = '''SELECT COUNT(*) FROM users 
                            WHERE account_number = %s AND password = %s'''
            self.db.cursor.execute(sql_verify, (account_number, old_password))
            if self.db.cursor.fetchone()[0] == 0:
                return "Invalid old password"

            # Update password
            sql_update = 'UPDATE users SET password = %s WHERE account_number = %s'
            self.db.cursor.execute(sql_update, (new_password, account_number))
            self.db.conn.commit()
            return "Password updated successfully"

        except Exception as e:
            self.db.conn.rollback()
            return f"Password update failed: {str(e)}"

    def toggle_account_status(self, account_number):
        try:
            sql = '''UPDATE users SET is_active = NOT is_active 
                     WHERE account_number = %s'''
            self.db.cursor.execute(sql, (account_number,))
            self.db.conn.commit()
            return "Account status updated successfully"

        except Exception as e:
            self.db.conn.rollback()
            return f"Status update failed: {str(e)}"
