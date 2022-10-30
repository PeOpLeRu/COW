import numpy as np

class Cow:
    def __init__(self, mem_size = 30) -> None:
        self.mem_size = mem_size
        self.memory = np.zeros((self.mem_size), dtype='uint8')
        self.pointer = 0

        self.register = None

    def inc_ptr(self):
        self.pointer += 1

    def dec_ptr(self):
        self.pointer -= 1

    def get_cell_value(self):
        return self.memory[self.pointer]

    def set_cell_value(self, value):
        self.memory[self.pointer] = value

    def inc_cell_value(self):
        self.memory[self.pointer] += 1

    def dec_cell_value(self):
        self.memory[self.pointer] -= 1

    def init_cell_zero(self):
        self.memory[self.pointer] = 0