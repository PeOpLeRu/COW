from .lexer import *
from .token import *
from .cow import *

class InterpreterException:
    ...

class Interpreter:
    def __init__(self) -> None:
        self.cow = Cow()
        self.lexer = Lexer()
        self.commands = ["moo", "mOo", "moO", "mOO", "Moo", "MOo", "MoO", "MOO", "OOO", "MMM", "OOM", "oom"]
        self.data = None
        self.end_data = False

    def str_to_index(self, str):
        try:
            instruction_index = self.commands.index(str)
        except Exception as e:
            print(f"Undefined operator -> {str}")

        return instruction_index

    def __get_token(self, desired : TokenType = None):
        while True:
            token = self.lexer.current_token
            if token.type == TokenType.EOL or token.type == TokenType.COMMENT:
                if len(self.data) <= 0:
                    self.end_data = True
                    break
                self.lexer.init_lexer(self.data[0])
                self.data.pop(0)
            else:
                self.lexer.next()

            if desired != None and token.type != desired:
                continue
            else:
                break

        return token

    def exec(self, name_file):
        file = open(name_file)
        self.data = file.readlines()
        self.lexer.init_lexer(self.data[0])
        self.data.pop(0)
        self.end_data = False
        file.close()

        while not self.end_data:
            token = self.__get_token()
            if token.type == TokenType.COMMENT or token.type == TokenType.EOL:
                continue
            elif token.type == TokenType.OPERATOR:
                instruction_index = self.str_to_index(token.value)

                if instruction_index == 7:
                    self.__loop_handler()
                else:
                    self.__handler(instruction_index)

        self.data = None

    def __handler(self, instr_index):
        match instr_index:
            case 1:
                self.cow.dec_ptr()
            case 2:
                self.cow.inc_ptr()
            case 3:
                value = self.cow.get_cell_value()
                if value == 3 or value > 11:
                    raise InterpreterException("Invalid value in cell for operator mOO")
                else:
                    self.__handler(value)
            case 4:
                value = self.cow.get_cell_value()
                if value == 0:
                    char = input("Enter char: ")
                    self.cow.set_cell_value(ord(char))
                else:
                    print(chr(value))
            case 5:
                self.cow.dec_cell_value()
            case 6:
                self.cow.inc_cell_value()
            case 8:
                self.cow.init_cell_zero()
            case 9:
                if self.cow.register == None:
                    self.cow.register = self.cow.get_cell_value()
                else:
                    self.cow.set_cell_value(self.cow.register)
                    self.cow.register = None
            case 10:
                print(f"Value in cell: {self.cow.get_cell_value()}")
            case 11:
                self.cow.set_cell_value(int(input("Enter number for cell: ")))
            case _:
                raise InterpreterException(f"Loop error with operator -> {self.commands[instr_index]}")

    def __loop_handler(self):
        instr_index = 7
        code_memory = [instr_index]

        iterator = None
        iterator_stack = []

        level = 0
        MOO_stack = [0]
        oom_stack = []

        is_returned = False
        need_move_iterator = False

        while len(MOO_stack) > 0:
            if iterator == None:
                token = self.__get_token(desired=TokenType.OPERATOR)
                instr_index = self.str_to_index(token.value)
                code_memory += [instr_index]
            else:
                if iterator + 1 >= len(code_memory):
                    iterator = None
                    continue
                if need_move_iterator:
                    iterator += 1
                instr_index = code_memory[iterator]

            if instr_index == 0:
                if len(MOO_stack) != len(oom_stack):
                    oom_stack += [len(code_memory) - 1]
                iterator = MOO_stack[level]
                is_returned = True
                need_move_iterator = False
            elif instr_index == 7:
                if is_returned:
                    if self.cow.get_cell_value() == 0:
                        level -= 1
                        MOO_stack.pop()
                        iterator = oom_stack.pop()
                else:
                    level += 1
                    MOO_stack += [len(code_memory) - 1]
                is_returned = False
                need_move_iterator = True
            else:
                self.__handler(instr_index)