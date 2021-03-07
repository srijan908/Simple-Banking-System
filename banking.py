# Write your code here
import random


# Class user which will store all the information of a user registered in our system
class User:
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # will be used to generate card number and pin

    def __init__(self):
        self.card_no = "400000"  # initializing the card number with 400000
        self.pin = ''
        self.balance = 0

    def generate_pin(self):
        # completing the card number
        while len(self.card_no) < 16:
            self.card_no += random.choice(User.num)

        # generating the pin for the card
        while len(self.pin) < 4:
            self.pin += random.choice(User.num)


# the user interface when if the credentials are present in the database
def log_in(cur_user):
    print("You have successfully logged in!")
    while True:
        user_ch = int(input("1. Balance\n2. Log out\n0. Exit\n"))
        if user_ch == 1:
            print(f'Balance: {cur_user.balance}')
        elif user_ch == 2:
            print("You have successfully logged out")
            return 1
        else:
            return 2


all_users = []  # will temporarily store the all the user objects

while True:
    choice = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    if choice == 1:
        new_user = User()
        new_user.generate_pin()
        print('Your car has been created')
        print(f'Your card number:\n{new_user.card_no}')
        print(f'Your card PIN:\n{new_user.pin}')

        all_users.append(new_user)  # adding to the list of the users

    elif choice == 2:
        card_num = input("Enter your card number:\n")
        card_pin = input("Enter you PIN:\n")
        found = False
        ch = 0
        for cur in range(len(all_users)):
            if all_users[cur].card_no == card_num and all_users[cur].pin == card_pin:
                found = True
                ch = log_in(all_users[cur])
                break
        if not found:
            print("Wrong card number or PIN")
            continue
        elif found and ch == 2:
            print('Bye!')
            break

    elif choice == 0:
        print('Bye!')
        break
