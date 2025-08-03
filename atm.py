import datetime
import os

class ATM:
    def __init__(self, user_file='user_data.txt'):
        self.user_file = user_file
        self.users = self.load_users()
        self.current_user = None

    def load_users(self):
        if not os.path.exists(self.user_file):
            return {}
        with open(self.user_file, 'r') as f:
            data = f.readlines()
        users = {}
        for line in data:
            if line.strip():
                username, pin, balance, *history = line.strip().split('|')
                users[username] = {
                    'pin': pin,
                    'balance': float(balance),
                    'history': history
                }
        return users

    def save_users(self):
        with open(self.user_file, 'w') as f:
            for username, info in self.users.items():
                history_str = '|'.join(info['history'])
                f.write(f"{username}|{info['pin']}|{info['balance']}|{history_str}\n")

    def login(self):
        username = input("Enter username: ")
        pin = input("Enter 4-digit PIN: ")
        if username in self.users and self.users[username]['pin'] == pin:
            self.current_user = username
            print(f"Welcome back, {username}!")
        else:
            print("Invalid username or PIN.")

    def create_account(self):
        username = input("Choose a username: ")
        if username in self.users:
            print("Username already exists.")
            return
        pin = input("Set a 4-digit PIN: ")
        self.users[username] = {
            'pin': pin,
            'balance': 0.0,
            'history': []
        }
        self.save_users()
        print("Account created successfully.")

    def check_balance(self):
        balance = self.users[self.current_user]['balance']
        print(f"Your current balance is: ${balance:.2f}")

    def deposit(self):
        amount = float(input("Enter amount to deposit: $"))
        if amount <= 0:
            print("Invalid amount.")
            return
        self.users[self.current_user]['balance'] += amount
        self.add_transaction(f"Deposited ${amount:.2f}")
        self.save_users()
        print(f"${amount:.2f} deposited successfully.")

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: $"))
        balance = self.users[self.current_user]['balance']
        if amount <= 0:
            print("Invalid amount.")
        elif amount > balance:
            print("Insufficient funds.")
        else:
            self.users[self.current_user]['balance'] -= amount
            self.add_transaction(f"Withdrew ${amount:.2f}")
            self.save_users()
            print(f"${amount:.2f} withdrawn successfully.")

    def view_history(self):
        print("Transaction History:")
        history = self.users[self.current_user]['history']
        if not history:
            print("No transactions yet.")
        else:
            for record in history:
                print(record)

    def add_transaction(self, action):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.users[self.current_user]['history'].append(f"{timestamp} - {action}")

    def logout(self):
        self.current_user = None
        print("Logged out successfully.")

    def run(self):
        while True:
            if not self.current_user:
                print("\n1. Login\n2. Create Account\n3. Exit")
                choice = input("Select an option: ")
                if choice == '1':
                    self.login()
                elif choice == '2':
                    self.create_account()
                elif choice == '3':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice.")
            else:
                print(f"\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Transaction History\n5. Logout")
                choice = input("Select an option: ")
                if choice == '1':
                    self.check_balance()
                elif choice == '2':
                    self.deposit()
                elif choice == '3':
                    self.withdraw()
                elif choice == '4':
                    self.view_history()
                elif choice == '5':
                    self.logout()
                else:
                    print("Invalid choice.")

if __name__ == "__main__":
    atm = ATM()
    atm.run()
