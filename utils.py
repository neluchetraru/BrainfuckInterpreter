import tkinter as tk


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


class MemoryViewer(tk.Frame):
    def __init__(self, master=None, memory=None):
        super().__init__(master)
        self.master = master
        self.memory = memory
        self.create_widgets()

    def create_widgets(self):
        self.entries = []
        self.labels = []
        for i in range(len(self.memory.memory)):
            label = tk.Label(self, text=f"{i}:", width=5)
            label.grid(row=i // 10, column=i % 10)
            self.labels.append(label)

            entry = tk.Entry(self, width=5)
            entry.grid(row=i // 10, column=i % 10, padx=2, pady=2)
            entry.insert(
                tk.END, str(self.memory.get_memory()[i])
            )  # Display initial values
            self.entries.append(entry)

    def update_entries(self):
        if len(self.entries) != len(self.memory.get_memory()):
            self.entries = []
            self.labels = []
            self.create_widgets()
            return
        for i, entry in enumerate(self.entries):
            current_value = str(self.memory.get_memory()[i])
            entry_value = entry.get()
            if current_value != entry_value:
                entry.delete(0, tk.END)
                entry.insert(tk.END, current_value)
                entry.config(fg="red")  # Highlight updated cells in red
            else:
                entry.config(fg="black")  # Reset color if not updated


def get_graph_nodes_count(path):
    digraph = open(path).readlines()
    nodes = set([])
    for line in digraph:
        temp = line.split("[label=")
        if len(temp) < 2:
            continue
        node0 = int(temp[0].split("->")[0].strip())
        node1 = int(temp[0].split("->")[1].strip())
        nodes.add(node0)
        nodes.add(node1)

    return len(nodes)
