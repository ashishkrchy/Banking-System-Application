import mysql.connector
from config.database import DB_CONFIG


class DatabaseConnection:
    def __init__(self):
        # Establish a connection to the database
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        # Ensure the tables exist
        self._create_tables()
        
    def _create_tables(self):
        # Create the `users` table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                account_number CHAR(10) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                dob DATE NOT NULL,
                city VARCHAR(50),
                password VARCHAR(100) NOT NULL,
                balance DECIMAL(10,2) NOT NULL,
                contact_number VARCHAR(10),
                email VARCHAR(100),
                address TEXT,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Create the `transactions` table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_number CHAR(10),
                transaction_type ENUM('credit', 'debit') NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_number) REFERENCES users(account_number)
            )
        ''')
        
        # Commit the changes to the database
        self.conn.commit()
    
    def __del__(self):
        # Close the cursor if it exists
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        # Close the connection if it is active
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()
