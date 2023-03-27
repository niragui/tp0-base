DOCKER_FILE = "docker-compose-dev.yaml"
HEADER = "header.txt"
FOOTER = "footer.txt"


def add_section(file_name, file):
    f_section = open(file_name, "r")

    for line in f_section:
        file.write(line)

    file.write("\n"*2)

    f_section.close()


def get_number(text):
    numero = input(text)

    while True:
        try:
            return int(numero)
        except:
            numero = input(text+" PLEASE INSERT A NUMBER ")


def add_clients(amount, file):
    for i in range(1, amount+1):
        file.write(f"  client{i}:\n")
        file.write(f"    container_name: client{i}\n")
        file.write("    image: client:latest\n")
        file.write("    entrypoint: /client\n")
        file.write("    environment:\n")
        file.write(f"      - CLI_ID={i}\n")
        file.write("      - CLI_LOG_LEVEL=DEBUG\n")
        file.write("    networks:\n")
        file.write("      - testing_net\n")
        file.write("    depends_on:\n")
        file.write("      - server\n")
        file.write("    volumes:\n")
        file.write("      - ./client/config.yaml:/config.yaml\n")
        file.write("\n"*2)


def main():
    amount = get_number("How Many Clients Would You Like To Add?")

    f = open(DOCKER_FILE, "w")
    add_section(HEADER, f)
    add_clients(amount, f)
    add_section(FOOTER, f)
    f.close()


if __name__ == "__main__":
    main()
