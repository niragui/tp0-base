LENGTH_LENGTH = 4
OK_BYTE = "O".encode("latin-1")
ERROR_BYTE = "E".encode("latin-1")
END_BYTE = "F".encode("latin-1")
BETS_BYTE = "B".encode("latin-1")

BET_TYPES = {}

AGENCY_BYTE = "A".encode("latin-1")
AGENCY_ATTRIBUTE = "agency"
BET_TYPES.update({AGENCY_BYTE: AGENCY_ATTRIBUTE})

NAME_BYTE = "N".encode("latin-1")
NAME_ATTRIBUTE = "first_name"
BET_TYPES.update({NAME_BYTE: NAME_ATTRIBUTE})

LAST_NAME_BYTE = "L".encode("latin-1")
LAST_NAME_ATTRIBUTE = "last_name"
BET_TYPES.update({LAST_NAME_BYTE: LAST_NAME_ATTRIBUTE})

DOCUMENT_BYTE = "D".encode("latin-1")
DOCUMENT_ATTRIBUTE = "document"
BET_TYPES.update({DOCUMENT_BYTE: DOCUMENT_ATTRIBUTE})

DATE_BYTE = "I".encode("latin-1")
DATE_ATTRIBUTE = "birthdate"
BET_TYPES.update({DATE_BYTE: DATE_ATTRIBUTE})

NUMBER_BYTE = "U".encode("latin-1")
NUMBER_ATTRIBUTE = "number"
BET_TYPES.update({NUMBER_BYTE: NUMBER_ATTRIBUTE})


ATTRIBUTES_BET = {v: k for k, v in BET_TYPES.items()}


WINNER_BYTE = "W".encode("latin-1")
WINNER_ATTRIBUTE = "Winner"
WINNERS_TYPE = {WINNER_BYTE: WINNER_ATTRIBUTE}
