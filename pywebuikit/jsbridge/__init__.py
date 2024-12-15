from __future__ import annotations

import typing
import random
from abc import abstractmethod

from .. import webwindow
from .. import public_objects

_TV_PWUIKJEA = typing.TypeVar("_TV_PWUIKJEA", covariant=True)

JS_UNDEFINED: PyWebUIKitJsEvalable = type("JS_UNDEFINED", (), {
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

class JavaScriptVariable:
    def __init__(self, v: str): self.v = v
    def __pywebuikit_jseval__(self) -> str: return self.v

class CanvasRenderingContext2D(JavaScriptVariable): ...
class WebGLRenderingContext(JavaScriptVariable): ...
class WebGL2RenderingContext(JavaScriptVariable): ...
class OffscreenCanvasRenderingContext2D(JavaScriptVariable): ...
class ImageBitmapRenderingContext(JavaScriptVariable): ...

class CanvasCaptureMediaStreamTrack(JavaScriptVariable): ...
class CanvasGradient(JavaScriptVariable): ...
class CanvasPattern(JavaScriptVariable): ...

class Path2D(JavaScriptVariable): ...
class ImageData(JavaScriptVariable): ...
class Element(JavaScriptVariable): ...

class HTMLImageElement(JavaScriptVariable): ...
class SVGImageElement(JavaScriptVariable): ...
class HTMLVideoElement(JavaScriptVariable): ...
class HTMLCanvasElement(JavaScriptVariable): ...
class ImageBitmap(JavaScriptVariable): ...
class OffscreenCanvas(JavaScriptVariable): ...
class VideoFrame(JavaScriptVariable): ...

pyobj_sifytype = (
    PyWebUIKitJsEvalable
    
    | str
    | int
    | float
    | bool
    
    | typing.Iterable
    | typing.Mapping
    
    | None
)

drawable_type = (
    HTMLImageElement
    | SVGImageElement
    | HTMLVideoElement
    | HTMLCanvasElement
    | ImageBitmap
    | OffscreenCanvas
    | VideoFrame
)

def stringify_pyobj(o: pyobj_sifytype) -> str:
    if isinstance(o, PyWebUIKitJsEvalable):
        return o.__pywebuikit_jseval__()
    
    elif isinstance(o, str):
        return webwindow.StringProcesser.replaceString2CodeEval(o)
    elif isinstance(o, int):
        return str(o)
    elif isinstance(o, float):
        return str(o)
    elif isinstance(o, bool):
        return str(o).lower()
    
    elif isinstance(o, typing.Iterable):
        return f"[{",".join(stringify_pyobj(i) for i in o)}]"
    elif isinstance(o, typing.Mapping):
        return f"{"{"}{",".join(f"{webwindow.StringProcesser.replaceString2CodeEval(key)}:{stringify_pyobj(value)}" for key, value in o.items())}{"}"}"
    
    elif isinstance(o, type(None)):
        return "null"
    
    else:
        raise TypeError(f"Unsupported type {type(o)}")

def iterable2jsarray(iterableObject: typing.Iterable[pyobj_sifytype], hasbracket: bool = True) -> str:
    result = ",".join(stringify_pyobj(i) for i in iterableObject)
    return f"[{result}]" if hasbracket else result

def createImageByUrl(window: webwindow.WebWindow, url: str):
    tid = random.randint(0, 2 << 31)
    promise: public_objects.pythonPromise[HTMLImageElement] = public_objects.pythonPromise()
    window.jsapi.set_attr(f"v_{tid}", lambda: promise.resolve(HTMLImageElement(f"v_{tid}")))
    window.evaluate_js(f"v_{tid} = new Image(); v_{tid}.src = {stringify_pyobj(url)}; v_{tid}.onload = () => pywebview.api.call_attr('v_{tid}');")
    return promise

