import random
from luhn_algorithm import generate


# Class user which be used to create a new verified user for our database
class User:
    num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # will be used to generate card number and pin

    def __init__(self):
        self.card_no = "400000"  # initializing the card number with 400000
        self.pin = ''
        self.balance = 0

    def generate_pin(self):
        # completing the card number
        while len(self.card_no) < 15:
            self.card_no += random.choice(User.num)

        # generating the pin for the card
        while len(self.pin) < 4:
            self.pin += random.choice(User.num)

        # validating the card number using luhn algorithm
        self.card_no = generate(self.card_no)
