import sqlite3
from luhn_algorithm import check_luhn

conn = sqlite3.connect('card.s3db')
conn.commit()

get_con = conn.cursor()  # cursor to manage the db
conn.commit()


# the user interface when if the credentials are present in the database
def log_in(cur_user_card, cur_user_pin):
    print("You have successfully logged in!")
    while True:
        user_ch = int(input("1. Balance\n2. Add income\n3. Do transfer"
                            "\n4. Close account\n5. Log out\n0. Exit\n"))

        # retrieving the current user's account balance for ease of access
        get_con.execute('''SELECT balance FROM card WHERE number = (?)''',
                        (cur_user_card,))
        cur_user_acc_bal = get_con.fetchone()

        # if the user presses 1
        if user_ch == 1:
            print('Balance:', cur_user_acc_bal[0])

        # if the user presses 2
        elif user_ch == 2:
            to_add = int(input('Enter income:\n'))
            get_con.execute('''UPDATE card SET balance = balance + (?) WHERE number = (?)''',
                            (to_add, cur_user_card))
            conn.commit()
            print("Income was added")

        # if the user presses 3
        elif user_ch == 3:
            print("Transfer\n")
            # testing the validity of the entered card number
            crd_no = input("Enter card number:\n")
            if not check_luhn(crd_no):
                print("Probably you made a mistake in the card number. Please try again!")
                continue

            # testing if the valid card number has actually been assigned to someone
            get_con.execute('''SELECT balance FROM card WHERE number = (?)''', (crd_no,))
            ex = get_con.fetchone()
            if ex is None:
                print("Such a card does not exist.")
                continue

            # checking if the entered amount is available in the account
            to_transfer = int(input("Enter how much money you want to transfer:\n"))
            if to_transfer > cur_user_acc_bal[0]:
                print("Not enough money!")
                continue

            # transferring the entered amount
            get_con.execute('''UPDATE card SET balance = balance - (?) WHERE number = (?)''',
                            (to_transfer, cur_user_card))
            conn.commit()
            get_con.execute('''UPDATE card SET balance = balance + (?) WHERE number = (?)''',
                            (to_transfer, crd_no))
            conn.commit()
            print("Success!")

        # if the user presses 4
        elif user_ch == 4:
            get_con.execute('''DELETE FROM card WHERE number = (?)''', (cur_user_card,))
            conn.commit()
            print("The account has been closed!")

        # if the user presses 5
        elif user_ch == 5:
            print("Bye!")
            break

        # if user decides to quit
        else:
            return 2