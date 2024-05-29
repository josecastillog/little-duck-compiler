import tkinter as tk
from tkinter import scrolledtext
import subprocess
import sys
import lex
import importlib

class CodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Editor")

        # Set default window size
        self.root.geometry("1600x1300")  # width x height

        # Create code editor area
        self.code_editor = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.code_editor.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Create a larger and styled run button
        self.run_button = tk.Button(self.root, text="Run Code", command=self.run_code, width=20, height=2, font=('Helvetica', 12, 'bold'))
        self.run_button.pack(pady=10)

        # Create output display area
        self.output_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=10, state=tk.DISABLED)
        self.output_display.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    def run_code(self):
        self.output_display.insert(tk.END, "Output:\n" + "Loading..." + "\n")

        code = self.code_editor.get("1.0", tk.END)
        self.output_display.config(state=tk.NORMAL)
        self.output_display.delete("1.0", tk.END)
        
        importlib.reload(lex)
        output = lex.run(code)

        def list_to_string_with_line_breaks(lst):
            return "\n".join(str(element) for element in lst)

        # try:
        #     # Run the code and capture output and errors
        #     result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
        #     output = result.stdout
        #     error = result.stderr
        # except subprocess.CalledProcessError as e:
        #     output = e.stdout
        #     error = e.stderr
        output = list_to_string_with_line_breaks(output)
        # Display output and errors
        if output:
            self.output_display.insert(tk.END, "Output:\n" + output + "\n")
        # if error:
        #     self.output_display.insert(tk.END, "Error:\n" + error + "\n")
        
        self.output_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditorApp(root)
    root.mainloop()
