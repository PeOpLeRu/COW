from enum import Enum, auto

class TokenType(Enum):
    OPERATOR = auto(),
    COMMENT = auto(),
    EOL = auto()

class Token:
    def __init__(self, type : TokenType, value : str) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f"Type -> {self.token_type}; Value -> {self.value}"