from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QLineEdit, QMessageBox, QStackedWidget, QSpacerItem, QSizePolicy,
                            QHBoxLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor
from database.db_handler import DatabaseHandler

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseHandler()
        self.current_user_id = None
        
        # Set window to full screen and remove window frame
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.showFullScreen()
        
        # Get screen dimensions
        screen = self.screen().geometry()
        self.setGeometry(screen)
        
        self.init_ui()
        self.setup_styles()

    def setup_styles(self):
        """Setup the application-wide styles"""
        # Set application-wide styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QPushButton {
                background-color: #ff8c00;
                color: white;
                border: none;
                padding: 20px;
                font-size: 32px;
                border-radius: 12px;
                min-width: 400px;
                min-height: 80px;
            }
            QPushButton:hover {
                background-color: #ffa500;
            }
            QPushButton:pressed {
                background-color: #ff6b00;
            }
            QLabel {
                color: white;
                font-size: 36px;
            }
            QLineEdit {
                padding: 20px;
                font-size: 32px;
                border: 2px solid #ff8c00;
                border-radius: 8px;
                background-color: #2a2a2a;
                color: white;
                min-height: 60px;
                min-width: 500px;
            }
            QMessageBox {
                background-color: #1a1a1a;
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #ff8c00;
                color: white;
                min-width: 100px;
            }
            #exitButton {
                background-color: #ff0000;
                color: white;
                border: 4px solid #ff0000;
                border-radius: 4px;
                font-size: 24px;
                font-weight: bold;
                min-width: 50px;
                min-height: 50px;
                max-width: 50px;
                max-height: 50px;
                padding: 0px;
                margin: 20px;
            }
            #exitButton:hover {
                background-color: #ff3333;
                border-color: #ff3333;
            }
            #exitButton:pressed {
                background-color: #cc0000;
                border-color: #cc0000;
            }
        """)

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Virtual ATM')
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create top bar with exit button
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(0, 0, 20, 0)
        top_bar_layout.setSpacing(0)
        top_bar_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Create exit button
        exit_button = QPushButton("X", self)
        exit_button.setObjectName("exitButton")
        exit_button.clicked.connect(self.close)
        exit_button.setFixedSize(50, 50)
        top_bar_layout.addWidget(exit_button)

        # Add top bar to main layout
        main_layout.addWidget(top_bar)

        # Create stacked widget for different screens
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Create and add screens
        self.main_menu = self.create_main_menu()
        self.login_screen = self.create_login_screen()
        self.activate_card_screen = self.create_activate_card_screen()
        self.user_menu = self.create_user_menu()
        self.deposit_screen = self.create_deposit_screen()
        self.withdraw_screen = self.create_withdraw_screen()
        self.transfer_screen = self.create_transfer_screen()
        self.check_balance_screen = self.create_check_balance_screen()

        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.activate_card_screen)
        self.stacked_widget.addWidget(self.user_menu)
        self.stacked_widget.addWidget(self.deposit_screen)
        self.stacked_widget.addWidget(self.withdraw_screen)
        self.stacked_widget.addWidget(self.transfer_screen)
        self.stacked_widget.addWidget(self.check_balance_screen)

    def create_main_menu(self):
        """Create the main menu screen"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(40)
        layout.setContentsMargins(100, 100, 100, 100)
        
        # Add flexible spacing at the top
        layout.addSpacerItem(QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding))

        title = QLabel("Welcome to Virtual ATM")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 64px; font-weight: bold; color: #ff8c00;")
        layout.addWidget(title)
        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        login_btn = QPushButton("Login")
        login_btn.setMinimumSize(QSize(400, 80))
        login_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.login_screen))
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        activate_btn = QPushButton("Activate New Card")
        activate_btn.setMinimumSize(QSize(400, 80))
        activate_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.activate_card_screen))
        layout.addWidget(activate_btn, alignment=Qt.AlignCenter)

        # Add flexible spacing at the bottom
        layout.addSpacerItem(QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        widget.setLayout(layout)
        return widget

    def create_login_screen(self):
        """Create the login screen"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(40)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addSpacerItem(QSpacerItem(20, 150, QSizePolicy.Minimum, QSizePolicy.Expanding))

        title = QLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 64px; font-weight: bold; color: #ff8c00;")
        layout.addWidget(title)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))

        username_label = QLabel("Username:")
        username_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        pin_label = QLabel("PIN Code:")
        pin_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(pin_label)
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pin_input, alignment=Qt.AlignCenter)

        login_btn = QPushButton("Login")
        login_btn.setMinimumSize(QSize(400, 80))
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        back_btn = QPushButton("Back")
        back_btn.setMinimumSize(QSize(400, 80))
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu))
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        layout.addSpacerItem(QSpacerItem(20, 150, QSizePolicy.Minimum, QSizePolicy.Expanding))
        widget.setLayout(layout)
        return widget

    def create_activate_card_screen(self):
        """Create the activate card screen"""
        widget = QWidget()
        layout = QVBoxLayout()

        new_username_label = QLabel("New Username:")
        self.new_username_input = QLineEdit()
        layout.addWidget(new_username_label)
        layout.addWidget(self.new_username_input)

        new_pin_label = QLabel("New PIN Code:")
        self.new_pin_input = QLineEdit()
        self.new_pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(new_pin_label)
        layout.addWidget(self.new_pin_input)

        activate_btn = QPushButton("Activate Card")
        activate_btn.clicked.connect(self.handle_activate_card)
        layout.addWidget(activate_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu))
        layout.addWidget(back_btn)

        widget.setLayout(layout)
        return widget

    def create_user_menu(self):
        """Create the user menu screen"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("ATM Services")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #ff8c00;")
        layout.addWidget(title)

        # Button container
        button_container = QWidget()
        button_layout = QVBoxLayout()
        button_layout.setSpacing(15)

        check_balance_btn = QPushButton("Check Balance")
        check_balance_btn.clicked.connect(self.show_check_balance)
        button_layout.addWidget(check_balance_btn)

        deposit_btn = QPushButton("Deposit")
        deposit_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.deposit_screen))
        button_layout.addWidget(deposit_btn)

        withdraw_btn = QPushButton("Withdraw")
        withdraw_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.withdraw_screen))
        button_layout.addWidget(withdraw_btn)

        transfer_btn = QPushButton("Transfer")
        transfer_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.transfer_screen))
        button_layout.addWidget(transfer_btn)

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.handle_logout)
        button_layout.addWidget(logout_btn)

        button_container.setLayout(button_layout)
        layout.addWidget(button_container, alignment=Qt.AlignCenter)

        widget.setLayout(layout)
        return widget

    def create_deposit_screen(self):
        """Create the deposit screen"""
        widget = QWidget()
        layout = QVBoxLayout()

        amount_label = QLabel("Amount to Deposit:")
        self.deposit_amount_input = QLineEdit()
        layout.addWidget(amount_label)
        layout.addWidget(self.deposit_amount_input)

        deposit_btn = QPushButton("Deposit")
        deposit_btn.clicked.connect(self.handle_deposit)
        layout.addWidget(deposit_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.user_menu))
        layout.addWidget(back_btn)

        widget.setLayout(layout)
        return widget

    def create_withdraw_screen(self):
        """Create the withdraw screen"""
        widget = QWidget()
        layout = QVBoxLayout()

        amount_label = QLabel("Amount to Withdraw:")
        self.withdraw_amount_input = QLineEdit()
        layout.addWidget(amount_label)
        layout.addWidget(self.withdraw_amount_input)

        withdraw_btn = QPushButton("Withdraw")
        withdraw_btn.clicked.connect(self.handle_withdraw)
        layout.addWidget(withdraw_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.user_menu))
        layout.addWidget(back_btn)

        widget.setLayout(layout)
        return widget

    def create_transfer_screen(self):
        """Create the transfer screen"""
        widget = QWidget()
        layout = QVBoxLayout()

        recipient_label = QLabel("Recipient Account ID:")
        self.recipient_input = QLineEdit()
        layout.addWidget(recipient_label)
        layout.addWidget(self.recipient_input)

        amount_label = QLabel("Amount to Transfer:")
        self.transfer_amount_input = QLineEdit()
        layout.addWidget(amount_label)
        layout.addWidget(self.transfer_amount_input)

        transfer_btn = QPushButton("Transfer")
        transfer_btn.clicked.connect(self.handle_transfer)
        layout.addWidget(transfer_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.user_menu))
        layout.addWidget(back_btn)

        widget.setLayout(layout)
        return widget

    def create_check_balance_screen(self):
        """Create the check balance screen"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Account Balance")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; color: #ff8c00;")
        layout.addWidget(title)

        self.balance_label = QLabel()
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            color: #00ff00;
            padding: 20px;
            background-color: #2a2a2a;
            border-radius: 10px;
        """)
        layout.addWidget(self.balance_label)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.user_menu))
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

        widget.setLayout(layout)
        return widget

    def handle_login(self):
        """Handle login attempt"""
        username = self.username_input.text()
        pin_code = self.pin_input.text()

        if not username or not pin_code:
            QMessageBox.warning(self, "Error", "Please enter both username and PIN code")
            return

        account_id = self.db.verify_user(username, pin_code)
        if account_id:
            self.current_user_id = account_id
            self.stacked_widget.setCurrentWidget(self.user_menu)
            self.username_input.clear()
            self.pin_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or PIN code")

    def handle_activate_card(self):
        """Handle new card activation"""
        username = self.new_username_input.text()
        pin_code = self.new_pin_input.text()

        if not username or not pin_code:
            QMessageBox.warning(self, "Error", "Please enter both username and PIN code")
            return

        if len(pin_code) != 4 or not pin_code.isdigit():
            QMessageBox.warning(self, "Error", "PIN code must be 4 digits")
            return

        if self.db.check_username_exists(username):
            QMessageBox.warning(self, "Error", "Username already exists")
            return

        if self.db.create_user(username, pin_code):
            QMessageBox.information(self, "Success", "Card activated successfully!")
            self.stacked_widget.setCurrentWidget(self.main_menu)
            self.new_username_input.clear()
            self.new_pin_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Failed to activate card")

    def handle_logout(self):
        """Handle user logout"""
        self.current_user_id = None
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def handle_deposit(self):
        """Handle deposit transaction"""
        try:
            amount = float(self.deposit_amount_input.text())
            if amount <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid amount")
            return

        if self.db.update_balance(self.current_user_id, amount):
            self.db.record_transaction(self.current_user_id, self.current_user_id, amount, 'DEPOSIT')
            QMessageBox.information(self, "Success", "Deposit successful!")
            self.deposit_amount_input.clear()
            self.stacked_widget.setCurrentWidget(self.user_menu)
        else:
            QMessageBox.warning(self, "Error", "Failed to process deposit")

    def handle_withdraw(self):
        """Handle withdraw transaction"""
        try:
            amount = float(self.withdraw_amount_input.text())
            if amount <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid amount")
            return

        current_balance = self.db.get_balance(self.current_user_id)
        if amount > current_balance:
            QMessageBox.warning(self, "Error", "Insufficient funds")
            return

        if self.db.update_balance(self.current_user_id, -amount):
            self.db.record_transaction(self.current_user_id, self.current_user_id, amount, 'WITHDRAW')
            QMessageBox.information(self, "Success", "Withdrawal successful!")
            self.withdraw_amount_input.clear()
            self.stacked_widget.setCurrentWidget(self.user_menu)
        else:
            QMessageBox.warning(self, "Error", "Failed to process withdrawal")

    def handle_transfer(self):
        """Handle transfer transaction"""
        try:
            recipient_id = int(self.recipient_input.text())
            amount = float(self.transfer_amount_input.text())
            if amount <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid recipient ID and amount")
            return

        current_balance = self.db.get_balance(self.current_user_id)
        if amount > current_balance:
            QMessageBox.warning(self, "Error", "Insufficient funds")
            return

        if self.db.update_balance(self.current_user_id, -amount) and \
           self.db.update_balance(recipient_id, amount):
            self.db.record_transaction(self.current_user_id, recipient_id, amount, 'TRANSFER')
            QMessageBox.information(self, "Success", "Transfer successful!")
            self.recipient_input.clear()
            self.transfer_amount_input.clear()
            self.stacked_widget.setCurrentWidget(self.user_menu)
        else:
            QMessageBox.warning(self, "Error", "Failed to process transfer")

    def show_check_balance(self):
        """Show current balance"""
        balance = self.db.get_balance(self.current_user_id)
        if balance is not None:
            self.balance_label.setText(f"Current Balance: ${balance:.2f}")
        else:
            self.balance_label.setText("Error retrieving balance")
        self.stacked_widget.setCurrentWidget(self.check_balance_screen)

    def resizeEvent(self, event):
        """Handle window resize to keep exit button in correct position"""
        super().resizeEvent(event)
        # Update exit button position when window is resized
        exit_button = self.findChild(QPushButton, "exitButton")
        if exit_button:
            exit_button.move(self.width() - 70, 20) 