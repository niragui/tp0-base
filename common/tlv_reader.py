from .protocol import LENGTH_LENGTH, int_from_bytes
from .socket import read_socket


def read_int(socket):
    aux = read_socket(socket, LENGTH_LENGTH)
    return int_from_bytes(aux)


class TLVReader():
    def __init__(self, attr_types):
        self.types = attr_types

    def read(self, socket):
        amount = read_int(socket)

        values_read = {}

        for i in range(amount):
            attr_type = read_socket(socket, 1)
            length = read_int(socket)
            value = read_socket(socket, length)
            attribute = self.attr_type.get(attr_type, None)
            if attribute is None:
                raise Exception(f"{attr_type} Type Not A Valid Type")
            values_read.update({attribute: value})

        return values_read