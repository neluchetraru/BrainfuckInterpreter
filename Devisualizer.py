from Visualizer import Visualizer

class Devisualizer(object):
    def __init__(self, graph: Visualizer) -> None:
        self.bfp = None
        self.graph = graph
        self.graph_to_bfp()

    def graph_to_bfp(self) -> None:
        if self.graph.is_compressed == None:
           raise ValueError("No graph produced in inputted Visualizer instance - Please run {Visualizer instance}.bfp_to_graph() to use this function.")

        #elif not self.graph.is_compressed:
        #    raise ValueError("This function is only meant for COMPRESSED bfp graphs - Please run {Visualizer instance}.bfp_to_graph() to use this function.")

        localbfp = []
        for start, end, name in self.graph.edgelist:
            namelist = name.split(" ")

            if len(namelist)==1:
                localbfp.insert(start,".")
                continue
            elif len(namelist)==2:
                amount = int(namelist[1])
                localbfp.insert(start,amount*".")
                continue

            parameter, opr, amount = namelist
            amount = int(amount)

            if opr == "==":
                continue
            elif opr == "!=":
                if start<end:
                    localbfp.insert(start,"[")
                elif start>end:
                    localbfp.insert(start,"]")
                else:
                    localbfp.insert(start,"[]")
                continue

            if parameter == "data_pointer": #Instruction is either "<" or ">"
                if opr == "+=":
                    instr = ">"
                else:
                    instr = "<"

            else:                           #Instruction is either "-" or "+"
                if opr == "+=":
                    instr = "+"
                else:
                    instr = "-"
                
            localbfp.insert(start,amount*instr)

        self.bfp = "".join(localbfp)
            
