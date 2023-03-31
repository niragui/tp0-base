import socket
import json
import datetime
import logging

from .socket import read_socket, write_socket, read_int, send_int, int_to_bytes
from .tlv_reader import TLVReader
from .constants import *


class TLV():
    def __init__(self, type, value):
        self.type = type
        self.value = str(value)

    def to_bytes(self):
        bytes = b""
        bytes += self.type
        value_b = self.value.encode("utf-8")
        length = len(value_b)
        bytes += int_to_bytes(length)
        bytes += value_b
        logging.debug(f"Type: {self.type}")
        logging.debug(f"Length: {length}")
        logging.debug(f"Value: {self.value}")

        return bytes


class Bet:
    """ A lottery bet registry. """
    def __init__(self, agency: str, first_name: str, last_name: str, document: str, birthdate: str, number: str):
        """
        agency must be passed with integer format.
        birthdate must be passed with format: 'YYYY-MM-DD'.
        number must be passed with integer format.
        """
        self.agency = int(agency)
        self.first_name = first_name
        self.last_name = last_name
        self.document = document
        self.birthdate = datetime.date.fromisoformat(birthdate)
        self.number = int(number)

    def get_tlv_values(self):
        tlv_values = []
        for attribute, type in ATTRIBUTES_BET.items():
            value = getattr(self, attribute)
            tlv_value = TLV(type, value)
            tlv_values.append(tlv_value)
        return tlv_values

    def parse_bet(self):
        amount = len(vars(self))
        values = self.get_tlv_values()
        bytes = b""


        bytes += int_to_bytes(amount)

        for value in values:
            bytes += value.to_bytes()

        return bytes


def read_bet(socket_connected, reader):
    bet = reader.read(socket_connected)

    agency = bet.get(AGENCY_ATTRIBUTE)
    first_name = bet.get(NAME_ATTRIBUTE)
    last_name = bet.get(LAST_NAME_ATTRIBUTE)
    document = bet.get(DOCUMENT_ATTRIBUTE)
    birthdate = bet.get(DATE_ATTRIBUTE)
    number = bet.get(NUMBER_ATTRIBUTE)

    return Bet(agency, first_name, last_name, document, birthdate, number)


def read_bets(socket_connected):
    amount = read_int(socket_connected)

    reader = TLVReader(BET_TYPES)

    bets = []

    for i in range(amount):
        bet = read_bet(socket_connected, reader)
        bets.append(bet)

    return bets


def send_bet(socket_connected, bet):
    bytes = bet.parse_bet()
    write_socket(socket_connected, bytes)


def send_bets(socket_connected, bets):
    amount = len(bets)

    write_socket(socket_connected, BETS_BYTE)
    send_int(socket_connected, amount)
    for bet in bets:
        send_bet(socket_connected, bet)


def reply_to_bet(socket_connected, error):
    if error is None:
        write_socket(socket_connected, OK_BYTE)
    else:
        write_socket(socket_connected, ERROR_BYTE)
        error = error.encode("utf-8")
        length = len(error)
        send_int(socket_connected, length)
        write_socket(socket_connected, error)


def read_reply_to_bet(socket_connected):
    status_byte = read_socket(socket_connected, 1)

    if status_byte == OK_BYTE:
        return None
    else:
        length = read_int(socket_connected)
        error = read_socket(socket_connected, length).decode("utf-8")
        return error


def send_end(socket_connected):
    write_socket(socket_connected, END_BYTE)


def read_socket_server(socket_connected):
    case = read_socket(socket_connected, 1)

    if case == END_BYTE:
        return None
    elif case == BETS_BYTE:
        return read_bets(socket_connected)
    else:
        raise Exception(f"Type Byte {case} Is Not Valid")


def read_winners(socket_connected):
    amount = read_int(socket_connected)

    winners = json.loads(read_socket(socket_connected, amount))

    return winners


def send_winners(socket_connected, winners):
    winners_json = json.dumps(winners)

    winners_bytes = winners_json.encode("utf-8")

    length = len(winners_bytes)

    send_int(socket_connected, length)
    write_socket(socket_connected, winners_bytes)
