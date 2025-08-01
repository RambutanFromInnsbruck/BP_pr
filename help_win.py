from tkinter import *
from tkinter import ttk
import json
import tkinter as tk


class HelpWindow():
    def __init__(self, parent):
        self.root = Toplevel(parent)
        self.parent = parent
        self.init()

    def init(self):
        self.root.title("Help")
        self.root.geometry("800x600")
        self.draw_widgets()

    def draw_widgets(self):
        main_frame = Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        srch_frame = Frame(main_frame)
        srch_frame.pack(fill=tk.X, pady=5)

        Label(srch_frame, text="Search:").pack(side=tk.LEFT)
        self.srch_entry = Entry(srch_frame, width=40)
        self.srch_entry.pack(side=tk.LEFT, padx=5)
        self.srch_entry.bind("<KeyRelease>", self.search_content)

        paned_window = PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        self.tree_frame = Frame(paned_window)
        self.tree = ttk.Treeview(self.tree_frame, show="tree")
        self.tree_scroll = Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.content_frame = Frame(paned_window)
        self.content_text = Text(self.content_frame, wrap="word", state="disabled")
        content_scroll = Scrollbar(self.content_frame, command=self.content_text.yview)
        self.content_text.configure(yscrollcommand=content_scroll.set)

        content_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_text.pack(fill=tk.BOTH, expand=True)

        paned_window.add(self.tree_frame, width=200)
        paned_window.add(self.content_frame)

        self.help_data = self.load_help_data()
        self.create_help_structure()
        self.tree.bind("<<TreeviewSelect>>", self.display_content)

    def load_help_data(self):
        filename = "help_data.json"
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def create_help_structure(self):
        root_node = self.help_data.get("Directory", [])
        self._build_tree("", root_node)

    def _build_tree(self, parent_id, nodes):
        for node in nodes:
            item_id = self.tree.insert(
                parent_id,
                "end",
                text=node["title"],
                values=[node["content"]],
                open=False
            )

            if node["children"]:
                self._build_tree(item_id, node["children"])

    def display_content(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        content = self.tree.item(selected, "values")
        self.content_text.config(state="normal")
        self.content_text.delete(1.0, tk.END)

        if content:
            self.content_text.insert(tk.END, content[0])
        self.content_text.config(state="disabled")

    def search_content(self, event):
        query = self.srch_entry.get().lower()

        self.content_text.tag_remove("found", 1.0, tk.END)
        self.content_text.config(state="normal")

        if not query:
            return

        start_index = "1.0"
        while True:
            start_index = self.content_text.search(query, start_index, stopindex=tk.END)
            if not start_index:
                break

            end_index = f"{start_index}+{len(query)}c"

            self.content_text.tag_add("found", start_index, end_index)
            start_index = end_index

        self.content_text.tag_config("found", background="yellow")
        self.content_text.config(state="disabled")