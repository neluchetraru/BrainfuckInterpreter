import graphviz
import time


class Visualizer(object):
    def __init__(self, bfp: [str], name: str = "") -> None:
        self.edgelist: [tuple] = []
        self.nodes: [int] = [0] * (len(bfp) + 1)
        self.bfp: [str] = bfp
        self.instruction_pointer: int = 0
        self.stack: [int] = []
        self.last_edge: tuple = tuple()
        self.count_sim: int = 1
        self.name: str = name

    def add_edge(self, start: int, end: int, name: str) -> None:
        self.nodes[start] = 1
        self.nodes[end] = 1
        self.edgelist.append((start, end, name))

    def find_end_loop(self, s) -> int:
        depth = 0
        src = s
        for instr in self.bfp[src:]:
            if instr == "[":
                depth += 1
            elif instr == "]":
                depth -= 1
            if depth == 0:
                return src
            src += 1

        return -1

    def bfp_to_graph(self) -> None:
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
                self.stack.append(self.instruction_pointer)
                end = self.find_end_loop(self.instruction_pointer)
                if end == -1:
                    print("ERROR: Check for syntax errors.")
                    return
                self.add_edge(
                    self.instruction_pointer, end, f"memory[data_pointer] == 0"
                )
                self.add_edge(
                    self.instruction_pointer,
                    self.instruction_pointer + 1,
                    f"memory[data_pointer] != 0",
                )

            elif instr == "]":
                self.add_edge(
                    self.instruction_pointer,
                    self.stack.pop(),
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

    def get_name(self) -> str:
        temp = self.name
        if self.name == "":
            temp = "graph_"
        return f'{temp}{str(time.time()).split(".")[0]}'

    def viz(self) -> None:
        dot = graphviz.Digraph()
        for i in range(len(self.nodes)):
            if self.nodes[i] == 1:
                dot.node(str(i), str(i))

        for i in range(len(self.edgelist)):
            dot.edge(
                str(self.edgelist[i][0]),
                str(self.edgelist[i][1]),
                label=self.edgelist[i][2],
            )
        dot.format = "svg"
        dot.render(f"./graphs/{self.get_name()}", view=True)

    def bfp_to_graph_compressed(self) -> None:
        self.bfp_to_graph()
        self.last_edge: tuple = self.edgelist[0]
        i = 1
        self.compressed = []
        self.nodes = [0 for i in range(len(self.nodes))]
        while i < len(self.edgelist):
            while self.edgelist[i][2] == self.last_edge[2]:
                self.count_sim += 1
                i += 1
            if self.count_sim > 1:
                self.nodes[self.last_edge[0]] = 1
                self.nodes[self.edgelist[i - 1][1]] = 1
                self.compressed.append(
                    (
                        self.last_edge[0],
                        self.edgelist[i - 1][1],
                        self.last_edge[2].split("= ")[0] + f"= {self.count_sim}",
                    )
                )
            else:
                self.nodes[self.last_edge[0]] = 1
                self.nodes[self.last_edge[1]] = 1
                self.compressed.append(self.last_edge)
            self.count_sim = 1
            self.last_edge = self.edgelist[i]
            i += 1
        self.compressed.append(self.last_edge)
        self.edgelist = self.compressed
