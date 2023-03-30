import socket
import logging
from threading import Thread
from .protocol import read_socket_server, reply_to_bet, send_winners
from .serverprotocol import handle_bets
from .utils import load_bets, has_won


class Server:
    def __init__(self, port, listen_backlog, agencies_to_check):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self.agencies = {}
        self.agencies_connected = 0
        self.agencies_loaded = 0
        self.agencies_waited = agencies_to_check
        self.is_awake = True

    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        threads = []

        while self.is_awake and self.agencies_connected < self.agencies_waited:
            client_sock = self.__accept_new_connection()
            self.agencies_connected += 1
            thread = Thread(target=self.__handle_client_connection, args=[client_sock])
            threads.append(thread)
            thread.run()
            if self.agencies_loaded >= self.agencies_waited:
                break

        if not self.is_awake:
            return

        for thread in threads:
            if thread.is_alive():
                thread.join()

        logging.info("action: sorteo | result: success")

        bets = load_bets()
        winners = {}
        for bet in bets:
            if has_won(bet):
                agency = bet.agency
                document = bet.document
                before = winners.get(agency, [])
                before.append(document)
                winners.update({agency: before})

        for agency, client_sock in self.agencies.items():
            winners_agency = winners.get(agency, [])
            send_winners(client_sock, winners_agency)
            client_sock.close()


    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """

        bets = []
        while bets is not None:
            try:
                bets = read_socket_server(client_sock)
                if bets is None:
                    self.agencies_loaded += 1
                    break
                agency = bets[0].agency
                self.agencies.update({agency: client_sock})
                handle_bets(bets)
                reply_to_bet(client_sock, None)
            except OSError as e:
                reply_to_bet(client_sock, f"{e}")
                logging.error("action: apuestas_almacenadas | result: fail | error: {e}")
                break

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        c, addr = self._server_socket.accept()
        logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
        return c

    def exit_gracefully(self):
        self.__del__()

    def __del__(self):
        self.is_awake = False
        self._server_socket.close()
