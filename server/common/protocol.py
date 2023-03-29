import json
import logging
from .utils import Bet, store_bets

def handle_bet_msg(msg):
    bet = json.loads(msg)

    dni = bet.get("DNI")
    number = bet.get("Apuesta")
    try:
        agency = bet.get("Local ID")
        name = bet.get("Nombre")
        last_name = bet.get("Apellido")
        birthdate = bet.get("Nacimiento")

        bet = Bet(agency, name, last_name, dni, birthdate, number)
        bets = [bet]
        store_bets(bets)

        logging.info(f"action: apuesta_almacenada | result: success | dni: {dni} | numero: {number}")
    except Exception as err:
        logging.info(f"action: apuesta_almacenada | result: fail | dni: {dni} | numero: {number} | Error: {err}")
