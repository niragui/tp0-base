#!/usr/bin/env python3

from configparser import ConfigParser
import logging
import os
import json
import signal
from threading import Thread
from common.lotterylocal import LotteryLocal
from common.client import Client, read_clients_from_csv


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
        config_params["port"] = int(os.getenv('SERVER_ADDRESS', config["SERVER"]["PORT"]))
        config_params["adress"] = int(os.getenv('LOCAL_ADRESS', config["LOCAL"]["ADDRESS"]))
        config_params["documents"] = json.loads(os.getenv('CLIENTS_DOCUMENTS', config["CLIENTS"]["DOCUMENTS"]))
        config_params["names"] = json.loads(os.getenv('CLIENTS_NAMES', config["CLIENTS"]["NAMES"]))
        config_params["last_names"] = json.loads(os.getenv('CLIENTS_LAST_NAMES', config["CLIENTS"]["LAST_NAMES"]))
        config_params["birthdates"] = json.loads(os.getenv('BIRTHDATES', config["CLIENTS"]["BIRTHDATES"]))
        config_params["numbers"] = json.loads(os.getenv('NUMBERS', config["CLIENTS"]["NUMBERS"]))
        config_params["logging"] = os.getenv('LEVEL', config["LOGGING"]["LEVEL"])
        config_params["files"] = json.loads(os.getenv('FILES', config["FILES"]["LOCATIONS"]))
        config_params["mode"] = json.loads(os.getenv('MODE', config["MODE"]["MODE"]))
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


def get_local(params):
    clients = []

    documents = params.get("documents")
    names = params.get("names")
    last_names = params.get("last_names")
    birthdates = params.get("birthdates")
    numbers = params.get("numbers")

    for i in range(len(documents)):
        document = documents[i]
        name = names[i]
        last_name = last_names[i]
        birthdate = birthdates[i]
        number = numbers[i]

        client = Client(document, name, last_name, birthdate, number)
        clients.append(client)

    local_id = params.get("adress")
    ip = params.get("ip")
    port = params.get("port")

    local = LotteryLocal(local_id, clients, ip, port)

    return local


def get_locals(params):
    locals = []

    files = params.get("files")
    ip = params.get("ip")
    port = params.get("port")

    for i, file in enumerate(files):
        clients = read_clients_from_csv(file)
        local = LotteryLocal(i+1, clients, ip, port)
        locals.append(local)

    return locals


def main():
    params = initialize_config()

    logging_level = params["logging"]
    initialize_log(logging_level)

    mode = params.get("mode")

    if mode == "Multiple":
        locals = get_locals(params)
    else:
        local = get_local(params)
        locals = [local]

    threads = []

    for local in locals:
        signal.signal(signal.SIGINT, local.close_store)
        thread = Thread(target=local.send_clients)
        thread.run()
        threads.append(thread)

    for thread in threads:
        thread.join()

    for local in locals:
        local.get_winners()
        local.close_store()


if __name__ == "__main__":
    main()
