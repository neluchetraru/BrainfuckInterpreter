def brainfuck_loop_unroll(bf_code, factor=2):
    result = ""
    loop_stack = []

    for char in bf_code:
        if char == "[":
            loop_stack.append(len(result))
        elif char == "]":
            if loop_stack:
                start_index = loop_stack.pop()
                loop_body = result[start_index:]
                result += loop_body * (factor - 1)
                if loop_stack:
                    result += bf_code[start_index + 1 : loop_stack[-1]]
                result += "]"

        result += char

    return result


bf_code = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
optimized_code = brainfuck_loop_unroll(bf_code, factor=2)
print("Original:", bf_code)
print("Optimized:", optimized_code)


# Abstract range
class BrainfuckAnalyzer:
    def __init__(self, program):
        self.program = program
        self.memory_ranges = [
            set(range(256)) for _ in range(30000)
        ]  # Assuming 30,000 memory cells

    def analyze(self):
        pointer = 0
        stack = []

        for i, char in enumerate(self.program):
            if char == ">":
                pointer += 1
            elif char == "<":
                pointer -= 1
            elif char == "+":
                self.memory_ranges[pointer] = self.memory_ranges[pointer].intersection(
                    set(range(256))
                )
            elif char == "-":
                self.memory_ranges[pointer] = self.memory_ranges[pointer].intersection(
                    set(range(256))
                )
            elif char == "[":
                stack.append(i)
            elif char == "]":
                start = stack.pop()
                self.memory_ranges[pointer] = self.memory_ranges[pointer].intersection(
                    set(
                        range(
                            min(self.memory_ranges[pointer]) // abs(i - start),
                            max(self.memory_ranges[pointer]) // abs(i - start) + 1,
                        )
                    )
                )

    def print_results(self):
        for i, cell_range in enumerate(self.memory_ranges):
            if i == 10:  # T
                break
            print(f"Memory Cell {i}: {min(cell_range)} - {max(cell_range)}")


brainfuck_program = "++++[>++<-]>[<+++++>-]<."

analyzer = BrainfuckAnalyzer(brainfuck_program)
analyzer.analyze()
analyzer.print_results()


# Alternative abstract range
class BrainfuckAnalyzer:
    def __init__(self, program):
        self.program = program
        self.memory_ranges = [
            (0, 255) for _ in range(30000)
        ]  # Assuming 30,000 memory cells

    def analyze(self):
        pointer = 0
        stack = []

        for i, char in enumerate(self.program):
            if char == ">":
                pointer += 1
            elif char == "<":
                pointer -= 1
            elif char == "+":
                self.memory_ranges[pointer] = self._update_range(
                    self.memory_ranges[pointer], 1, 1
                )
            elif char == "-":
                self.memory_ranges[pointer] = self._update_range(
                    self.memory_ranges[pointer], -1, -1
                )
            elif char == "[":
                stack.append(i)
            elif char == "]":
                start = stack.pop()
                self.memory_ranges[pointer] = self._update_range(
                    self.memory_ranges[pointer], -(i - start), -(i - start)
                )

    def _update_range(self, current_range, min_change, max_change):
        min_val = max(0, current_range[0] + min_change)
        max_val = min(255, current_range[1] + max_change)
        return (min_val, max_val)

    def print_results(self):
        for i, (min_val, max_val) in enumerate(self.memory_ranges):
            if i == 10:
                return
            print(f"Memory Cell {i}: Minimum: {min_val}, Maximum: {max_val}")


brainfuck_program = "++++[>++<-]>[<+++++>-]<."

analyzer = BrainfuckAnalyzer(brainfuck_program)
analyzer.analyze()
analyzer.print_results()
