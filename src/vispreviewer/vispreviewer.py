class VisOpResult:
    def __init__(self, success, err_msg):
        self.success = success
        self.err_msg = err_msg
    
    def __iter__(self):
        return iter([self.success, self.err_msg])

def VisOpSuccess():
    return VisOpResult(True, None)

def VisOpFailure(err_msg):
    return VisOpResult(False, err_msg)

class VisPreviewer:
    def __init__(
        self,
        code,
    ): 
        self.code = self._convert_code_to_lines(code)
        self.curr_co_index = -1
        self.curr_code = None
        success, err_msg = self.step()
        if not success:
            err_msg
    
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

    def _step(self):
        self.curr_co_index += 1
        self.curr_code = self.code[self.curr_co_index] if self.curr_co_index < len(self.code) else None

    def _jump(self, lineno):
        self.curr_co_index = lineno - 1
        self.curr_code = self.code[self.curr_co_index] if self.curr_co_index < len(self.code) else None

    def _convert_code_to_lines(code):
        return code.split('\n') if isinstance(code, str) else code