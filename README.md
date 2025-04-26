# Virtual ATM System

A Python-based virtual ATM system with a graphical user interface and MySQL database integration.

## Features

- User authentication (login/register)
- Balance checking
- Deposit money
- Withdraw money
- Transfer money between accounts
- Transaction history tracking

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- PyQt6
- mysql-connector-python
- python-dotenv

## Setup Instructions

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up the MySQL database:
   - Create a MySQL database named 'virtual_atm'
   - Run the SQL script in `database/setup.sql` to create the necessary tables

3. Configure the database connection:
   - Create a `.env` file in the project root
   - Add the following variables:
     ```
     DB_HOST=localhost
     DB_USER=your_username
     DB_PASSWORD=your_password
     DB_NAME=virtual_atm
     ```

## Running the Application

1. Start the MySQL server
2. Run the main application:
   ```bash
   python main.py
   ```

## Project Structure

- `main.py` - Main application entry point
- `gui/` - GUI-related files
  - `main_window.py` - Main window and UI components
- `database/` - Database-related files
  - `setup.sql` - Database schema and setup
  - `db_handler.py` - Database operations handler
- `config/` - Configuration files
  - `database_config.py` - Database configuration

## Security Features

- PIN code protection
- Input validation
- Transaction validation
- Secure database operations

## Notes

- PIN codes must be 4 digits
- Usernames must be unique
- Users cannot withdraw or transfer more than their current balance
- All transactions are recorded in the database 