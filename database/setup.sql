-- Create the database
CREATE DATABASE IF NOT EXISTS virtual_atm;
USE virtual_atm;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    pin_code TEXT NOT NULL,  -- Changed to TEXT type to store bcrypt hash
    balance DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    amount DECIMAL(10,2) NOT NULL,
    transaction_type ENUM('DEPOSIT', 'WITHDRAW', 'TRANSFER') NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(account_id),
    FOREIGN KEY (receiver_id) REFERENCES users(account_id)
); 