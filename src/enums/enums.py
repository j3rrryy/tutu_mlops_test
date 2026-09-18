from enum import Enum


class Prepayment(str, Enum):
    CARD = "card"
    CASH = "cash"
    SBP = "sbp"
