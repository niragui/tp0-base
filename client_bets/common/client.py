from .protocol import Bet

class Client():
    def __init__(self, document, name, last_name, birthdate, number) -> None:
        self.document = document
        self.name = name
        self.last_name = last_name
        self.birthdate = birthdate
        self.number = number

    def get_bet(self, local_address):
        bet = Bet(local_address, self.name, self.last_name, self.document, self.birthdate, self.number)

        return bet
