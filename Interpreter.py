from typing import Any
import re


class Memory(object):
    def __init__(self, size=10) -> None:
        self.size = size
        self.memory = [0] * self.size
        self.memory_accesses = [0] * self.size
        self.limit = 30000
        self.max = [0] * self.size  # debugging
        self.max_pointer = 0

    def get_memory(self) -> list:
        return self.memory

    def get_size(self) -> int:
        return self.size

    def print_at_pointer(self, pointer: int) -> None:
        char = chr(int(str(self.memory[pointer])))
        print(char, end="", flush=True)
        return char

    def add_at_pointer(self, pointer: int, amount: int) -> None:
        if pointer >= len(self.memory):
            self.memory += [0] * (pointer - len(self.memory) + 1)
            self.memory_accesses += [0] * (pointer - len(self.memory_accesses) + 1)
            self.max += [0] * (pointer - len(self.max) + 1)
        self.memory[pointer] = (self.memory[pointer] + amount) % 256
        self.memory_accesses[pointer] += 1
        if self.memory[pointer] > self.limit:
            raise Exception("Memory limit exceeded.")
        if self.memory[pointer] > self.max[pointer]:
            self.max[pointer] = self.memory[pointer]
        if self.max_pointer < pointer:
            self.max_pointer = pointer
        return self.memory[pointer]

    def get_value_at(self, pointer: int) -> int:
        if len(self.memory) - 1 < pointer:
            self.memory += [0] * (pointer - len(self.memory) + 1)
            self.memory_accesses += [0] * (pointer - len(self.memory_accesses) + 1)
            self.max += [0] * (pointer - len(self.max) + 1)
        self.memory_accesses[pointer] += 1
        return self.memory[pointer]

    def reset(self) -> None:
        self.memory = [0] * self.size
        self.memory_accesses = [0] * self.size

    def get_memory_state(self) -> list:
        return sum(self.memory)


class Interpreter(object):
    def __init__(self, memory, timeout=0) -> None:
        self.memory = memory
        self.data_pointer = 0
        self.pc = 0
        self.stack = []
        self.timeout = timeout
        self.count_loops = 0
        self.running = True

        self.input_pointer = 0

    def get_input(self) -> Any:
        try:
            data = self.inputter.get("1.0", "end-1c").strip().split(" ")
            if data == [""]:
                data = []
        except:
            data = []
        if self.input_pointer >= len(data):
            self.output("ERROR: Input limit exceeded.")
            raise Exception("Input limit exceeded.")
        else:
            self.input_pointer += 1
            return ord(data[self.input_pointer - 1])

    def output(self, arg, clear=False) -> str:
        if clear and self.printer:
            self.printer.delete("end-1c")
        if self.printer:
            self.printer.insert("end", arg)

    def move_pointer(self, amount: int) -> int:
        self.data_pointer = (self.data_pointer + amount) % self.memory.limit
        return self.data_pointer

    def run(self, code: str, printer=None, inputter=None) -> None:
        self.printer = printer
        self.inputter = inputter
        self.infinite_loop = False
        code = clean_code(code)

        try:
            syntax_checker(code)
        except Exception:
            self.output("ERROR: Unbalanced brackets in code.")
            return

        prev_memory_state = self.memory.get_memory_state()

        while self.pc < len(code) and self.running:
            if code[self.pc] == ">":
                self.move_pointer(1)
            elif code[self.pc] == "<":
                self.move_pointer(-1)
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
                    if self.timeout > 0:
                        prev_memory_state = self.memory.get_memory_state()
                    self.stack.append(self.pc)
            elif code[self.pc] == "]":
                if self.memory.get_value_at(self.data_pointer) != 0:
                    if self.timeout > 0:  # Only if infinite loop detection is enabled
                        current_memory_state = self.memory.get_memory_state()
                        if current_memory_state - prev_memory_state >= 0:
                            self.count_loops += 1
                            prev_memory_state = current_memory_state
                            if self.count_loops > self.timeout:
                                self.output(
                                    "ERROR: Timeout. Possible infinite loop detected.",
                                )
                                self.infinite_loop = True  # For testing purposes
                                return
                    self.pc = self.stack[-1]
                else:
                    if self.timeout > 0:
                        self.count_loops = 0
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


def clean_code(code) -> str:
    new_code = ""
    for char in re.findall(r"\+|\-|\<|\>|\[|\]|\.|\,", code):
        new_code += char

    return new_code


def syntax_checker(code) -> None:
    depth = 0
    i = 0
    while i < len(code):
        if code[i] == "[":
            depth += 1
        if code[i] == "]":
            depth -= 1
        if depth == 0:
            return
        i += 1
    if depth != 0:
        raise Exception("Unbalanced brackets in code.", i)
