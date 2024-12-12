from __future__ import annotations

import typing
from abc import abstractmethod

from .. import webwindow

_TV_PWUIKJEA = typing.TypeVar("_TV_PWUIKJEA", covariant=True)
JS_UNDEFINED = type("JS_UNDEFINED", (), {
    "__bool__": lambda _: False,
    "__str__": lambda _: "undefined",
    "__repr__": lambda _: "undefined",
    "__pywebuikit_jseval__": lambda _: "undefined",
    "__setattr__": lambda self, name, value: None,
    "__delattr__": lambda self, name: None
})()

@typing.runtime_checkable
class PyWebUIKitJsEvalable(typing.Protocol[_TV_PWUIKJEA]):
    @abstractmethod
    def __pywebuikit_jseval__(self) -> str: ...

class BaseRender:
    def __init__(self, window: webwindow.WebWindow):
        self.window = window
        self.ctxname = "ctx"
        self._drawmethods = []
    
    def reg_drawMethod(self, name: str, jsfunc: str):
        self._drawmethods.append((name, jsfunc))
    
    def draw(self, method: str, *args: tuple[evalable_type_aliases]):
        return self.window.evaluate_js(f"{self.ctxname}.{method}({",".join(self.format_args(args))});")
    
    def format_args(self, args: evalable_type_aliases):
        for arg in args:
            if hasattr(arg, "__pywebuikit_jseval__"):
                yield arg.__pywebuikit_jseval__()
            elif isinstance(arg, str):
                yield webwindow.StringProcesser.replaceString2CodeEval(arg)
            elif isinstance(arg, int):
                yield str(arg)
            elif isinstance(arg, float):
                yield str(arg)
            elif isinstance(arg, bool):
                yield str(arg).lower()
            elif isinstance(arg, dict):
                yield f"{"{"}{",".join(f"{webwindow.StringProcesser.replaceString2CodeEval(key)}:{self.format_args(value)}" for key, value in arg.items())}{"}"}"
            elif isinstance(arg, type(None)):
                yield "null"
            elif isinstance(arg, BaseRender):
                yield arg.ctxname
            elif hasattr(arg, "__iter__"):
                yield f"[{",".join(self.format_args(arg))}]"
            else:
                raise TypeError(f"Unsupported type {type(arg)}")

class MoreMethodsRender(BaseRender):
    def __init__(self, window: webwindow.WebWindow):
        super().__init__(window)

evalable_type_aliases = (
    str
    | int
    | float
    | bool
    | dict
    | None
    | BaseRender
    | typing.Iterable
    | PyWebUIKitJsEvalable
)