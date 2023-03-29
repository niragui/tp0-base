import csv
import datetime
import time
from .protocol import Bet


""" Bets storage location. """
STORAGE_FILEPATH = "./bets.csv"
""" Simulated winner number in the lottery contest. """
LOTTERY_WINNER_NUMBER = 7574


def has_won(bet: Bet) -> bool:
    """ Checks whether a bet won the prize or not. """
    return bet.number == LOTTERY_WINNER_NUMBER


def store_bets(bets: list[Bet]) -> None:
    """
    Persist the information of each bet in the STORAGE_FILEPATH file.
    Not thread-safe/process-safe.
    """
    with open(STORAGE_FILEPATH, 'a+') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        for bet in bets:
            writer.writerow([bet.agency, bet.first_name, bet.last_name,
                             bet.document, bet.birthdate, bet.number])


def load_bets() -> list[Bet]:
    """
    Loads the information all the bets in the STORAGE_FILEPATH file.
    Not thread-safe/process-safe.
    """
    with open(STORAGE_FILEPATH, 'r') as file:
        reader = csv.reader(file, quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            yield Bet(row[0], row[1], row[2], row[3], row[4], row[5])

