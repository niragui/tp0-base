import json


def parse_bet(bet, local):
    bet.update({"Local ID": local})

    return json.dumps(bet)


def get_reply(socket):
    try:
        data = socket.recv(1024).decode()
        if data == "Ok":
            return None
        else:
            return data
    except Exception as err:
        return str(err)
