from enum import Enum

class OrderStatus(Enum):
    PENDING = "PENDING"
    FILLED = "FILLED"
    PARTIAL = "PARTIAL"

class OrderType(Enum):
    SELLING = "SELLING"
    BUYING = "BUYING"

class OrderKind(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"