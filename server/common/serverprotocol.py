import logging
from .utils import store_bets
from .protocol import Bet

def handle_bet(bet):
    dni = bet.document
    number = bet.number
    try:
        bets = [bet]
        store_bets(bets)

        logging.info(f"action: apuesta_almacenada | result: success | dni: {dni} | numero: {number}")
    except Exception as err:
        logging.info(f"action: apuesta_almacenada | result: fail | dni: {dni} | numero: {number} | Error: {err}")
