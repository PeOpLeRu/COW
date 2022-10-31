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
        self.data = None   # Список строк кода из файла
        self.end_data = False

    def str_to_index(self, str):    # Соотносит название инструкции с ее номером
        try:
            instruction_index = self.commands.index(str)
        except Exception as e:
            print(f"Undefined operator -> {str}")

        return instruction_index

    def __init_data(self, name_file):   # Считывание данных с файла, подготовка лексера
        file = open(name_file)
        self.data = file.readlines()
        
        self.lexer.init_lexer(self.data[0])
        self.data.pop(0)
        self.end_data = False
        
        file.close()

    def __get_token(self, desired : TokenType = None):  # Достает очередной токен
        while True:
            token = self.lexer.get_current()
            if token.type == TokenType.EOL or token.type == TokenType.COMMENT:  # Надо доставать новую строку кода
                if len(self.data) <= 0:  # Если кончились данные с файла (код)
                    self.end_data = True  # Флаг
                    self.data = None  # Сброс данных
                    break
                self.lexer.init_lexer(self.data[0])  # Инициализируем лексер новой строкой данных
                self.data.pop(0)  # Извлекаем эту строку из данных
            else:  # Иначе просто сдвигаем на следующий токен
                self.lexer.next()

            if desired != None and token.type != desired:  # Если задан тип требуемого токена и найденный ему не соответсвует, то продолжаем
                continue
            else:
                break

        return token

    def exec(self, name_file):
        self.__init_data(name_file)

        while not self.end_data:    # Пока данные не кончились
            token = self.__get_token()
            if token.type == TokenType.COMMENT or token.type == TokenType.EOL:
                continue
            elif token.type == TokenType.OPERATOR:
                instruction_index = self.str_to_index(token.value)

                if instruction_index == 7:  # Если цикл, то специальный обработчик (отслеживаем по команде MOO)
                    self.__loop_handler()
                else:
                    self.__handler(instruction_index)  # Иначе просто выполняем "простую" инструкцию

    def __handler(self, instr_index):  # Обработчик "простых" инструкций
        match instr_index:  # Обработка всех инструкций, кроме 0 (moo) и 7 (MOO)
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
                    print(chr(value), end="")
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
                raise InterpreterException(f"Runtime error (from __handler()) with operator -> {self.commands[instr_index]}")

    def __loop_handler(self):  # Обработчик "сложных" инструкций -> 0 (moo) и 7 (MOO)
        instr_index = 7  # Первая инструкция при входе всегда - 7 -> MOO (начало цикла)
        code_memory = [instr_index]  # Здесь хранится история инструкций

        iterator = None  # IP -> Указатель на текущую инструкцию (ее номер)

        level = 0  # Вложенность цикла
        MOO_stack = [0]  # Точки начала цикла
        moo_stack = []  # Точки конца цикла

        is_returned = False  # Если True, то точка входа уже встречалась (цикл будет выполнятся снова)

        skip = False  # Если видим цикл первый раз раз и в него не заходим (условие ложно) - то скипаем его инструкции до инструкции moo
        skip_inner_loops_counter = 0  # Если скипаем инструкции и встречаем другие циклы -> то и их скипаем (подсчет уровней вложенности -> чтобы выйти по нужной moo)

        if self.cow.get_cell_value() == 0:  # Если цикл выполнять не надо
            MOO_stack = []  # Точки начала цикла
            skip = True

        need_move_iterator = False

        while len(MOO_stack) > 0 or skip:
            if iterator == None:  # Итератор пуст - читаем инструкции с файла
                token = self.__get_token(desired=TokenType.OPERATOR)
                instr_index = self.str_to_index(token.value)
                code_memory += [instr_index]  # Добавляем в память
            else:  # Иначе берем с памяти по итератору
                if need_move_iterator and iterator + 1 >= len(code_memory):  # Если нужно сдвигуть итератор, и уже кончилась память
                    iterator = None  # То убираем итератор и будем читать инструкции с файла
                    continue
                if need_move_iterator:  # Двигаем итератор
                    iterator += 1
                instr_index = code_memory[iterator]  # берем инструкцию с памяти по итератору

            if skip:
                if instr_index == 7:  # Если встретили MOO - игнорим вложенный цикл
                    skip_inner_loops_counter += 1
                elif instr_index == 0 and skip_inner_loops_counter > 0:  # Если встретили moo и были вложенные циклы - снижаем уровень вложенности
                    skip_inner_loops_counter -= 1
                elif instr_index == 0 and skip_inner_loops_counter == 0:  # Если встретили moo и не было вложенных циклов - выходим
                    skip = False
                continue

            if instr_index == 0:  # Если moo
                if iterator != None and iterator not in moo_stack:
                    moo_stack += [iterator]
                elif iterator == None and len(code_memory) - 1 not in moo_stack:
                    moo_stack += [len(code_memory) - 1]
                iterator = MOO_stack[level]
                is_returned = True
                need_move_iterator = False
            elif instr_index == 7:  # Если MOO
                if is_returned: # Если здесь уже были
                    if self.cow.get_cell_value() == 0:
                        level -= 1
                        MOO_stack.pop()
                        iterator = moo_stack.pop()
                else: # Если встретили первый раз
                    if self.cow.get_cell_value() == 0:
                        skip = True # Условие выхода истинно - пропускаем инструкции до первой moo и идем дальше
                    else:
                        level += 1
                        if iterator != None: # Заносим адрес инструкции в стэк (для прыжков к ней в дальнейшем)
                            MOO_stack += [iterator]
                        else:
                            MOO_stack += [len(code_memory) - 1]
                is_returned = False # Сброс флага
                need_move_iterator = True
            else:  # Если "простая" инструкция
                self.__handler(instr_index)