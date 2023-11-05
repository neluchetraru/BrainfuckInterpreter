from Visualizer import Visualizer
from Devisualizer import Devisualizer

vis = Visualizer(
    #"++++++++[>++++[>++>+++]]",
    "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.",
    #"+++[]---",
    "Simple",
)
vis.bfp_to_graph()
#vis.bfp_to_graph_compressed()
#vis.viz()

devis = Devisualizer(vis)

print(f"Original BFP = {vis.bfp}\nDeconstructed= {devis.bfp}")
