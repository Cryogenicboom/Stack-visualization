import tkinter as tk
from tkinter import messagebox, simpledialog
from stack import Stack

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class StackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Stack Visualization (Matplotlib)")
        self.stack_size = self.ask_stack_size()
        self.stack = Stack(self.stack_size)
        self.last_pushed_index = None

        self.root.configure(bg="#f0f4f8")

        title = tk.Label(root, text="Stack Visualization", font=("Arial Rounded MT Bold", 20), bg="#f0f4f8", fg="#2d415a")
        title.pack(pady=(10, 0))

        self.input_frame = tk.Frame(root, bg="#f0f4f8")
        self.input_frame.pack(pady=10)

        self.entry = tk.Entry(self.input_frame, width=12, font=("Arial", 14))
        self.entry.pack(side=tk.LEFT, padx=5)

        self.push_button = tk.Button(self.input_frame, text="Push", command=self.push, bg="#4caf50", fg="white", font=("Arial", 12), width=7)
        self.push_button.pack(side=tk.LEFT, padx=5)

        self.pop_button = tk.Button(self.input_frame, text="Pop", command=self.pop, bg="#f44336", fg="white", font=("Arial", 12), width=7)
        self.pop_button.pack(side=tk.LEFT, padx=5)

        self.peek_button = tk.Button(self.input_frame, text="Peek", command=self.peek, bg="#2196f3", fg="white", font=("Arial", 12), width=7)
        self.peek_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(root, text="", fg="#2d415a", bg="#f0f4f8", font=("Arial", 12))
        self.status_label.pack()

        self.mpl_canvas = None
        self.draw_stack_matplotlib()

    def ask_stack_size(self):
        while True:
            try:
                size = simpledialog.askinteger("Stack Size", "Enter stack (array) size (3-10):", minvalue=3, maxvalue=10)
                if size is None:
                    raise Exception("Stack size selection cancelled.")
                return size
            except Exception:
                messagebox.showerror("Input Error", "Please enter a valid stack size between 3 and 10.")

    def push(self):
        value = self.entry.get()
        if value == "":
            messagebox.showwarning("Input Error", "Please enter a value to push.")
            return
        try:
            self.stack.push(value)
            self.last_pushed_index = self.stack.size() - 1
            self.status_label.config(text=f"Pushed: {value}")
        except Exception as e:
            messagebox.showerror("Stack Error", str(e))
        self.entry.delete(0, tk.END)
        self.draw_stack_matplotlib()

    def pop(self):
        try:
            popped = self.stack.pop()
            self.status_label.config(text=f"Popped: {popped}")
            self.last_pushed_index = None
        except Exception as e:
            messagebox.showerror("Stack Error", str(e))
        self.draw_stack_matplotlib()

    def peek(self):
        top = self.stack.peek()
        if top is not None:
            self.status_label.config(text=f"Top: {top}")
        else:
            self.status_label.config(text="Stack is empty.")

    def draw_stack_matplotlib(self):
        # Remove previous canvas if it exists
        if self.mpl_canvas:
            self.mpl_canvas.get_tk_widget().pack_forget()
            self.mpl_canvas = None

        fig, ax = plt.subplots(figsize=(3.5, self.stack_size * 0.7))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, self.stack_size)
        ax.axis('off')

        base_address = 1000
        address_step = 4

        for i in range(self.stack.max_size):
            y = i  # <-- Draw from bottom to top
            rect_color = "#b3e5fc" if i != len(self.stack.items) - 1 else "#ffeb3b"
            edge_color = "#0288d1" if i != len(self.stack.items) - 1 else "#fbc02d"
            rect = plt.Rectangle((0.25, y + 0.1), 0.5, 0.8, facecolor=rect_color, edgecolor=edge_color, linewidth=2)
            ax.add_patch(rect)
            # Value
            if i < len(self.stack.items):
                ax.text(0.5, y + 0.5, str(self.stack.items[i]), ha='center', va='center', fontsize=14, fontweight='bold', color="#2d415a")
                if i == len(self.stack.items) - 1:
                    ax.text(0.8, y + 0.5, "← Top", color="#fbc02d", fontsize=11, fontweight='bold', va='center')
            # Address
            ax.text(0.18, y + 0.5, str(base_address + i * address_step), ha='right', va='center', fontsize=10, color="#607d8b", fontfamily="monospace")
            # Array index
            ax.text(0.95, y + 0.5, f"[{i}]", ha='left', va='center', fontsize=10, color="#607d8b", fontfamily="monospace")

        # Draw stack base line
        ax.plot([0.23, 0.77], [0.1, 0.1], color="#607d8b", linewidth=4)

        plt.tight_layout()
        self.mpl_canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.mpl_canvas.draw()
        self.mpl_canvas.get_tk_widget().pack(pady=10)
        plt.close(fig)

if __name__ == "__main__":
    root = tk.Tk()
    app = StackGUI(root)
    root.mainloop()