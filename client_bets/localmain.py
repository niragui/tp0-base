#!/usr/bin/env python3

from configparser import ConfigParser
import logging
import os
import json
import signal
from .client import Client
from .lotterylocal import LotteryLocal


def initialize_config():
    """
    Parse env variables or config file to find program config params

    Function that search and parse program configuration parameters in the
    program environment variables first and the in a config file.
    If at least one of the config parameters is not found a KeyError exception
    is thrown. If a parameter could not be parsed, a ValueError is thrown.

    If parsing succeeded, the function returns a ConfigParser object
    with config parameters
    """

    config = ConfigParser(os.environ)
    # If config.ini does not exists original config object is not modified
    config.read("config.ini")

    config_params = {}
    try:
        config_params["ip"] = os.getenv('SERVER_ADDRESS', config["SERVER"]["IP"])
        config_params["port"] = os.getenv('SERVER_ADDRESS', config["SERVER"]["PORT"])
        config_params["adress"] = os.getenv('LOCAL_ADRESS', config["LOCAL"]["ADDRESS"])
        config_params["documents"] = json.loads(os.getenv('CLIENTS_DOCUMENTS', config["CLIENTS"]["DOCUMENTS"]))
        config_params["names"] = json.loads(os.getenv('CLIENTS_NAMES', config["CLIENTS"]["NAMES"]))
        config_params["last_names"] = json.loads(os.getenv('CLIENTS_LAST_NAMES', config["CLIENTS"]["LAST_NAMES"]))
        config_params["birthdates"] = json.loads(os.getenv('BIRTHDATES', config["CLIENTS"]["BIRTHDATES"]))
        config_params["numbers"] = json.loads(os.getenv('NUMBERS', config["CLIENTS"]["NUMBERS"]))
        config_params["logging"] = json.loads(os.getenv('LEVEL', config["LOGGING"]["LEVEL"]))
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    return config_params


def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )


def main():
    params = initialize_config()

    logging_level = params["logging"]

    initialize_log(logging_level)

    clients = []

    names = params.get("names")
    last_names = params.get("last_names")
    birthdates = params.get("birthdates")
    numbers = params.get("numbers")

    for i in range(len(names)):
        name = names[i]
        last_name = last_names[i]
        birthdate = birthdates[i]
        number = numbers[i]

        client = Client(name, last_name, birthdate, number)
        clients.append(client)

    local_id = params.get("adress")
    ip = params.get("ip")
    port = params.get("port")

    local = LotteryLocal(local_id, clients, ip, port)
    signal.signal(signal.SIGINT, local.exit_gracefully)

    local.send_clients()

    local.close_store()


if __name__ == "__main__":
    main()
