import graphviz
import time


class Visualizer(object):
    """
    Visualizer, made for obtaining a program graph from a
    BrainFuck program as an input string list.

    The graphs can be obtained either by running class
    function bfp_to_graph() or bfp_to_graph_compressed().
    The former is the graph most true to the program, 
    and the latter is the graph obtained by combining
    certain edges into one.


    Input:

    bfp: str list or str, the BrainFuck program.

    name: str, will be part of the name of the file the
          graph gets saved to, otherwise it will simply
          be "graph_" (see get_name() function).

          
    Attributes:

    edgelist: (int * int * str) tuple list, used to store
              edges of the produced graph.

    nodes: int list, is used to keep track of which nodes
           are actually used: if used, the number at that
           index will be updated to 1, otherwise 0 (see
           viz() function).

    bfp: str list or str, the BrainFuck program from input

    instruction_pointer: ????????????????????????????????

    stack: ????????????????????????????????

    last_edge: ????????????????????????????????

    count_sim: ????????????????????????????????

    name: ????????????????????????????????

    is_compressed: ????????????????????????????????

    
    Functions (check their docs):

    add_edge: int * int * str -> None

    find_end_loop: int -> int

    bfp_to_graph: None -> None

    get_name: None -> str

    viz: None -> None

    is_math_operation: (int * int * str) tuple -> bool

    get_operation: (int * int * str) tuple -> str

    get_operand: (int * int * str) tuple -> int
    
    get_operator: (int * int * str) tuple -> str

    is_optimizable: (int * int * str) tuple * 
                    (int * int * str) tuple -> bool

    get_optimized_edge: (int * int * str) tuple * 
                        (int * int * str) tuple -> 
                        (int * int * str) tuple

    bfp_to_graph_compressed: None -> None
    """

    def __init__(self, bfp: [str], name: str = "") -> None:
        self.edgelist: [tuple] = []
        self.nodes: [int] = [0] * (len(bfp) + 1)
        self.bfp: [str] = bfp
        self.instruction_pointer: int = 0
        self.stack: [int] = []
        self.last_edge: tuple = tuple()
        self.count_sim: int = 1
        self.name: str = name

        self.is_compressed = None

    def add_edge(self, start: int, end: int, name: str) -> None:
        """
        Text

        
        Return type: None

        
        Input:

        start: int, text

        end: int, text

        name: str, text


        Example: (Example)
        """
        self.nodes[start] = 1
        self.nodes[end] = 1
        self.edgelist.append((start, end, name))

    def find_end_loop(self, s) -> int:
        """
        Text

        
        Return type: int

        
        Input:

        s: int, text


        Example: (Example)
        """
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
        """
        Text

        
        Return type: None


        Example: (Example)
        """
        self.is_compressed = False
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
            else:
                self.instruction_pointer-=1 #failsafe to not have weird node numbers
            self.instruction_pointer += 1

    def get_name(self) -> str:
        """
        Text

        
        Return type: str


        Example: (Example)
        """
        temp = self.name
        if self.name == "":
            temp = "graph_"
        self.name = f'{temp}{str(time.time()).split(".")[0]}'
        return self.name

    def viz(self) -> None:
        """
        Text

        
        Return type: None


        Example: (Example)
        """
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
        dot.format = "png"
        dot.render(f"./graphs/{self.get_name()}", view=False)

    def is_math_operation(self, edge: (int,int,str)) -> bool:
        """
        Text

        
        Return type: bool


        Input:

        edge: (int * int * str) tuple, text


        Example: (Example)
        """
        if len(edge[2].split("+=")) == 2:
            return True
        elif len(edge[2].split("-=")) == 2:
            return True
        return False

    def get_operation(self, edge: (int,int,str)) -> str:
        """
        Text

        
        Return type: str


        Input:

        edge: (int * int * str) tuple, text


        Example: (Example)
        """
        if len(edge[2].split(" +=")) == 2:
            return edge[2].split(" +=")[0]
        elif len(edge[2].split(" -=")) == 2:
            return edge[2].split(" -=")[0]
        return ""

    def get_operand(self, edge: (int,int,str)) -> int:
        """
        Text

        
        Return type: int


        Input:

        edge: (int * int * str) tuple, text


        Example: (Example)
        """
        return int(edge[2].split("=")[1])

    def get_operator(self, edge: (int,int,str)) -> str:
        """
        Text

        
        Return type: str


        Input:

        edge: (int * int * str) tuple, text


        Example: (Example)
        """
        if len(edge[2].split("+=")) == 2:
            return "+"
        elif len(edge[2].split("-=")) == 2:
            return "-"
        return ""

    def is_optimizable(self, edge_1: (int,int,str), edge_2: (int,int,str)) -> bool:
        """
        Text

        
        Return type: bool


        Input:

        edge_1: (int * int * str) tuple, text

        edge_2: (int * int * str) tuple, text


        Example: (Example)
        """
        if (
            (self.get_operator(edge_1) == "+" and self.get_operator(edge_2) == "+")
            or (self.get_operator(edge_1) == "-" and self.get_operator(edge_2) == "-")
            or (self.get_operator(edge_1) == "-" and self.get_operator(edge_2) == "+")
            or (self.get_operator(edge_1) == "+" and self.get_operator(edge_2) == "-")
        ) and self.get_operation(edge_1) == self.get_operation(edge_2):
            return True
        return False

    def get_optimized_edge(self, edge_1: (int,int,str), edge_2: (int,int,str)) -> (int,int,str):
        """
        Text

        
        Return type: (int * int * str) tuple


        Input:

        edge_1: (int * int * str) tuple, text

        edge_2: (int * int * str) tuple, text


        Example: (Example)
        """
        operand_1 = self.get_operand(edge_1)
        operand_2 = self.get_operand(edge_2)
        operation = self.get_operation(edge_1)
        opr1 = self.get_operator(edge_1)
        opr2 = self.get_operator(edge_2)
        if opr1 == "+" and opr2 == "+":
            return (
                edge_1[0],
                edge_2[1],
                f"{operation} += {operand_1 + operand_2}",
            )
        elif opr1 == "-" and opr2 == "-":
            return (
                edge_1[0],
                edge_2[1],
                f"{operation} -= {operand_1 + operand_2}",
            )

        elif operand_1-operand_2<0:
            return (
                edge_1[0],
                edge_2[1],
                f"{operation} -= {abs(operand_1 - operand_2)}",
            )
        else:
            return (
                edge_1[0],
                edge_2[1],
                f"{operation} += {operand_1 - operand_2}",
            )

        return

    def bfp_to_graph_compressed(self) -> None:
        """
        Text

        
        Return type: None


        Example: (Example)
        """
        self.bfp_to_graph()
        self.is_compressed = True
        self.last_edge: tuple = self.edgelist[0]
        i = 1
        self.compressed = []
        self.nodes = [0 for _ in range(len(self.nodes))]
        while i <= len(self.edgelist):
            while (
                i < len(self.edgelist)
                and self.edgelist[i][2] == self.last_edge[2]
                and self.is_math_operation(self.edgelist[i])
            ):
                self.count_sim += 1
                i += 1

            if self.count_sim > 1:
                self.nodes[self.last_edge[0]] = 1
                self.nodes[self.edgelist[i - 1][1]] = 1

                self.compressed.append(
                    (
                        self.last_edge[0],
                        self.edgelist[i - 1][1],
                        f"{self.get_operation(self.last_edge)} {self.get_operator(self.last_edge)}= {self.count_sim}",
                    )
                )
            else:
                self.nodes[self.last_edge[0]] = 1
                self.nodes[self.last_edge[1]] = 1
                self.compressed.append(self.last_edge)

            if len(self.compressed) > 1 and self.is_optimizable(
                self.compressed[-1], self.compressed[-2]
            ):
                new_edge = self.get_optimized_edge(
                    self.compressed[-2], self.compressed[-1]
                )
                self.compressed[-2] = new_edge
                self.nodes[self.compressed[-1][0]] = 0
                self.nodes[self.compressed[-1][1]] = 0
                self.compressed.pop()

            self.count_sim = 1
            if i == len(self.edgelist):
                self.edgelist = self.compressed
                return
            self.last_edge = self.edgelist[i]
            if (
                self.is_math_operation(self.compressed[-1])
                and self.get_operand(self.compressed[-1]) == 0
            ):
                self.last_edge = (
                    self.compressed[-1][0],
                    self.last_edge[1],
                    self.last_edge[2],
                )
                self.nodes[self.compressed[-1][0]] = 0
                self.nodes[self.compressed[-1][1]] = 0
                self.compressed.pop()

            i += 1

        self.compressed.append(self.last_edge)
        self.edgelist = self.compressed
