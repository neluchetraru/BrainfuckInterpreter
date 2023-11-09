# from Visualizer import Visualizer
# from Devisualizer import Devisualizer

# vis = Visualizer(
#     # "++++++++[>++++[>++>+++]]",
#     # "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.",
#     "++[]--",
#     "Simple",
# )
# # vis.bfp_to_graph()
# vis.bfp_to_graph_compressed()
# # vis.viz()

# devis = Devisualizer(vis)

# print(f"Original BFP = {vis.bfp}\nDeconstructed= {devis.bfp}")

import tkinter as tk
from Interpreter import Interpreter, Memory
from Visualizer import Visualizer


def run_program():
    code = code_editor.get("1.0", "end-1c")  # Get the code from the text widget
    inte = Interpreter(Memory)
    inte.run(code)  # Call your Brainfuck interpreter
    output_label.delete("1.0", "end")
    output_label.insert(
        "1.0", "".join(inte.output)
    )  # Display the output in the output text widget


class ScrollableImage(tk.Frame):
    def __init__(self, master=None, **kw):
        self.image = kw.pop("image", None)
        sw = kw.pop("scrollbarwidth", 10)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tk.Canvas(self, highlightthickness=0, **kw)
        self.cnvs.create_image(0, 0, anchor="nw", image=self.image)
        # Vertical and Horizontal scrollbars
        self.v_scroll = tk.Scrollbar(self, orient="vertical", width=sw)
        self.h_scroll = tk.Scrollbar(self, orient="horizontal", width=sw)
        # Grid and configure weight.
        self.cnvs.grid(row=0, column=0, sticky="nsew")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set the scrollbars to the canvas
        self.cnvs.config(
            xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set
        )
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.cnvs.yview)
        self.h_scroll.config(command=self.cnvs.xview)
        # Assign the region to be scrolled
        self.cnvs.config(scrollregion=self.cnvs.bbox("all"))
        self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)

    def mouse_scroll(self, evt):
        if evt.state == 0:
            self.cnvs.yview_scroll(-1 * (evt.delta), "units")  # For MacOS
            self.cnvs.yview_scroll(int(-1 * (evt.delta / 120)), "units")  # For windows
        if evt.state == 1:
            self.cnvs.xview_scroll(-1 * (evt.delta), "units")  # For MacOS
            self.cnvs.xview_scroll(int(-1 * (evt.delta / 120)), "units")  # For windows


def display_program_graph_simple():
    code = code_editor.get("1.0", "end-1c")
    vis = Visualizer(code)
    vis.bfp_to_graph()
    vis.viz()

    graph_window = tk.Toplevel(root)
    graph_window.title("Program Graph")
    graph_img = tk.PhotoImage(file=f"./graphs/{vis.name}.png")
    height = min(root.winfo_screenheight(), graph_img.height()) - 100
    width = min(root.winfo_screenwidth(), graph_img.width())
    graph_window.geometry(f"{width + 50}x{height}")
    image_window = ScrollableImage(
        graph_window,
        image=graph_img,
        height=height,
        width=width,
    )
    image_window.pack()


def display_program_graph_compressed():
    code = code_editor.get("1.0", "end-1c")
    vis = Visualizer(code)
    vis.bfp_to_graph_compressed()
    vis.viz()

    graph_window = tk.Toplevel(root)
    graph_window.title("Program Graph Compressed")
    graph_img = tk.PhotoImage(file=f"./graphs/{vis.name}.png")
    height = min(root.winfo_screenheight(), graph_img.height()) - 100
    width = min(root.winfo_screenwidth(), graph_img.width())
    graph_window.geometry(f"{width + 50}x{height}")
    image_window = ScrollableImage(
        graph_window,
        image=graph_img,
        height=height,
        width=width,
    )
    image_window.pack()


# Create the main application window
root = tk.Tk()
root.title("Brainfuck Interpreter")


# Create a text widget for code input
code_editor = tk.Text(root, wrap=tk.WORD, width=40, height=20)
code_editor.grid(row=0, column=0, padx=10, pady=10)

# Create a frame to group the buttons in the same row
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, padx=10, pady=10)

# Create a button to run the Brainfuck program and visualize it
run_button = tk.Button(button_frame, text="Run program", command=run_program)
run_button.grid(row=0, column=0, padx=10)

# Create another button in the same frame
other_button = tk.Button(
    button_frame, text="Visualize Simple", command=display_program_graph_simple
)
other_button.grid(row=0, column=1, padx=10)
other_button = tk.Button(
    button_frame, text="Visualize Compressed", command=display_program_graph_compressed
)
other_button.grid(row=0, column=2, padx=10)

# Create an output label as a read only
output_label = tk.Text(root, width=40, height=5)
output_label.grid(row=2, column=0, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()
