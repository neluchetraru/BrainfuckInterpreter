from typing import Any
import re


class Memory(object):
    def __init__(self, size = 30000) -> None:
        self.size = size
        self.memory = [0] * size

    def get_memory(self) -> list:
        return self.memory
    
    def get_size(self) -> int:
        return self.size
    
    def print_at_pointer(self, pointer: int) -> None:
        print(chr(self.memory[pointer]),end="",flush=True)
    
class MemoryByteArray(object):
    def __init__(self, size = 30000) -> None:
        self.size = size
        self.memory = bytearray(size)

    def get_memory(self) -> list:
        return self.memory
    
    def get_size(self) -> int:
        return self.size
    
    def print_at_pointer(self, pointer: int) -> None:
        print(chr(int(str(self.memory[pointer]))), end='', flush=True)
    


class Interpreter(object):

    def __init__(self, memclass) -> None:
        self.memory =  memclass()
        self.data_pointer = 0
        self.pc = 0
        self.stack = []
        self.loop_depth = 0
    
    def run(self, code: str) -> None:
        while self.pc < len(code):
            print(self.memory.get_memory()[:8])
            if code[self.pc] == '>':
                self.data_pointer += 1
            elif code[self.pc] == '<':
                self.data_pointer -= 1
            elif code[self.pc] == '+': 
                self.memory.get_memory()[self.data_pointer] =  (self.memory.get_memory()[self.data_pointer] + 1) % 255
            elif code[self.pc] == '-':
                self.memory.get_memory()[self.data_pointer] =  (self.memory.get_memory()[self.data_pointer] - 1) % 255
            elif code[self.pc] == '.':
                self.memory.print_at_pointer(self.data_pointer)
            elif code[self.pc] == ',':
                self.memory.get_memory()[self.data_pointer] = ord(input()) 
            elif code[self.pc] == '[': 
                if self.memory.get_memory()[self.data_pointer] == 0: 
                    self.skip_until_nzero(code)
                else:
                    self.stack.append(self.pc)
            elif code[self.pc] == ']':
                if self.memory.get_memory()[self.data_pointer] != 0:
                    self.pc = self.stack[-1] 
                else:
                    self.stack = self.stack[:-1]
            self.pc += 1
            
    def skip_until_nzero (self, code: str) -> None:
        depth = 0
        while self.pc < len(code):
            if (code[self.pc] == "["):
                depth += 1
            if (code[self.pc] == "]"):
                depth -= 1
            if (depth == 0):
                return
            self.pc += 1


code = open("program.bf").read()

print(len(code))


def clean_code(code) -> list:
    new_code = []
    for char in  re.findall(r"\+|\-|\<|\>|\[|\]|\.|\,",code):
       new_code.append(char)
    return new_code

clean_code = clean_code(code)

print(len(clean_code))
print(clean_code)
interpreter = Interpreter(Memory)
interpreter.run(clean_code)
