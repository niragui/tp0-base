import socket
import json
import datetime

LENGTH_LENGTH = 4
OK_BYTE = "O".encode("utf-8")
ERROR_BYTE = "N".encode("utf-8")
MAX_SIZE = 8000


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


def int_to_bytes(x: int, length: int = LENGTH_LENGTH) -> bytes:
    return x.to_bytes(length, 'big')

 
def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def read_socket(socket_connected, bytes):
    buffer = b""
    while len(buffer) < bytes:
        missing = bytes - len(buffer)
        aux = socket_connected.recv(missing)
        buffer += aux

    return aux


def read_bet(socket_connected):
    length = int_from_bytes(read_socket(socket_connected, LENGTH_LENGTH))

    bet = read_socket(socket_connected, length).decode('utf-8')

    bet = json.loads(bet)

    agency = bet.get("agency")
    first_name = bet.get("first_name")
    last_name = bet.get("last_name")
    document = bet.get("document")
    birthdate = bet.get("birthdate")
    number = bet.get("number")

    return Bet(agency, first_name, last_name, document, birthdate, number)


def write_socket(socket_connected, bytes):
    sent = 0

    while sent < len(bytes):
        end = len(bytes) - sent
        if end - sent > MAX_SIZE:
            end = sent + MAX_SIZE
        aux = socket_connected.send(bytes[sent:end])
        sent += aux

    return aux


def send_bet(socket_connected, bet):
    bet_dic = vars(bet)

    for key, value in bet_dic.items():
        bet_dic.update({key: str(value)})

    bet_text = json.dumps(bet_dic).encode("utf-8")

    length = len(bet_text)

    write_socket(socket_connected, int_to_bytes(length))
    write_socket(socket_connected, bet_text)


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
