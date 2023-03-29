import socket
import logging
from .protocol import parse_bet, get_reply


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
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.server, self.port))
                if not self.open:
                    break
                bet = client.get_bet()
                bet_report = parse_bet(bet, self.address)
                self.socket.sendall(bet_report.encode())
                dni = bet.get("DNI")
                apuesta = bet.get("Apuesta")
                error = get_reply(self.socket)
            except Exception as err:
                error = str(err)

            if error is None:
                log_text = "action: apuesta_enviada | result: success"
                log_text += f" | dni: {dni} | numero: {apuesta}"
            else:
                log_text = "action: apuesta_enviada | result: fail"
                log_text += f" | error: {error}"

            logging.info(log_text)
            self.socket.close()

    def close_store(self):
        self.socket.close()
        self.open = False

