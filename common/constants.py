LENGTH_LENGTH = 4
OK_BYTE = "O".encode("utf-8")
ERROR_BYTE = "E".encode("utf-8")
END_BYTE = "F".encode("utf-8")
BETS_BYTE = "B".encode("utf-8")

BET_TYPES = {}

AGENCY_BYTE = "A".encode("utf-8")
AGENCY_ATTRIBUTE = "agency"
BET_TYPES.update({AGENCY_BYTE: AGENCY_ATTRIBUTE})

NAME_BYTE = "N".encode("utf-8")
NAME_ATTRIBUTE = "first_name"
BET_TYPES.update({NAME_BYTE: NAME_ATTRIBUTE})

LAST_NAME_BYTE = "L".encode("utf-8")
LAST_NAME_ATTRIBUTE = "last_name"
BET_TYPES.update({LAST_NAME_BYTE: LAST_NAME_ATTRIBUTE})

DOCUMENT_BYTE = "D".encode("utf-8")
DOCUMENT_ATTRIBUTE = "document"
BET_TYPES.update({DOCUMENT_BYTE: DOCUMENT_ATTRIBUTE})

DATE_BYTE = "I".encode("utf-8")
DATE_ATTRIBUTE = "birthdate"
BET_TYPES.update({DATE_BYTE: DATE_ATTRIBUTE})

NUMBER_BYTE = "U".encode("utf-8")
NUMBER_ATTRIBUTE = "number"
BET_TYPES.update({NUMBER_BYTE: NUMBER_ATTRIBUTE})


ATTRIBUTES_BET = {v: k for k, v in BET_TYPES.items()}