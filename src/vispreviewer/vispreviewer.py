SUCCESS = (True, None)

class VisPreviwer:
    def __init__(
        self,
        code,
    ): 
        self.code = self._convert_code_to_lines(code)
        self.curr_co_index = -1
        self.curr_code = None
        success, err_msg = self.step()
    
    def step(self):
        self._step()
        if self.curr_code is None:
            return False, "it's the end of the code!"
        return SUCCESS
    
    def jump(self, lineno):
        self._jump(lineno)
        if self.curr_code is None:
            return False, "the code just have {} lines!"
        return SUCCESS

    def _step(self):
        self.curr_co_index += 1
        self.curr_code = self.code[self.curr_co_index] if self.curr_co_index < len(self.code) else None

    def _jump(self, lineno):
        self.curr_co_index = lineno - 1
        self.curr_code = self.code[self.curr_co_index] if self.curr_co_index < len(self.code) else None

    def _convert_code_to_lines(code):
        return code.split('\n') if isinstance(code, str) else code