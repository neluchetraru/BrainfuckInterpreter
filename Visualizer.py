import graphviz


class Visualizer(object):
    def __init__(self, bfp: [str]) -> None:
        self.edgelist = []
        self.nodecount = 0
        self.loop_count = 0
        self.bfp: [str] = bfp
        self.instruction_pointer = 0
        self.stack = []

    def add_edge(self, start: int, end: int, name: str) -> None:
        self.nodecount += 1
        self.edgelist.append((start, end, name))

    def find_end_loop(self) -> int:
        depth = 0
        for instr in self.bfp[self.nodecount :]:
            if instr == "[":
                depth += 1
            elif instr == "]":
                depth -= 1
            if depth == 0:
                return self.nodecount
            self.nodecount += 1

    def bfp_to_graph(self):
        for instr in self.bfp:
            if instr == ">":
                self.add_edge(
                    self.instruction_pointer,
                    self.instruction_pointer + 1,
                    f"data_pointer += 1",
                )
            elif instr == "<":
                self.add_edge(
                    self.instruction_pointer,
                    self.instruction_pointer + 1,
                    f"data_pointer -= 1",
                )
            elif instr == "+":
                self.add_edge(
                    self.instruction_pointer,
                    self.instruction_pointer + 1,
                    f"memory[data_pointer] += 1",
                )
            elif instr == "-":
                self.add_edge(
                    self.instruction_pointer,
                    self.instruction_pointer + 1,
                    f"memory[data_pointer] -= 1",
                )
            elif instr == "[":
                self.loop_count += 1
                self.stack.append(self.instruction_pointer)
                end = self.find_end_loop()
                self.add_edge(
                    self.instruction_pointer, end, f"memory[data_pointer] == 0"
                )
                self.add_edge(
                    self.instruction_pointer,
                    self.instruction_pointer + 1,
                    f"memory[data_pointer] != 0",
                )

            elif instr == "]":
                self.loop_count -= 1

                self.add_edge(
                    self.instruction_pointer,
                    self.stack[-1],
                    f"memory[data_pointer] != 0",
                )
                self.add_edge(
                    self.instruction_pointer,
                    self.instruction_pointer + 1,
                    f"memory[data_pointer] == 0",
                )

            elif instr == ".":
                self.add_edge(
                    self.instruction_pointer,
                    self.instruction_pointer + 1,
                    f"print(chr(memory[data_pointer]))",
                )
            self.instruction_pointer += 1

    def viz(self):
        dot = graphviz.Digraph()
        for i in range(self.instruction_pointer):
            dot.node(str(i), str(i))

        for i in range(len(self.edgelist)):
            dot.edge(
                str(self.edgelist[i][0]),
                str(self.edgelist[i][1]),
                label=self.edgelist[i][2],
            )
        dot.format = "svg"
        dot.render("graph.gv", view=True)
