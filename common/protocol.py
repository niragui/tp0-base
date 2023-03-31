import socket
import json
import datetime

from .socket import read_socket, write_socket
from .tlv_reader import TLVReader

LENGTH_LENGTH = 4
OK_BYTE = "O".encode("utf-8")
ERROR_BYTE = "E".encode("utf-8")
END_BYTE = "F".encode("utf-8")
BETS_BYTE = "B".encode("utf-8")

BET_TYPES = {}

AGENCY_BYTE = "A".encode("utf-8")
AGENCY_ATTRIBUTE = "agency"
BET_TYPES.update({AGENCY_BYTE: AGENCY_ATTRIBUTE})

NAME_BYTE = "N".encode("utf-8")
NAME_ATTRIBUTE = "first_name"
BET_TYPES.update({NAME_BYTE: NAME_ATTRIBUTE})

LAST_NAME_BYTE = "L".encode("utf-8")
LAST_NAME_ATTRIBUTE = "last_name"
BET_TYPES.update({LAST_NAME_BYTE: LAST_NAME_ATTRIBUTE})

DOCUMENT_BYTE = "D".encode("utf-8")
DOCUMENT_ATTRIBUTE = "document"
BET_TYPES.update({DOCUMENT_BYTE: DOCUMENT_ATTRIBUTE})

DATE_BYTE = "I".encode("utf-8")
DATE_ATTRIBUTE = "birthdate"
BET_TYPES.update({DATE_BYTE: DATE_ATTRIBUTE})

NUMBER_BYTE = "U".encode("utf-8")
NUMBER_ATTRIBUTE = "number"
BET_TYPES.update({NUMBER_BYTE: NUMBER_ATTRIBUTE})

ATTRIBUTES_BET = {v: k for k, v in BET_TYPES.items()}


class TLV():
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def to_bytes(self):
        bytes = b""
        bytes += self.type
        value_b = self.value.encode("utf-8")
        length = len(value_b)
        bytes += int_to_bytes(length)
        bytes += value_b

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

    def parse_bet(self):
        tlv_values = []
        for attribute, type in ATTRIBUTES_BET.items():
            value = getattr(self, attribute)
            tlv_value = TLV(type, value)
            tlv_values.append(tlv_value)
        return tlv_value


def int_to_bytes(x: int, length: int = LENGTH_LENGTH) -> bytes:
    return x.to_bytes(length, 'big')

 
def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


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
    amount = int_from_bytes(read_socket(socket_connected, LENGTH_LENGTH))

    reader = TLVReader(BET_TYPES)

    bets = []

    for i in range(amount):
        bet = read_bet(socket_connected, reader)
        bets.append(bet)

    return bets


def send_bet(socket_connected, bet):
    amount = len(vars(bet))

    values = bet.parse_bet()
    bytes = b""

    for value in values:
        bytes += value.to_bytes()

    write_socket(socket_connected, int_to_bytes(amount))
    write_socket(socket_connected, bytes)


def send_bets(socket_connected, bets):
    amount = len(bets)

    write_socket(socket_connected, BETS_BYTE)
    write_socket(socket_connected, int_to_bytes(amount))
    for bet in bets:
        send_bet(socket_connected, bet)


def reply_to_bet(socket_connected, error):
    if error is None:
        write_socket(socket_connected, OK_BYTE)
    else:
        write_socket(socket_connected, ERROR_BYTE)
        error = error.encode("utf-8")
        length = len(error)
        write_socket(socket_connected, int_to_bytes(length))
        write_socket(socket_connected, error)


def read_reply_to_bet(socket_connected):
    status_byte = read_socket(socket_connected, 1)

    if status_byte == OK_BYTE:
        return None
    else:
        length = int_from_bytes(read_socket(socket_connected, LENGTH_LENGTH))
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
    amount = int_from_bytes(read_socket(socket_connected, LENGTH_LENGTH))

    winners = json.loads(read_socket(socket_connected, amount))

    return winners


def send_winners(socket_connected, winners):
    winners_json = json.dumps(winners)

    winners_bytes = winners_json.encode("utf-8")

    length = len(winners_bytes)

    write_socket(socket_connected, int_to_bytes(length))
    write_socket(socket_connected, winners_bytes)
