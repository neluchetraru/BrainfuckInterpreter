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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
from optimize import (
    brainfuck_loop_unroll,
    memory_range_analysis_1,
    memory_range_analysis_2,
)

memory = Memory()
detect_infinite_loops = True


def run_program():
    code = code_editor.get("1.0", "end-1c")  # Get the code from the text widget
    output_label.delete("1.0", "end")  # Clear the output text widget
    memory.reset()
    inte = Interpreter(memory, 1000 if detect_infinite_loops else 0)
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

    # Label for graph info
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

    memory_access_heat_map_btn = tk.Button(
        viewer_window,
        text="Memory Access Heat Map",
        command=lambda: display_memory_access_heat_map(memory),
    )

    memory_access_heat_map_btn.pack()


def display_memory_access_heat_map(memory):
    memory_accesses = memory.memory_accesses

    heatmap_window = tk.Toplevel()
    heatmap_window.title("Memory Access Heatmap")

    def generate_heatmap(memory_accesses, size):
        data = np.array([memory_accesses]).reshape((1, -1))

        fig, ax = plt.subplots()
        cax = ax.matshow(data, cmap="viridis")

        plt.xticks(np.arange(size), [str(i) for i in range(size)])
        plt.yticks([])  # Assuming you don't need y-axis ticks

        plt.xlabel("Memory Cells")
        plt.ylabel("Memory Accesses")

        plt.title("Memory Access Heatmap")

        plt.colorbar(cax, label="Access Count")

        return fig

    fig = generate_heatmap(memory_accesses, len(memory_accesses))

    canvas = FigureCanvasTkAgg(fig, master=heatmap_window)
    canvas.draw()
    canvas.get_tk_widget().pack()


def handle_loop_unrolling_optimizer():
    code = code_editor.get("1.0", "end-1c")
    output_label.delete("1.0", "end")
    output_label.insert("1.0", "Optimized code: \n" + brainfuck_loop_unroll(code))


def handle_memory_range_analysis_1():
    code = code_editor.get("1.0", "end-1c")

    memory_range_analysis_1_window = tk.Toplevel()
    memory_range_analysis_1_window.title("Memory Range Analysis 1")
    frame = tk.Frame(memory_range_analysis_1_window)

    mem_analysis = memory_range_analysis_1(code)
    for i, mem_cell in enumerate(mem_analysis):
        potential_min, potential_max = min(mem_cell), max(mem_cell)
        entry = tk.Entry(frame, width=8)
        entry.grid(row=i // 10, column=i % 10, padx=2, pady=2)
        entry.insert(tk.END, f"{potential_min} - {potential_max}")

    frame.pack()


def handle_memory_range_analysis_2():
    code = code_editor.get("1.0", "end-1c")

    memory_range_analysis_2_window = tk.Toplevel()
    memory_range_analysis_2_window.title("Memory Range Analysis 2")
    frame = tk.Frame(memory_range_analysis_2_window)

    mem_analysis = memory_range_analysis_2(code)
    for i, mem_cell in enumerate(mem_analysis):
        potential_min, potential_max = min(mem_cell), max(mem_cell)
        entry = tk.Entry(frame, width=8)
        entry.grid(row=i // 10, column=i % 10, padx=2, pady=2)
        entry.insert(tk.END, f"{potential_min} - {potential_max}")

    frame.pack()


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


def generate_program_controls_window():
    global program_controls_window, detect_infinite_loops
    program_controls_window = tk.Toplevel(root)
    program_controls_window.title("Program Controls")
    button_frame = tk.Frame(program_controls_window)
    button_frame.grid(row=0, column=0, padx=10, pady=10)

    # Create a button to run the Brainfuck program and visualize it
    tk.Button(
        button_frame,
        text="Run program",
        command=lambda: Thread(target=run_program).start(),
    ).grid(row=0, column=0, padx=10, pady=5)
    # Create another button in the same frame
    tk.Button(
        button_frame,
        text="Visualize Simple",
        command=lambda: Thread(target=display_program_graph_simple).start(),
    ).grid(row=0, column=1, padx=10, pady=5)

    tk.Button(
        button_frame,
        text="Visualize Compressed",
        command=lambda: Thread(target=display_program_graph_compressed).start(),
    ).grid(row=0, column=2, padx=10)

    tk.Button(
        button_frame,
        text="Open Memory Viewer",
        command=lambda: Thread(target=open_memory_viewer, args=(memory,)).start(),
    ).grid(row=1, column=0, pady=5, padx=10)

    tk.Button(
        button_frame,
        text="Optimize: loop unroll",
        command=handle_loop_unrolling_optimizer,
    ).grid(row=1, column=1, pady=5, padx=10)

    tk.Button(
        button_frame,
        text="Optimize: memory range analysis 1",
        command=lambda: handle_memory_range_analysis_1(),
    ).grid(row=2, column=0, pady=5, padx=10)

    tk.Button(
        button_frame,
        text="Optimize: memory range analysis 2",
        command=lambda: handle_memory_range_analysis_2(),
    ).grid(row=2, column=1, pady=5, padx=10)

    detect_infinite_loops_btn = tk.Button(
        button_frame,
        text="Detect Infinite Loops: " + ("ON" if detect_infinite_loops else "OFF"),
        command=lambda: toggle_detect_infinite_loops(),
    )

    def toggle_detect_infinite_loops():
        global detect_infinite_loops
        detect_infinite_loops = not detect_infinite_loops
        detect_infinite_loops_btn.config(
            text="Detect Infinite Loops: " + ("ON" if detect_infinite_loops else "OFF"),
        )

    detect_infinite_loops_btn.grid(row=1, column=2, pady=5, padx=10)

    return program_controls_window


program_controls_window = generate_program_controls_window()
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
program_controls_button = tk.Button(
    root,
    text="Program Controls",
    command=lambda: generate_program_controls_window()
    if not program_controls_window.winfo_exists()
    else None,
).grid(row=current_row, column=0, padx=10, pady=10)


# Make the window fixed size
root.resizable(False, False)

# Start the Tkinter main loop
root.mainloop()
