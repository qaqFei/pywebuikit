from __future__ import annotations

import typing
import random
from abc import abstractmethod

from .. import webwindow
from .. import public_objects
from .._real_overload import overload, OverloadMeta

_TV_PWUIKJEA = typing.TypeVar("_TV_PWUIKJEA", covariant=True)
_TV_WEBFILTERFUNC_VALUE = typing.TypeVar("_TV_WEBFILTERFUNC_VALUE", covariant=True)

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
    
    def release_ref(self, window: webwindow.WebWindow):
        """
        if you want to release the reference to the variable in the JavaScript context,
        you can use this method,
        but you should be careful not to use the variable after calling this method
        """
        
        window.evaluate_js(f"delete {self.v};")

class BaseWebFilterFunction(typing.Generic[_TV_WEBFILTERFUNC_VALUE]):
    unit: str = ""
    
    def _strify(self, v: _TV_WEBFILTERFUNC_VALUE) -> str: raise NotImplementedError
    def setvalue(self, v: _TV_WEBFILTERFUNC_VALUE): self.v = v
    def __init__(self, v: _TV_WEBFILTERFUNC_VALUE): self.v = v
    def __pywebuikit_jseval__(self) -> str: return self._strify(stringify_pyobj(self.v))
    
    def __setattr__(self, n, v):
        if n == "_strify": raise AttributeError("cannot change _strify")
        super().__setattr__(n, v)

class WebFilterFunc_URL(BaseWebFilterFunction):
    _strify = lambda self, v: f"url({v}{self.unit})"

class WebFilterFunc_SRC(BaseWebFilterFunction):
    _strify = lambda self, v: f"src({v}{self.unit})"

class WebFilterFunc_Blur(BaseWebFilterFunction):
    unit: str = "px"
    _strify = lambda self, v: f"blur({v}{self.unit})"

class WebFilterFunc_Brightness(BaseWebFilterFunction):
    _strify = lambda self, v: f"brightness({v}{self.unit})"

class WebFilterFunc_Contrast(BaseWebFilterFunction):
    _strify = lambda self, v: f"contrast({v}{self.unit})"

class WebFilterFunc_DropShadow(BaseWebFilterFunction):
    _strify = lambda self, v: f"drop-shadow({v}{self.unit})"

class WebFilterFunc_Grayscale(BaseWebFilterFunction):
    _strify = lambda self, v: f"grayscale({v}{self.unit})"

class WebFilterFunc_HueRotate(BaseWebFilterFunction):
    unit: str = "deg"
    _strify = lambda self, v: f"hue-rotate({v}{self.unit})"

class WebFilterFunc_Invert(BaseWebFilterFunction):
    _strify = lambda self, v: f"invert({v}{self.unit})"

class WebFilterFunc_Opacity(BaseWebFilterFunction):
    _strify = lambda self, v: f"opacity({v}{self.unit})"

class WebFilterFunc_Sepia(BaseWebFilterFunction):
    _strify = lambda self, v: f"sepia({v}{self.unit})"

class WebFilterFunc_Saturate(BaseWebFilterFunction):
    _strify = lambda self, v: f"saturate({v}{self.unit})"

class WebFilterSet:
    def __init__(self, *webfilters: BaseWebFilterFunction):
        self._filters = list(webfilters)
    
    def append(self, webfilter: BaseWebFilterFunction, add: bool = False):
        if not isinstance(webfilter, BaseWebFilterFunction):
            raise TypeError(f"cannot append {type(webfilter)} to filter set")
        
        ft = type(webfilter)
        ts = tuple(type(i) for i in self._filters)
        
        if ft in ts:
            if add:
                self._filters[ts.index(ft)].v += webfilter.v
            else:
                raise ValueError(f"cannot append {type(webfilter)} to filter set")
        else:
            self._filters.append(webfilter)
        
    def remove(self, webfilter: BaseWebFilterFunction):
        self._filters.remove(webfilter)
    
    def empty(self):
        return len(self) == 0
    
    def remove_byType(self, ft: type[BaseWebFilterFunction]):
        self._filters.pop(tuple(type(i) for i in self._filters).index(ft))
    
    def __iter__(self):
        return iter(self._filters)
    
    def __len__(self):
        return len(self._filters)
    
    def __contains__(self, webfilter: BaseWebFilterFunction):
        return webfilter in self._filters
    
    def __pywebuikit_jseval__(self):
        return " ".join(stringify_pyobj(i) for i in self._filters)

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
    window.evaluate_js(f"v_{tid} = new Image(); v_{tid}.onload = () => pywebview.api.call_attr('v_{tid}'); v_{tid}.src = {stringify_pyobj(url)};")
    return promise

def setFilter(window: webwindow.WebWindow, webfilterset: WebFilterSet, element: Element):
    # why call stringify_pyobj twice?
    # 1. stringify_pyobj(webfilterset) -> str (has no quotes)
    # 2. stringify_pyobj(stringify_pyobj(webfilterset)) -> str (has quotes)
    
    window.evaluate_js(f"{element.v}.style.filter = {stringify_pyobj(stringify_pyobj(webfilterset))};")

def removeFilter(window: webwindow.WebWindow, element: Element):
    window.evaluate_js(f"{element.v}.style.filter = '';")