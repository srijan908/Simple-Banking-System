# Write your code here
import random
import sqlite3
from loggingin import log_in
from User import User


# inserting newly created cards to the database
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
