from Visualizer import Visualizer

class Devisualizer(object):
    """
    Devisualizer, which is made for obtained BrainFuck code 
    from a program graph made using the Visualizer class

    Before making a Devisualizer instance, make sure the
    inputted Visualizer instance has already made a graph
    using either its function bfp_to_graph() or
    bfp_to_graph_compressed(), otherwise the Devisualizer
    will throw an error.

    
    Input:

    graph: Visualizer instance 
           
           Its class variable "edgelist" will serve as the 
           graph. This will also be made an attribute of 
           the Devisualizer instance with the same name.

    
    Attributes:

    bfp:   str, The BrainFuck program obtained by 
           reconstructing it from the graph.

    graph: Visualizer instance, The input of this class


    Functions (check their docs):

    graph_to_bfp: None -> None
    """
    def __init__(self, graph: Visualizer) -> None:
        self.bfp = None    #Will be written to in graph_to_bfp() call
        self.graph = graph
        self.graph_to_bfp()

    def graph_to_bfp(self) -> None:
        """
        Takes the class variable "graph", reconstructs
        the BrainFuck Program from it, and saves it as
        a string to the class variable "bfp".


        Example: THIS IS AN INTERNAL FUNCTION - 
                 IT WILL BE RUN UPON INITIALIZATION OF 
                 THE DEVISUALIZER CLASS
        """

        #Throws error if there's no graph in inputted Visualizer instance
        if self.graph.is_compressed == None:
           err_message= "No graph produced in inputted Visualizer instance - "
           err_message+="Please run {Visualizer instance}.bfp_to_graph() or "
           err_message+="{Visualizer instance}.bfp_to_graph_compressed() to use this function."
           raise ValueError(err_message)

        localbfp = []                       #Resulting program is saved to this list

        for start, end, name in self.graph.edgelist: #Loop through edges
            
            namelist = name.split(" ")      #Edge label as a list of "words"        

            if len(namelist)==1:            #Label: print(chr(memory[data_pointer]))
                localbfp.insert(start,".")
                continue
            elif len(namelist)==2:          #Label: print(chr(memory[data_pointer])) = [amount]
                amount = int(namelist[1])
                localbfp.insert(start,amount*".")
                continue

            parameter, opr, amount = namelist
            amount = int(amount)

            if opr == "==":                 #Label: memory[data_pointer] == 0
                                            #This specifies a loop, but since
                                            #loops have two edges, we want to
                                            #ignore one of the edges
                continue
            elif opr == "!=":               #Label: memory[data_pointer] != 0
                
                if end==start+1:            #Edgecase - Empty loop
                    localbfp.insert(start,"[]")
                elif start<end:             #Edge going forwards, meaning start of loop
                    localbfp.insert(start,"[")
                elif start>end:             #Edge going backwards, meaning end of loop
                    localbfp.insert(start,"]")
                else:                       #DEPRECATED, empty loops were in one node
                    localbfp.insert(start,"[]")
                continue

            if parameter == "data_pointer": #Label: data_pointer [opr] [amount]
                                            #Which means instruction is either ">" or "<"
                if opr == "+=":
                    instr = ">"
                else:
                    instr = "<"

            else:                           #Label: memory[data_pointer] [opr] [amount]
                                            #Which means instruction is either "+" or "-"
                if opr == "+=":
                    instr = "+"
                else:
                    instr = "-"
                
            localbfp.insert(start,amount*instr) #amount specifies how many of the instruction are in a row

        self.bfp = "".join(localbfp)        #bfp is now a string with the BrainFuck Program
            
