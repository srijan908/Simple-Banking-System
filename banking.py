# Write your code here
import random
import sqlite3
from luhn_algorithm import check_luhn


# Class user which will store all the information of a user registered in our system
class User:
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # will be used to generate card number and pin

    def __init__(self):
        self.card_no = "400000"  # initializing the card number with 400000
        self.pin = ''
        self.balance = 0

    def generate_pin(self):
        # completing the card number
        check_sum = 0
        while len(self.card_no) < 15:
            self.card_no += random.choice(User.num)

        # Applying the Luhn algorithm to generate a universally valid credit card
        for x in range(1, 16):
            if x % 2 == 1:
                temp = 2 * int(self.card_no[x - 1])
                if temp > 9:
                    temp -= 9
                check_sum += temp
            else:
                check_sum += int(self.card_no[x - 1])

        if check_sum % 10 == 0:
            self.card_no += '0'
        else:
            self.card_no += str(10-check_sum % 10)

        # generating the pin for the card
        while len(self.pin) < 4:
            self.pin += random.choice(User.num)


# the user interface when if the credentials are present in the database
def log_in(cur_user_card, cur_user_pin):
    print("You have successfully logged in!")
    while True:
        user_ch = int(input("1. Balance\n2. Add income\n3. Do transfer"
                            "\n4. Close account\n5. Log out\n0. Exit\n"))
        get_con.execute('''SELECT balance FROM card WHERE number = (?)''',
                        (cur_user_card,))
        cur_user_acc_bal = get_con.fetchone()
        if user_ch == 1:
            print('Balance:', cur_user_acc_bal[0])
        elif user_ch == 2:
            to_add = int(input('Enter income:\n'))
            get_con.execute('''UPDATE card SET balance = balance + (?) WHERE number = (?)''',
                            (to_add, cur_user_card))
            conn.commit()
            print("Income was added")
        elif user_ch == 3:
            print("Transfer\n")
            crd_no = input("Enter card number:\n")
            if not check_luhn(crd_no):
                print("Probably you made a mistake in the card number. Please try again!")
                continue
            get_con.execute('''SELECT balance FROM card WHERE number = (?)''', (crd_no,))
            ex = get_con.fetchone()
            if ex is None:
                print("Such a card does not exist.")
                continue
            to_transfer = int(input("Enter how much money you want to transfer:\n"))
            if to_transfer > cur_user_acc_bal[0]:
                print("Not enough money!")
                continue
            get_con.execute('''UPDATE card SET balance = balance - (?) WHERE number = (?)''',
                            (to_transfer, cur_user_card))
            conn.commit()
            get_con.execute('''UPDATE card SET balance = balance + (?) WHERE number = (?)''',
                            (to_transfer, crd_no))
            conn.commit()
            print("Success!")
        elif user_ch == 4:
            get_con.execute('''DELETE FROM card WHERE number = (?)''', (cur_user_card,))
            conn.commit()
            print("The account has been closed!")
        elif user_ch == 5:
            print("Bye!")
            break
        else:
            return 2


def manage_db(insert_user):
    get_con.execute('''INSERT INTO card (number, pin)
                            VALUES (?, ?);''', (insert_user.card_no, insert_user.pin))
    conn.commit()


# all_users = []  # will temporarily store the all the user objects

# setting up the connection with the database
conn = sqlite3.connect('card.s3db')
conn.commit()

get_con = conn.cursor()  # cursor to manage the db
conn.commit()

get_con.execute('''CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY,
                                          number TEXT,
                                          pin TEXT,
                                          balance INTEGER DEFAULT 0);''')
conn.commit()


while True:
    choice = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    if choice == 1:
        new_user = User()
        new_user.generate_pin()
        print('Your card has been created')
        print(f'Your card number:\n{new_user.card_no}')
        print(f'Your card PIN:\n{new_user.pin}')

        # all_users.append(new_user)  # adding to the list of the users
        manage_db(new_user)  # to save the generated user in the database

    elif choice == 2:
        card_num = input("Enter your card number:\n")
        card_pin = input("Enter you PIN:\n")
        get_con.execute('''SELECT EXISTS(SELECT id FROM card WHERE number = (?))''', (card_num,))
        found = get_con.fetchone()
        get_con.execute('''SELECT pin FROM card WHERE number = (?)''', (card_num,))
        ch_pin = get_con.fetchone()
        ch = 0
        '''
        print('found =', found)
        print('ch_pin =', ch_pin)

        temp_cur = conn.execute(''SELECT number FROM card'')
        for row in temp_cur:
            print('ID           =', row[0])
            print('Card num     =', row[1])
            print('Card pin     =', row[2])
            print('Card balance =', row[3])
        '''
        if found is not None and ch_pin is not None:
            if ch_pin[0] == card_pin:
                ch = log_in(card_num, card_pin)
        if found is None or ch == 0:
            print("Wrong card number or PIN")
            continue
        if found and ch == 2:
            print('Bye!')
            break

    elif choice == 0:
        print('Bye!')
        break
