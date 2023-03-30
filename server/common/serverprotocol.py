import logging
from .utils import store_bets
from .protocol import Bet

def handle_bets(bets):
    try:
        store_bets(bets)

        logging.info(f"action: apuestas_almacenadas | result: success | amount: {len(bets)}")
    except Exception as err:
        logging.error(f"action: apuesta_almacenada | result: fail | error: {err}")
