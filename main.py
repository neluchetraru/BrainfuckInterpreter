# vis = Visualizer(
#     # "++++++++[>++++[>++>+++]]",
#     # "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.",
#     "++[]--",
#     "Simple",
# )
predefined_programs = {
    "Hello World": "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.",
    "Fibonacci": ">++++++++++>+>+[[+++++[>++++++++<-]>.<++++++[>--------<-]+<<<]>.>>[[-]<[>+<-]>>[<<+>+>-]<[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>[-]>+>+<<<-[>+<-]]]]]]]]]]]+>>>]<<<]",
    "Squares": "++++[>+++++<-]>[<+++++>-]+<+[>[>+>+<<-]++>>[<<+>>-]>>>[-]++>[-]+>>>+[[-]++++++>>>]<<<[[<++++++++<++>>-]+<.<[>----<-]<]<<[>>>>>[>>>[-]+++++++++<[>-<-]+++++++++>[-[<->-]+[<<<]]<[>+<-]>]<<-]<<-]",
}
import tkinter as tk
from Interpreter import Interpreter, Memory
from Visualizer import Visualizer
from Devisualizer import Devisualizer
import time
from threading import Thread
from tkinter import ttk
from utils import ScrollableImage, MemoryViewer

memory = Memory()


def run_program():
    code = code_editor.get("1.0", "end-1c")  # Get the code from the text widget
    output_label.delete("1.0", "end")  # Clear the output text widget
    memory.reset()
    inte = Interpreter(memory)
    time_ = time.time()
    inte.run(code, printer=output_label, inputter=input_label)
    time_ = time.time() - time_

    output_label.insert("end", "\n")
    output_label.insert("end", f"Execution finished in {time_} seconds.")


def display_program_graph_simple():
    code = code_editor.get("1.0", "end-1c")
    vis = Visualizer(code)
    vis.bfp_to_graph()
    vis.viz()

    graph_window = tk.Toplevel(root)
    graph_window.title("Program Graph")
    graph_img = tk.PhotoImage(file=f"./graphs/{vis.name}.png")
    height = min(root.winfo_screenheight() - 100, graph_img.height())
    width = min(root.winfo_screenwidth(), graph_img.width())
    graph_window.geometry(f"{width + 50}x{height+20}")
    image_window = ScrollableImage(
        graph_window,
        image=graph_img,
        height=height,
        width=width,
    )
    devis = Devisualizer(vis)

    button = tk.Button(
        graph_window,
        text="Devisualize",
        command=lambda: handleDevisualizeBtn(graph_window, devis),
        pady=10,
    )

    button.pack()
    image_window.pack()


def handleDevisualizeBtn(gw, devis: Devisualizer):
    gw.destroy()
    devis.graph_to_bfp
    output_label.delete("1.0", "end")
    output_label.insert("1.0", devis.bfp)


def display_program_graph_compressed():
    code = code_editor.get("1.0", "end-1c")
    vis = Visualizer(code)
    vis.bfp_to_graph_compressed()
    vis.viz()

    graph_window = tk.Toplevel(root)
    graph_window.title("Program Graph Compressed")
    graph_img = tk.PhotoImage(file=f"./graphs/{vis.name}.png")
    height = min(root.winfo_screenheight() - 100, graph_img.height())
    width = min(root.winfo_screenwidth(), graph_img.width())
    image_window = ScrollableImage(
        graph_window,
        image=graph_img,
        height=height,
        width=width,
    )

    devis = Devisualizer(vis)

    button = tk.Button(
        graph_window,
        text="Devisualize",
        command=lambda: handleDevisualizeBtn(graph_window, devis),
        pady=10,
    )

    button.pack()
    image_window.pack()


def open_memory_viewer(memory):
    memory.reset()
    viewer_window = tk.Toplevel()
    viewer_window.title("Memory Viewer")

    memory_viewer = MemoryViewer(viewer_window, memory)
    memory_viewer.pack()

    def update_entries():
        memory_viewer.update_entries()
        viewer_window.after(10, update_entries)

    update_entries()


# Create the main application window
root = tk.Tk()
root.title("Brainfuck Interpreter")
current_row = 0

# Predifined program part
menu_frame = tk.Frame(root)
menu_frame.grid(row=current_row, pady=10)
current_row += 1
program_var = tk.StringVar()
program_var.set("Select a program")
program_combobox = ttk.Combobox(
    menu_frame, textvariable=program_var, values=list(predefined_programs.keys())
)
program_combobox.grid(row=0, column=0, padx=10)
# Create a button to load the selected program
load_button = tk.Button(
    menu_frame, text="Load Program", command=lambda: load_program(program_var.get())
)
load_button.grid(row=0, column=1, padx=10)


def load_program(selected_program):
    code_editor.delete("1.0", "end")
    code_editor.insert("1.0", predefined_programs[selected_program])


# Brainfuck program part
label_1 = tk.Label(root, text="Brainfuck Program:", anchor="w")
label_1.grid(row=current_row, column=0, sticky="w", padx=20)
current_row += 1
# Create a text widget for code input
code_editor = tk.Text(root, wrap=tk.WORD, width=50, height=7)
code_editor.grid(row=current_row, column=0, padx=10, pady=10)
current_row += 1

# Create a frame to group the buttons in the same row
button_frame = tk.Frame(root)
button_frame.grid(row=current_row, column=0, padx=10, pady=10)
current_row += 1

# Create a button to run the Brainfuck program and visualize it
run_button = tk.Button(
    button_frame, text="Run program", command=lambda: Thread(target=run_program).start()
)
run_button.grid(row=0, column=0, padx=10, pady=5)
# Create another button in the same frame
other_button = tk.Button(
    button_frame,
    text="Visualize Simple",
    command=lambda: Thread(target=display_program_graph_simple).start(),
)
other_button.grid(row=0, column=1, padx=10, pady=5)
other_button = tk.Button(
    button_frame,
    text="Visualize Compressed",
    command=lambda: Thread(target=display_program_graph_compressed).start(),
)
other_button.grid(row=0, column=2, padx=10)


# Input part
input_frame = tk.Frame(root)
input_frame.grid(row=current_row, column=0, padx=10, pady=10)
current_row += 1

label_1 = tk.Label(input_frame, text="Program Input:", anchor="w")
label_1.grid(row=0, column=0, padx=10, sticky="w")

input_label = tk.Text(input_frame, width=50, height=1)
input_label.grid(row=1, column=0, padx=10, pady=10)

# Output part
output_frame = tk.Frame(root)
output_frame.grid(row=current_row, column=0, padx=10, pady=10)

current_row += 1

label_1 = tk.Label(output_frame, text="Program Output:", anchor="w")
label_1.grid(row=0, column=0, padx=10, sticky="w")

output_label = tk.Text(output_frame, width=50, height=5)
output_label.grid(row=current_row, column=0, padx=10, pady=10)

current_row += 1

open_viewer_button = tk.Button(
    root,
    text="Open Memory Viewer",
    command=lambda: Thread(target=open_memory_viewer, args=(memory,)).start(),
)
open_viewer_button.grid(row=current_row, column=0, pady=10)
current_row += 1

# Make the window fixed size
root.resizable(False, False)

# Start the Tkinter main loop
root.mainloop()
