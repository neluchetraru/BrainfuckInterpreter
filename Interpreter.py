from typing import Any
import re


class Memory(object):
    def __init__(self, size=10) -> None:
        self.size = size
        self.memory = [0] * self.size
        self.limit = 300

    def get_memory(self) -> list:
        return self.memory

    def get_size(self) -> int:
        return self.size

    def print_at_pointer(self, pointer: int) -> None:
        char = chr(int(str(self.memory[pointer])))
        print(char, end="", flush=True)
        return char

    def add_at_pointer(self, pointer: int, amount: int) -> None:
        if len(self.memory) - 1 < pointer:
            self.memory += [0] * (pointer - len(self.memory) + 1)
        self.memory[pointer] = (self.memory[pointer] + amount) % 256
        if self.memory[pointer] > self.limit:
            raise Exception("Memory limit exceeded.")
        return self.memory[pointer]

    def get_value_at(self, pointer: int) -> int:
        if len(self.memory) - 1 < pointer:
            self.memory += [0] * (pointer - len(self.memory) + 1)
        return self.memory[pointer]

    def reset(self) -> None:
        self.memory = [0] * self.size


class Interpreter(object):
    def __init__(self, memory) -> None:
        self.memory = memory
        self.data_pointer = 0
        self.pc = 0
        self.stack = []
        self.input_pointer = 0

    def get_input(self) -> Any:
        try:
            data = self.inputter.get("1.0", "end-1c").strip().split(" ")
            if data == [""]:
                data = []
        except:
            data = []
        print(data)
        if self.input_pointer >= len(data):
            raise Exception("Input limit exceeded.")
        else:
            self.input_pointer += 1
            return ord(data[self.input_pointer - 1])

    def output(self, arg) -> str:
        self.printer.insert("end", arg)

    def run(self, code: str, printer, inputter) -> None:
        self.printer = printer
        self.inputter = inputter
        while self.pc < len(code):
            if code[self.pc] == ">":
                self.data_pointer = self.data_pointer + 1
            elif code[self.pc] == "<":
                self.data_pointer = self.data_pointer - 1
            elif code[self.pc] == "+":
                self.memory.add_at_pointer(self.data_pointer, 1)
            elif code[self.pc] == "-":
                self.memory.add_at_pointer(self.data_pointer, -1)
            elif code[self.pc] == ".":
                self.output(chr(self.memory.get_value_at(self.data_pointer)))
            elif code[self.pc] == ",":
                self.memory.add_at_pointer(self.data_pointer, self.get_input())
            elif code[self.pc] == "[":
                if self.memory.get_value_at(self.data_pointer) == 0:
                    self.skip_until_nzero(code)
                else:
                    self.stack.append(self.pc)
            elif code[self.pc] == "]":
                if self.memory.get_value_at(self.data_pointer) != 0:
                    self.pc = self.stack[-1]
                else:
                    self.stack = self.stack[:-1]
            self.pc += 1

    def skip_until_nzero(self, code: str) -> None:
        depth = 0
        pointer = self.pc
        while self.pc < len(code):
            if code[self.pc] == "[":
                depth += 1
            if code[self.pc] == "]":
                depth -= 1
            if depth == 0:
                return
            self.pc += 1
        if depth != 0:
            raise Exception("Unbalanced brackets in code.", pointer)


def clean_code(code) -> list:
    new_code = []
    for char in re.findall(r"\+|\-|\<|\>|\[|\]|\.|\,", code):
        new_code.append(char)
    return new_code
