def brainfuck_loop_unroll(bf_code):
    """
    Unrolls all loops in a given Brainfuck code string and returns the optimized code.

    Inputs:
        bf_code: str, The Brainfuck code string to optimize.
        mem_count: int, The number of memory cells to analyse.

    Returns:
        str: The optimized Brainfuck code string with all loops unrolled.
    """
    result = ""
    loop_stack = []

    for char in bf_code:
        if char == "[":
            loop_stack.append(len(result))
        elif char == "]":
            if loop_stack:
                start_index = loop_stack.pop()
                loop_body = result[start_index:]
                result += loop_body
                if loop_stack:
                    result += bf_code[start_index + 1 : loop_stack[-1]]
                result += "]"

        result += char

    return result


# Abstract range
def memory_range_analysis_1(bf_code, mem_count=20):
    """
    Analyzes the memory ranges that each pointer in a Brainfuck program can access
    after executing the given code.

    Inputs:
        bf_code: str, The Brainfuck code to analyze.
        mem_count: int, The number of memory cells available in the program.

    Returns:
        A list of sets, where each set represents the memory ranges that a pointer
        can access after executing the code. The i-th set in the list corresponds
        to the i-th pointer in the program.
    """
    pointer = 0
    stack = []
    memory_ranges = [set(range(256)) for _ in range(mem_count)]

    for i, char in enumerate(bf_code):
        if char == ">":
            pointer += 1
        elif char == "<":
            pointer -= 1
        elif char == "+":
            memory_ranges[pointer] = memory_ranges[pointer].intersection(
                set(range(256))
            )
        elif char == "-":
            memory_ranges[pointer] = memory_ranges[pointer].intersection(
                set(range(256))
            )
        elif char == "[":
            stack.append(i)
        elif char == "]":
            start = stack.pop()
            memory_ranges[pointer] = memory_ranges[pointer].intersection(
                set(
                    range(
                        min(memory_ranges[pointer]) // abs(i - start),
                        max(memory_ranges[pointer]) // abs(i - start) + 1,
                    )
                )
            )

    return memory_ranges


def memory_range_analysis_2(bf_code, mem_count=20):
    """
    Analyzes the memory ranges that each pointer in a Brainfuck program can access
    after executing the given code.

    Inputs:
        bf_code: str, The Brainfuck code to analyze.
        mem_count: int, The number of memory cells available in the program.

    Returns:
        A list of tuple, where each tuple represents the memory ranges that a pointer
        can access after executing the code. The i-th tuple in the list corresponds
        to the i-th pointer in the program.
    """

    pointer = 0
    stack = []

    memory_ranges = [(0, 255) for _ in range(mem_count)]

    def _update_range(current_range, min_change, max_change):
        min_val = max(0, current_range[0] + min_change)
        max_val = min(255, current_range[1] + max_change)
        return (min_val, max_val)

    for i, char in enumerate(bf_code):
        if char == ">":
            pointer += 1
        elif char == "<":
            pointer -= 1
        elif char == "+":
            memory_ranges[pointer] = _update_range(memory_ranges[pointer], 1, 1)
        elif char == "-":
            memory_ranges[pointer] = _update_range(memory_ranges[pointer], -1, -1)
        elif char == "[":
            stack.append(i)
        elif char == "]":
            start = stack.pop()
            memory_ranges[pointer] = _update_range(
                memory_ranges[pointer], -(i - start), -(i - start)
            )

    return memory_ranges
