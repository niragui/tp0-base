from .socket import read_socket, read_int
import logging


class TLVReader():
    def __init__(self, attr_types):
        self.types = attr_types

    def read(self, socket):
        amount = read_int(socket)

        values_read = {}

        for i in range(amount):
            attr_type = read_socket(socket, 1)
            logging.debug(f"Type: {attr_type}")
            length = read_int(socket)
            logging.debug(f"Length: {length}")
            value = read_socket(socket, length).decode("utf-8")
            logging.debug(f"Value: {value}")
            attribute = self.types.get(attr_type, None)
            if attribute is None:
                raise Exception(f"{attr_type} Type Not A Valid Type")
            values_read.update({attribute: value})

        return values_read
