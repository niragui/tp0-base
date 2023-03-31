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
        value_b = self.value.encode("latin-1")
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


def send_bet(socket_connected, bet):
    bytes = bet.parse_bet()
    write_socket(socket_connected, bytes)


def reply_to_bet(socket_connected, error):
    if error is None:
        write_socket(socket_connected, OK_BYTE)
    else:
        write_socket(socket_connected, ERROR_BYTE)
        error = error.encode("latin-1")
        length = len(error)
        send_int(socket_connected, length)
        write_socket(socket_connected, error)


def read_reply_to_bet(socket_connected):
    status_byte = read_socket(socket_connected, 1)

    if status_byte == OK_BYTE:
        return None
    else:
        length = read_int(socket_connected)
        error = read_socket(socket_connected, length).decode("latin-1")
        return error
