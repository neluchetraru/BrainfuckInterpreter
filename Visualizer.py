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

    bfp: str, the BrainFuck program.

    name: str, will be part of the name of the file the
          graph gets saved to, otherwise it will simply
          be "graph_" (see get_name() function).


    Attributes:

    edgelist: (int * int * str) tuple list, used to store
              edges of the produced graph.

    bfp: str, the BrainFuck program from input
         (see above)

    instruction_pointer: int, corresponds to the
                         instruction pointer of the bfp
                         (see bfp_to_graph() function).

    stack: int list, corresponds to the loop stack
           (see bfp_to_graph() function).

    last_edge: (int * int * str) tuple, used as a variable
               in bfp_to_graph_compressed() function to
               keep track of the edge in the last iteration

    count_dup: int, used as a variable in
               bfp_to_graph_compressed() function to keep
               track of how many duplicate edges there are
               in a row (in order to compress them)

    name: str, the name from input (see above), but after
          running get_name() will be changed to also have
          numbers from current time (for unique file name
          purposes).

    is_compressed: bool, initially None. If bfp_to_graph()
                   has been run, it will be False, if
                   bfp_to_graph_compressed() has been run,
                   it will be True


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

    def __init__(self, bfp: str, name: str = "") -> None:
        self.edgelist: [tuple] = []
        self.bfp: str = bfp
        self.instruction_pointer: int = 0
        self.stack: [int] = []
        self.last_edge: tuple = tuple()
        self.count_dup: int = 1
        self.name: str = name

        self.is_compressed = None

    def add_edge(self, start: int, end: int, name: str) -> None:
        """
        Adds an edge to the edgelist class variable


        Return type: None


        Input:

        start: int, starting node

        end: int, end node

        name: str, edge label


        Example: THIS IS AN INTERNAL FUNCTION -
                 IT WILL BE RUN IN bfp_to_graph()
        """
        self.edgelist.append((start, end, name))

    def find_end_loop(self, start_instruction_pointer) -> int:
        """
        Finds instruction pointer for the end of the loop
        associated with the loop the inputted pointer, which
        points to the start of loop.


        Return type: int


        Input:

        start_instruction_pointer: int, the value of the pointer
                                   where the loop starts


        Example: THIS IS AN INTERNAL FUNCTION -
                 IT WILL BE RUN IN bfp_to_graph()
        """
        depth = 0
        for instr in self.bfp[start_instruction_pointer:]:
            if instr == "[":
                depth += 1
            elif instr == "]":
                depth -= 1
            if depth == 0:
                return start_instruction_pointer
            start_instruction_pointer += 1

        return -1

    def bfp_to_graph(self) -> None:
        """
        Turns the program in the class variable bfp into the
        corresponding program graph. Each instruction is one
        edge (except "[" and "]", there's both a ==0 and !=0 edge)


        Return type: None


        Example: bfp = "++++++++++++++++++."
                 vis = Visualizer(bfp)
                 vis.bfp_to_graph()
                 vis.viz() #graph saved to ./graphs/
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
                self.instruction_pointer -= 1  # failsafe to not have weird node numbers
            self.instruction_pointer += 1

    def get_name(self) -> str:
        """
        Returns the name chosen upon input - unless none
        was chosen, in which case "graph_" is chosen instead -
        together with the numbers from the current time for
        unique file name purposes.


        Return type: str


        Example: THIS IS AN INTERNAL FUNCTION -
                 IT WILL BE RUN IN viz()
        """
        temp = self.name
        if self.name == "":
            temp = "graph_"
        self.name = f'{temp}{str(time.time()).split(".")[0]}'
        return self.name

    def viz(self) -> None:
        """
        Creates a graph visualization of the edgelist using graphviz library and saves it as a png file.

        Parameters:
        None

        Returns:
        None

        Example:
            vis = Visualizer("++")
            vis.bfp_to_graph_compressed()
            vis.viz()
        """
        dot = graphviz.Digraph()
        for i in range(len(self.edgelist)):
            dot.edge(
                str(self.edgelist[i][0]),
                str(self.edgelist[i][1]),
                label=self.edgelist[i][2],
            )
        dot.format = "png"
        dot.render(f"./graphs/{self.get_name()}", view=False)

    def is_math_operation(self, edge: (int, int, str)) -> bool:
        """
        Determines whether the given edge represents a mathematical operation.

        Input:
        edge: (int, int, str), A tuple of three elements representing the edge to check. The first two elements are integers
                representing the start and end nodes of the edge, respectively. The third element is a string
                representing the label of the edge.

        Returns: bool, A boolean value indicating whether the given edge represents a mathematical operation.

        Example:
            is_math_operation((0, 1, 'x += 1')) -> True
            is_math_operation((1, 2, 'y -= 2')) -> True
            is_math_operation((2, 3, 'z = 3')) -> False
        """
        if len(edge[2].split("+=")) == 2:
            return True
        elif len(edge[2].split("-=")) == 2:
            return True
        return False

    def get_operation(self, edge: (int, int, str)) -> str:
        """
        This method receives a tuple with three elements: two integers and a string.
        The string represents an operation that is performed on a variable.
        The method returns the variable that is being operated on.

        Input:
        edge: (int, int, str), representing the edge of a graph.

        Returns: str, the variable that is being operated on.

        Example:
        get_operation((1, 2, 'x += 1')) -> 'x'
        """
        if len(edge[2].split(" +=")) == 2:
            return edge[2].split(" +=")[0]
        elif len(edge[2].split(" -=")) == 2:
            return edge[2].split(" -=")[0]
        return ""

    def get_operand(self, edge: (int, int, str)) -> int:
        """
        Returns the operand value of the given edge.

        Input:
        edge: (int, int, str), A tuple of three values representing the edge. The first two values are the indices of the nodes
                  connected by the edge, and the third value is the label of the edge in the format "operand=<value>".

        Returns: int, The integer value of the operand.

        Example:
            get_operand((0, 1, "operand=10")) -> 10
        """
        return int(edge[2].split("=")[1])

    def get_operator(self, edge: (int, int, str)) -> str:
        """
        Returns the operator of the given edge.
        The operator is determined by checking if the third element of the edge tuple
        contains either '+=' or '-='.

        Input:
        edge: (int, int, str), A tuple of three elements (int, int, str) representing an edge in the graph.

        Returns: str, A string representing the operator of the given edge. If the operator is not
                 found, an empty string is returned.

        Example:
            get_operator((0, 1, '+=')) -> '+'
        """
        if len(edge[2].split("+=")) == 2:
            return "+"
        elif len(edge[2].split("-=")) == 2:
            return "-"
        return ""

    def is_comparing_operation(self, edge: (int, int, str)) -> bool:
        if len(edge[2].split("==")) == 2:
            return True
        elif len(edge[2].split("!=")) == 2:
            return True
        return False

    def is_optimizable(self, edge_1: (int, int, str), edge_2: (int, int, str)) -> bool:
        """
        Determines if two edges in the graph can be optimized by combining them into a single edge.

        Input:

        edge_1: tuple(int, int, str), A tuple representing the first edge in the graph. The tuple should contain three elements:
                       the starting node, the ending node, and the operation performed by the edge.
        edge_2: tuple(int, int, str), A tuple representing the second edge in the graph. The tuple should contain three elements:
                       the starting node, the ending node, and the operation performed by the edge.

        Returns: bool, A boolean value indicating whether the two edges can be optimized.

        Example:
            is_optimizable((0, 1, '+'), (1, 2, '+')) -> True
        """
        if (
            (self.get_operator(edge_1) == "+" and self.get_operator(edge_2) == "+")
            or (self.get_operator(edge_1) == "-" and self.get_operator(edge_2) == "-")
            or (self.get_operator(edge_1) == "-" and self.get_operator(edge_2) == "+")
            or (self.get_operator(edge_1) == "+" and self.get_operator(edge_2) == "-")
        ) and self.get_operation(edge_1) == self.get_operation(edge_2):
            return True
        return False

    def get_optimized_edge(
        self, edge_1: (int, int, str), edge_2: (int, int, str)
    ) -> (int, int, str):
        """
        Given two edges, returns an optimized edge that combines the two operations if possible.

        Input:
        edge_1: tuple(int, int, str), a tuple representing the first edge, containing the starting node index, ending node index, and operation string.
        edge_2: tuple(int, int, str), a tuple representing the second edge, containing the starting node index, ending node index, and operation string.

        Returns: tuple(int, int, str), a tuple representing the optimized edge, containing the starting node index, ending node index, and operation string.

        Example:
            get_optimized_edge((0, 1, "a"), (1, 2, "b")) -> (0, 2, "a += b")
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

        elif opr1 == "-" and opr2 == "+":
            if operand_1 - operand_2 < 0:
                return (
                    edge_1[0],
                    edge_2[1],
                    f"{operation} += {abs(operand_1-operand_2)}",
                )
            return (
                edge_1[0],
                edge_2[1],
                f"{operation} -= {abs(operand_1 - operand_2)}",
            )
        else:
            if operand_1 - operand_2 < 0:
                return (
                    edge_1[0],
                    edge_2[1],
                    f"{operation} -= {abs(operand_1-operand_2)}",
                )
            return (
                edge_1[0],
                edge_2[1],
                f"{operation} += {abs(operand_1 - operand_2)}",
            )

    def bfp_to_graph_compressed(self) -> None:
        """
        Compresses the edgelist of the graph generated from the Brainfuck code by combining consecutive edges that have the same operation and operator.
        If an edge is compressed, its operation is changed to the corresponding math operation (+= or -=) and its weight is set to the number of consecutive edges that were compressed.
        If the compressed edge can be further optimized with the previous edge, they are combined into a single edge.
        If the compressed edge is +=/-= 0, it is removed.

        Return: None

        Example:
            vis = Vizualizer("++")
            vis.bfp_to_graph(compressed)  # Generate the edgelist for the compressed graph
            vis.viz()  # Use graphviz to visualize



        """
        self.bfp_to_graph()
        self.is_compressed = True
        self.last_edge: tuple = self.edgelist[0]
        i = 1
        self.compressed = []
        while i <= len(self.edgelist):
            # Count how many duplicate edges in a row
            while (
                i < len(self.edgelist)
                and self.edgelist[i][2] == self.last_edge[2]
                and self.is_math_operation(self.edgelist[i])
            ):
                self.count_dup += 1
                i += 1

            # If duplicate edges, add new compressed edge
            if self.count_dup > 1:
                self.compressed.append(
                    (
                        self.last_edge[0],
                        self.edgelist[i - 1][1],
                        f"{self.get_operation(self.last_edge)} {self.get_operator(self.last_edge)}= {self.count_dup}",
                    )
                )

            # No duplicate edges, last edge is compressed
            else:
                self.compressed.append(self.last_edge)

            # Compress added edge with the one prior if possible
            if len(self.compressed) > 1 and self.is_optimizable(
                self.compressed[-2], self.compressed[-1]
            ):
                new_edge = self.get_optimized_edge(
                    self.compressed[-2], self.compressed[-1]
                )
                self.compressed[-2] = new_edge
                self.compressed.pop()

            # Every edge has been check, update edgelist, end function
            if i == len(self.edgelist):
                self.edgelist = self.compressed
                return

            # Update last_edge - if last compressed edge is +=/-= 0, remove it
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
                if self.is_comparing_operation(self.last_edge):
                    self.last_edge = (
                        self.last_edge[1],
                        self.last_edge[1],
                        self.last_edge[2],
                    )
                    self.compressed.pop()
                self.compressed.pop()

            # Reset counters
            self.count_dup = 1
            i += 1

        # Every edge has been check, update edgelist, end function
        self.compressed.append(self.last_edge)
        self.edgelist = self.compressed
