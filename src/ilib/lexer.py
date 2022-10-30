from .token import *

class LexerException(Exception):
    ...

class Lexer:
    def __init__(self) -> None:
        self.data = ""
        self.current_token : Token = None
        self.iterator = 0

    def init_lexer(self, data : str) -> None:
        self.data = data
        self.current_token : Token = None
        self.iterator = 0   # Итератор сразу указывает на начало следующего токена
        self.next() # Иниализируем первый токен

    def get_current(self):  # Получить текущий токен
        return self.current_token

    def next(self): # Сдвиг на следующий токен
        self.__forward()

        return self.current_token

    def __forward(self):
        while self.iterator < len(self.data):
            if self.data[self.iterator] in [' ', '\t', '\n']:
                self.__skip()
                continue
            else:
                word = self.__get_word()
                if len(word) >= 2 and word[0] == '/' and word[1] == '/':
                    self.current_token = Token(TokenType.COMMENT, word)
                    return
                elif len(word) == 3:
                    self.current_token = Token(TokenType.OPERATOR, word)
                    return
                else:
                    raise LexerException(f"Invalid token ({word})")

        self.current_token = Token(TokenType.EOL, "")
        return

    def __skip(self):
        while self.iterator < len(self.data) and self.data[self.iterator] in [' ', '\t', '\n']:
            self.iterator += 1

    def __get_word(self) -> str:
        res : str = ""

        while self.iterator < len(self.data) and self.data[self.iterator] not in [' ', '\t', '\n']:
            res += self.data[self.iterator]
            self.iterator += 1
        
        return res