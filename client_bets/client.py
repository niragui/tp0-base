
class client():
    def __init__(self, document, name, last_name, birthdate, number) -> None:
        self.document = document
        self.name = name
        self.last_name = last_name
        self.birthdate = birthdate
        self.number = number

    def get_bet(self):
        bet = {}
        bet.update({"DNI": self.document})
        bet.update({"Nombre": self.name})
        bet.update({"Apellido": self.last_name})
        bet.update({"Nacimiento": self.birthdate})
        bet.update({"Apuesta": self.number})

        return bet
