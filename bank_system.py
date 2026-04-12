import os
import pandas as pd
from git_sync import push

class User_account:
    def __init__(self, user_id, name, password, phone_number, balance, file_path):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.balance = balance
        self.transaction_history = {
            "Current Balance": [self.balance],
            "Operation": ["No Operation Yet"],
            "Amount": ["No Operation Yet"]
        }
        self._add_to_csv(file_path)

    def _add_to_csv(self, file_path):
        if not os.path.exists(file_path):
            pd.DataFrame(columns=['user_id', 'name', 'password', 'phone_number', 'balance']).to_csv(file_path, index=False)

        data = pd.read_csv(file_path)
        if self.user_id in data['user_id'].values:
            return

        data.loc[len(data)] = [self.user_id, self.name, self.password, self.phone_number, self.balance]
        data.to_csv(file_path, index=False)
        push(f"new account {self.user_id}")

    def Delete_account(self, file_path):
        data = pd.read_csv(file_path)
        data = data[data['user_id'] != self.user_id]
        data.to_csv(file_path, index=False)
        push(f"deleted account {self.user_id}")

    def Update_username(self, new_username, file_path):
        self.name = new_username
        data = pd.read_csv(file_path)
        data.loc[data['user_id'] == self.user_id, 'name'] = self.name
        data.to_csv(file_path, index=False)
        push(f"updated username {self.user_id}")

    def Update_password(self, new_password, file_path):
        self.password = new_password
        data = pd.read_csv(file_path)
        data.loc[data['user_id'] == self.user_id, 'password'] = self.password
        data.to_csv(file_path, index=False)
        push(f"updated password {self.user_id}")

    def Update_number(self, new_number, file_path):
        self.phone_number = new_number
        data = pd.read_csv(file_path)
        data.loc[data['user_id'] == self.user_id, 'phone_number'] = self.phone_number
        data.to_csv(file_path, index=False)
        push(f"updated phone {self.user_id}")

    def _init_transactions_file(self, transaction_file):
        if not os.path.exists(transaction_file):
            pd.DataFrame(columns=['user_id', 'name', 'balance', 'amount', 'operation']).to_csv(transaction_file, index=False)

    def Deposite(self, amount, file_path, transaction_file):
        self.balance += amount
        self.transaction_history["Current Balance"].append(self.balance)
        self.transaction_history["Operation"].append("Deposit")
        self.transaction_history["Amount"].append(amount)

        data = pd.read_csv(file_path)
        data.loc[data['user_id'] == self.user_id, 'balance'] = self.balance
        data.to_csv(file_path, index=False)

        self._init_transactions_file(transaction_file)
        data = pd.read_csv(transaction_file)
        data.loc[len(data)] = [self.user_id, self.name, self.balance, "+" + str(amount), "Deposit"]
        data.to_csv(transaction_file, index=False)
        push(f"deposit {self.user_id}")

    def Withdraw(self, amount, file_path, transaction_file):
        if amount > self.balance:
            return
        self.balance -= amount
        self.transaction_history["Current Balance"].append(self.balance)
        self.transaction_history["Operation"].append("Withdraw")
        self.transaction_history["Amount"].append(amount)

        data = pd.read_csv(file_path)
        data.loc[data['user_id'] == self.user_id, 'balance'] = self.balance
        data.to_csv(file_path, index=False)

        self._init_transactions_file(transaction_file)
        data = pd.read_csv(transaction_file)
        data.loc[len(data)] = [self.user_id, self.name, self.balance, "-" + str(amount), "Withdraw"]
        data.to_csv(transaction_file, index=False)
        push(f"withdraw {self.user_id}")

    def Display_user_info(self):
        print(f"User ID: {self.user_id}\nUsername: {self.name}\nPhone: {self.phone_number}\nBalance: {self.balance}")

    def Transaction_history(self):
        print(self.transaction_history)
