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
            length = read_int(socket)
            value = read_socket(socket, length).decode("latin-1")
            if len(value) != length:
                raise Exception("Short Read Element")
            attribute = self.types.get(attr_type, None)
            if attribute is None:
                raise Exception(f"{attr_type} Type Not A Valid Type")
            values_read.update({attribute: value})

        return values_read
