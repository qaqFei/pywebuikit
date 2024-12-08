from .. import webwindow

class BaseRender:
    def __init__(self, window: webwindow.WebWindow):
        self.window = window
        self.ctxname = "ctx"
        self._drawmethods = []
    
    def reg_drawMethod(self, name: str, jsfunc: str):
        self._drawmethods.append((name, jsfunc))
    
    def draw(self, method: str, *args):
        return self.window.evaluate_js(f"{self.ctxname}.{method}({",".join(self.format_args(args))});")
    
    def format_args(self, args):
        for arg in args:
            if isinstance(arg, str):
                yield webwindow.StringProcesser.replaceString2CodeEval(arg)
            elif isinstance(arg, int):
                yield str(arg)
            elif isinstance(arg, float):
                yield str(arg)
            elif isinstance(arg, bool):
                yield str(arg).lower()
            elif isinstance(arg, list):
                yield f"[{",".join(self.format_args(arg))}]"
            elif isinstance(arg, tuple):
                yield f"({",".join(self.format_args(arg))})"
            elif isinstance(arg, set):
                yield f"[{",".join(self.format_args(arg))}]"
            elif isinstance(arg, dict):
                yield f"{"{"}{",".join(f"{webwindow.StringProcesser.replaceString2CodeEval(key)}:{value}" for key, value in arg.items())}{"}"}"
            elif isinstance(arg, type(None)):
                yield "null"
            elif isinstance(arg, BaseRender):
                yield arg.ctxname
            else:
                if hasattr(arg, "__pywebuikit_jseval__"):
                    yield arg.__pywebuikit_jseval__()
                else:
                    raise TypeError(f"Unsupported type {type(arg)}")

class MoreMethodsRender(BaseRender):
    def __init__(self, window: webwindow.WebWindow):
        super().__init__(window)