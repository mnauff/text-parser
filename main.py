# interpreter_gui.py
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from interpreter import Interpreter

class CodeInterpreterApp:
    def __init__(self, root):
        self.output_terminal = None
        self.root = root
        self.root.title("Code Interpreter")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        self.run_menu = tk.Menu(self.menubar, tearoff=0)
        self.run_menu.add_command(label="Run", command=self.run_code)
        self.menubar.add_cascade(label="Run", menu=self.run_menu)

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.line_numbers = tk.Text(self.frame, bg='#f3f3f3', fg='gray25', width=4, padx=10, pady=10, font=("Fira Code", 12))
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.code_editor = scrolledtext.ScrolledText(self.frame, bg='white', fg='gray25', insertbackground='gray25',
                                                    selectbackground='grey', padx=10, pady=10, undo=True, font=("Fira Code", 12))
        self.code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.code_editor.bind('<KeyRelease>', self.update_line_numbers)

        self.output_terminal = scrolledtext.ScrolledText(self.root, bg='white', fg='gray25', padx=10, pady=10,
                                                         font=("Fira Code", 12))
        self.output_terminal.pack(fill=tk.BOTH, expand=True)

        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        lines = self.code_editor.get(1.0, tk.END).count('\n')
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        self.line_numbers.tag_configure("center", justify='center', font=("Fira Code", 12))
        self.line_numbers.tag_configure("small", font=("Fira Code", 12))
        for i in range(1, lines + 2):
            self.line_numbers.insert(tk.END, f'{i}\n', "center small")
        self.line_numbers.config(state=tk.DISABLED)


    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
                self.code_editor.delete(1.0, tk.END)
                self.code_editor.insert(tk.END, code)
                self.update_line_numbers()

    def save_file(self):
        file_path = getattr(self, 'file_path', None)
        if file_path:
            code = self.code_editor.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(code)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            code = self.code_editor.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(code)
            self.file_path = file_path

    def run_code(self):
        code = self.code_editor.get("1.0", tk.END)
        interpreter = Interpreter()
        interpreter.execute_command(code, self.output_terminal)

def main():
    root = tk.Tk()
    app = CodeInterpreterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
