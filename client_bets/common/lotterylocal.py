import socket
import logging
from .protocol import send_bets, read_reply_to_bet


class LotteryLocal():
    def __init__(self, adress, clients, ip_server, port_server):
        self.address = adress
        self.clients = clients
        self.server = ip_server
        self.port = port_server
        self.socket = None
        self.open = True

    def send_clients(self):
        bets = []
        for client in self.clients:
            bet = client.get_bet(self.address)
            bets.append(bet)

        if not self.open:
            return
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server, self.port))
            send_bets(self.socket, bets)
            error = read_reply_to_bet(self.socket)
        except Exception as err:
            error = str(err)

        if error is None:
            log_text = "action: apuestas_enviadas | result: success"
            log_text += f" | amount: {len(bets)}"
        else:
            log_text = "action: apuestas_enviadas | result: fail"
            log_text += f" | error: {error}"

        logging.info(log_text)
        self.socket.close()

    def close_store(self):
        self.socket.close()
        self.open = False

