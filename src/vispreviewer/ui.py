import tkinter as tk, easygui as eg
from .vispreviewer import VisPreviewer, null
import threading

class VisUI:
    def __init__(self, fn, code):
        #############################################
        # DEFINITION SECTION
        #############################################

        ############### UI Part ###############
        self.root = tk.Tk()    
        self.terminal = tk.Text(self.root)
        self.error = tk.Text(self.root)
        self.cost_var = tk.StringVar(self.root, str(self.now_cost))
        self.cost_display = tk.Label(self.root, textvariable=self.cost_var)
        ############### Evaluate Part ###############
        self._previewer = VisPreviewer(fn, code, self)
        self.terminal_update_thread = threading.Thread(target=self.update_terminal)

        #############################################
        # INITIALIZATION SECTION
        #############################################
        self.terminal.pack(side='top')
        self.terminal_update_thread.start()

    def update_terminal(self):
        while True:
            self.terminal.config(state=tk.NORMAL)
            self.error.config(state=tk.NORMAL)
            self.terminal.delete(1.0, tk.END)
            self.terminal.insert(1.0, self._previewer.terminal)
            self.error.delete(1.0, tk.END)
            self.error.insert(1.0, self._previewer.stderr)
            self.terminal.config(state=tk.DISABLED)
            self.error.config(state=tk.DISABLED)

    def _get_input(prompt):
        response = eg.enterbox(prompt, 'VisPreviewer input')
        return response if response is not None else ''