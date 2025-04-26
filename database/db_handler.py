import mysql.connector
from mysql.connector import Error
from config.database_config import DB_CONFIG
import bcrypt

class DatabaseHandler:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Establish connection to the database"""
        try:
            # First connect without database to create it if needed
            temp_config = DB_CONFIG.copy()
            temp_config.pop('database', None)  # Remove database name
            temp_conn = mysql.connector.connect(**temp_config)
            
            # Create database if it doesn't exist
            cursor = temp_conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            cursor.close()
            temp_conn.close()

            # Now connect to the specific database
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("Successfully connected to the database")
                
                # Create tables if they don't exist
                self.create_tables()
                
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            cursor = self.connection.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    account_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    pin_code TEXT NOT NULL,
                    balance DECIMAL(10,2) DEFAULT 0.00,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    sender_id INT,
                    receiver_id INT,
                    amount DECIMAL(10,2) NOT NULL,
                    transaction_type ENUM('DEPOSIT', 'WITHDRAW', 'TRANSFER') NOT NULL,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users(account_id),
                    FOREIGN KEY (receiver_id) REFERENCES users(account_id)
                )
            """)
            
            self.connection.commit()
            cursor.close()
            print("Tables created successfully")
            
        except Error as e:
            print(f"Error creating tables: {e}")

    def disconnect(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def execute_query(self, query, params=None, fetch=True):
        """Execute a SQL query and return results if fetch is True"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                self.connection.commit()
                cursor.close()
                return True
        except Error as e:
            print(f"Error executing query: {e}")
            return False

    def hash_pin(self, pin_code):
        """Hash a PIN code using bcrypt"""
        try:
            pin_bytes = pin_code.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(pin_bytes, salt)
            return hashed.decode('utf-8')
        except Exception as e:
            print(f"Error hashing PIN: {e}")
            return None

    def verify_pin(self, pin_code, hashed_pin):
        """Verify a PIN code against its hash"""
        try:
            pin_bytes = pin_code.encode('utf-8')
            hashed_bytes = hashed_pin.encode('utf-8')
            return bcrypt.checkpw(pin_bytes, hashed_bytes)
        except (ValueError, AttributeError):
            # If the hash is invalid or not in the correct format
            return False

    def create_user(self, username, pin_code):
        """Create a new user in the database with hashed PIN"""
        hashed_pin = self.hash_pin(pin_code)
        if not hashed_pin:
            return False
        query = "INSERT INTO users (username, pin_code) VALUES (%s, %s)"
        return self.execute_query(query, (username, hashed_pin), fetch=False)

    def verify_user(self, username, pin_code):
        """Verify user credentials and return account_id if valid"""
        try:
            # First get the hashed PIN for the username
            query = "SELECT account_id, pin_code FROM users WHERE username = %s"
            result = self.execute_query(query, (username,))
            
            if not result:
                return None
                
            account_id, hashed_pin = result[0]
            
            # Verify the provided PIN against the stored hash
            if self.verify_pin(pin_code, hashed_pin):
                return account_id
            return None
        except Exception as e:
            print(f"Error verifying user: {e}")
            return None

    def get_balance(self, account_id):
        """Get user's current balance"""
        query = "SELECT balance FROM users WHERE account_id = %s"
        result = self.execute_query(query, (account_id,))
        return result[0][0] if result else None

    def update_balance(self, account_id, amount):
        """Update user's balance"""
        query = "UPDATE users SET balance = balance + %s WHERE account_id = %s"
        return self.execute_query(query, (amount, account_id), fetch=False)

    def record_transaction(self, sender_id, receiver_id, amount, transaction_type):
        """Record a transaction in the database"""
        query = """
        INSERT INTO transactions (sender_id, receiver_id, amount, transaction_type)
        VALUES (%s, %s, %s, %s)
        """
        return self.execute_query(query, (sender_id, receiver_id, amount, transaction_type), fetch=False)

    def check_username_exists(self, username):
        """Check if a username already exists"""
        query = "SELECT COUNT(*) FROM users WHERE username = %s"
        result = self.execute_query(query, (username,))
        return result[0][0] > 0 if result else False 