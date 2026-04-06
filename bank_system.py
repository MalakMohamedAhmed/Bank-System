import os
import csv
import pandas as pd

class User_account:
    def __init__(self, user_id, name, password, phone_number, balance, file_path):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.balance = balance
        self.transaction_history = {"Current Balance" : [self.balance],
                                   "Operation" : ["No Operation Yet"],
                                   "Amount" : ["No Operation Yet"]}
        self._add_to_csv(file_path)

    def _add_to_csv(self, file_path):
        if os.path.exists(file_path):
            data = pd.read_csv(file_path)
            if self.user_id in data['user_id'].values:
                print(f"User {self.user_id} already exists.")
                return

        new_row = [self.user_id, self.name, self.password, self.phone_number, self.balance]
        data = pd.read_csv(file_path)
        data.loc[len(data)] = new_row
        data.to_csv(file_path, index=False)
        
        print(f"Account for {self.name} saved to database.")
        
    def Delete_account(self, file_path):
        target_id = self.user_id
        rows_to_keep = []
        
        data = pd.read_csv(file_path)
        data = data[data['user_id'] != self.user_id]
        data.to_csv(file_path, index=False)

    def Update_username(self, new_username, file_path):
        self.name = new_username
        data = pd.read_csv(file_path)
        data.loc[data['user_id'] == self.user_id, 'name'] = self.name
        data.to_csv(file_path, index=False)
        
    def Update_password(self, new_password, file_path):
        self.password = new_password
        data = pd.read_csv(file_path)
        data.loc[data['user_id'] == self.user_id, 'password'] = self.password
        data.to_csv(file_path, index=False)

    def Update_number(self, new_number, file_path):
        self.phone_number = new_number
        data = pd.read_csv(file_path)
        data.loc[data['user_id'] == self.user_id, 'phone_number'] = self.phone_number
        data.to_csv(file_path, index=False)

    def Display_user_info(self):
        print(f"""User ID: {self.user_id} \n Username: {self.name} \n Password: {self.password} \n 
        Phone Number: {self.phone_number} \n Bank Balance: {self.balance}""")

    def Deposite(self, amount, file_path, transaction_file):
        self.balance += amount
        self.transaction_history["Current Balance"].append(self.balance)
        self.transaction_history["Operation"].append("Deposit")
        self.transaction_history["Amount"].append(amount)

        data = pd.read_csv(file_path)
        data.loc[data['user_id'] == self.user_id, 'balance'] = self.balance
        data.to_csv(file_path, index=False)
        
        data = pd.read_csv(transaction_file)
        data.loc[len(data)] = [self.user_id, self.name, self.balance, "+" + str(amount), "Deposite"]
        data.to_csv(transaction_file, index=False)

    def Withdraw(self, amount, file_path, transaction_file):
        if amount > self.balance:
            print("Insufficient funds!")
            return
        self.balance -= amount
        self.transaction_history["Current Balance"].append(self.balance)
        self.transaction_history["Operation"].append("Withdraw")
        self.transaction_history["Amount"].append(amount)

        data = pd.read_csv(file_path)
        data.loc[data['user_id'] == self.user_id, 'balance'] = self.balance
        data.to_csv(file_path, index=False)

        data = pd.read_csv(transaction_file)
        data.loc[len(data)] = [self.user_id, self.name, self.balance, "-" + str(amount), "Withdraw"]
        data.to_csv(transaction_file, index=False)

    def Transaction_history(self):
        print(self.transaction_history)
