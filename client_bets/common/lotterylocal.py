import socket
import logging
from .clientprotocol import parse_bet, get_reply
from .protocol import send_bet, read_reply_to_bet


class LotteryLocal():
    def __init__(self, adress, clients, ip_server, port_server):
        self.address = adress
        self.clients = clients
        self.server = ip_server
        self.port = port_server
        self.socket = None
        self.open = True

    def send_clients(self):
        for client in self.clients:
            try:
                if not self.open:
                    break
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.server, self.port))
                bet = client.get_bet(self.address)
                send_bet(self.socket, bet)
                error = read_reply_to_bet(self.socket)
                dni = bet.document
                number = bet.number
            except Exception as err:
                error = str(err)

            if error is None:
                log_text = "action: apuesta_enviada | result: success"
                log_text += f" | dni: {dni} | numero: {number}"
            else:
                log_text = "action: apuesta_enviada | result: fail"
                log_text += f" | error: {error}"

            logging.info(log_text)
            self.socket.close()

    def close_store(self):
        self.socket.close()
        self.open = False

