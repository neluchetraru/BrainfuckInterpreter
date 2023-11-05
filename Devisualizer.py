from Visualizer import Visualizer

class Devisualizer(object):
    def __init__(self, graph: Visualizer) -> None:
        self.bfp = None
        self.graph = graph
        self.graph_to_bfp()
        
    def graph_to_bfp(self) -> None:
        """
        IMPORTANT: This ONLY works for NON-compressed bfp graphs
        """
        if self.graph.is_compressed == None:
           raise ValueError("No graph produced in inputted Visualizer instance - Please run {Visualizer instance}.bfp_to_graph() to use this function.")

        elif self.graph.is_compressed:
            raise ValueError("This function is only meant for NON-compressed bfp graphs - Please run {Visualizer instance}.bfp_to_graph() to use this function.")

        localbfp = ""
        skipnext = False
        for start, end, name in self.graph.edgelist:
            if skipnext:
                skipnext = False
                continue

            namelist = name.split(" ")
            if len(namelist)==1:
                localbfp+="."
                continue
            
            parameter, opr, amount = namelist
            amount = int(amount)

            if end != start+1: #Instruction is either "[" or "]" WILL NOT WORK FOR EMPTY LOOPS!!
                skipnext = True
                if opr == "==":
                    localbfp += "["
                    continue

                if end == start-1:
                    localbfp += "[]" #Edge case, end of empty loop encountered
                    continue

                localbfp += "]"
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
                
            localbfp+=amount*instr

        self.bfp = localbfp

            

            
            




            