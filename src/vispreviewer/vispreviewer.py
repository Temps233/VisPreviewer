import sys
import traceback as tb
import tkinter as tk
import time
from .ui import VisUI

class NULL: 
    def __repr__(self): return "null"

null = NULL()

class VisPreviwerSupportingError(NotImplementedError): ...

class VisOpResult:
    def __init__(self, success, err_msg):
        self.success = success
        self.err_msg = err_msg
    
    def __iter__(self):
        return iter([self.success, self.err_msg])

def vis_not_support(exact_feature):
    raise VisPreviwerSupportingError(f"VisPreviewer do not support the feature ({exact_feature}) now.")

def vis_print(self):
    def print(*values, sep=' ', end='\n', file, flush=True):
        if file != sys.stdout:
            vis_not_support("printing to streams except sys.stdout")
        elif flush == False:
            vis_not_support("printing with flush=False")
        self.terminal += sep.join(map(str, values)) + end
    return print

def vis_input(self):
    def input(prompt=''):
        return self._read(prompt)
    return input

def vis_open():
    def open(*args, **kwargs) -> NULL:
        vis_not_support("opening files")
    return open

def VisOpSuccess():
    return VisOpResult(True, None)

def VisOpFailure(err_msg):
    return VisOpResult(False, err_msg)

class VisPreviewer:
    def __init__(
        self,
        fn: str | list,
        code: str,
        ui: VisUI,
    ): 
        self.fn = fn
        self.ui = ui
        self.ui.terminal.config(state=tk.DISABLED)
        self.code = self._convert_code_to_lines(code)
        self.globals = {
            "print": vis_print(self),
            "open": vis_open(),
            "input": vis_input(self)
        }
        self.locals = {
            "print": vis_print(self),
            "open": vis_open(),
            "input": vis_input(self)
        }
        self.terminal = ""
        self.stderr = ""
        self.curr_co_index = -1
        self.curr_code = None
        self._step()

    def step(self):
        self._step()
        if self.curr_code is None:
            return VisOpFailure("it's the end of the code!")
        return VisOpSuccess()
    
    def jump(self, lineno):
        self._jump(lineno)
        if self.curr_code is None:
            return VisOpFailure("the code just have {} lines!")
        return VisOpSuccess()

    def eval(self):
        cost = self._eval()
        self.ui.cost_var.set(str(cost)+'ns')

    def _step(self):
        self.curr_co_index += 1
        self.curr_code = self.code[self.curr_co_index] if self.curr_co_index < len(self.code) else None

    def _jump(self, lineno):
        self.curr_co_index = lineno - 1
        self.curr_code = self.code[self.curr_co_index] if self.curr_co_index < len(self.code) else None

    def _read(self, prompt):
        self.ui._get_input(prompt)

    def _eval(self):
        try:
            start = time.perf_counter_ns()
            exec(compile(("\n"*self.curr_co_index)+self.curr_code, self.fn), self.globals, self.locals)
            end = time.perf_counter_ns()
        except BaseException:
            self.stderr += tb.format_exc() + '\n'
            return null
        else:
            return end - start

    def _convert_code_to_lines(code):
        return code.split('\n') if isinstance(code, str) else code