import csv
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


def read_clients_from_csv(file):
    clients = []
    with open(file, 'r', encoding="latin-1") as file:
        reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            client = Client(row[2], row[0], row[1], row[3], row[4])
            clients.append(client)

    return clients
