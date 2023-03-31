MAX_SIZE = 8000


def read_socket(socket_connected, bytes):
    buffer = b""
    while len(buffer) < bytes:
        missing = bytes - len(buffer)
        if missing > MAX_SIZE:
            missing = MAX_SIZE
        aux = socket_connected.recv(missing)
        buffer += aux

    return aux


def write_socket(socket_connected, bytes):
    sent = 0

    while sent < len(bytes):
        end = len(bytes) - sent
        if end - sent > MAX_SIZE:
            end = sent + MAX_SIZE
        aux = socket_connected.send(bytes[sent:end])
        sent += aux

    return aux
