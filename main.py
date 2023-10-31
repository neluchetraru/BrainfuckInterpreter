from Visualizer import Visualizer

vis = Visualizer(
    # "++++++++[>++++[>++>+++]]"
    "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.",
    "Simple",
)
vis.bfp_to_graph()
# vis.bfp_to_graph_compressed()
vis.viz()
