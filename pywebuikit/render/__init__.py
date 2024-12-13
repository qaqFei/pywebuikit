from __future__ import annotations

import typing
from abc import abstractmethod
from typing_extensions import overload

from .. import webwindow
from .. import jscodes

_TV_PWUIKJEA = typing.TypeVar("_TV_PWUIKJEA", covariant=True)
JS_UNDEFINED = type("JS_UNDEFINED", (), {
    "__bool__": lambda _: False,
    "__str__": lambda _: "undefined",
    "__repr__": lambda _: "undefined",
    "__pywebuikit_jseval__": lambda _: "undefined",
    "__setattr__": lambda self, name, value: None,
    "__delattr__": lambda self, name: None
})()

numtype = int|float
fillRuleType = typing.Literal["nonzero", "evenodd"]
repetitionType = typing.Literal["repeat", "repeat-x", "repeat-y", "no-repeat"]

@typing.runtime_checkable
class PyWebUIKitJsEvalable(typing.Protocol[_TV_PWUIKJEA]):
    @abstractmethod
    def __pywebuikit_jseval__(self) -> str: ...

class JavaScriptVariable:
    def __init__(self, vn: str): self.vn = vn
    def __pywebuikit_jseval__(self) -> str: return self.vn
    
class Path2D(JavaScriptVariable): ...
class ImageData(JavaScriptVariable): ...
class WebJsImage(JavaScriptVariable): ...
class Element(JavaScriptVariable): ...

class BaseRender:
    def __init__(self, window: webwindow.WebWindow):
        self.window = window
        self.ctxname = "ctx"
    
    def reg_drawMethod(self, prototype: str, name: str, jsfunc: str):
        return self.window.evaluate_js(f"{prototype}.{name} = ({jsfunc});")
    
    def call_method(self, method: str, *args: tuple[evalable_type_aliases]):
        return self.window.evaluate_js(f"{self.ctxname}.{method}({",".join(self.format_args(args))});")
    
    def format_args(self, args: evalable_type_aliases):
        for arg in args:
            if isinstance(arg, PyWebUIKitJsEvalable):
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

class Context2DRender(BaseRender):
    def create_mainCanvas(self):
        return self.window.evaluate_js(jscodes.CREATE_2DCANVAS)
    
    def setAttribute(self, name: str, value: evalable_type_aliases):
        return self.window.evaluate_js(f"{self.ctxname}.{name} = ({next(iter(self.format_args([value])))});")
    
    def getAttribute(self, name: str):
        return self.window.evaluate_js(f"{self.ctxname}.{name};")
    
    @overload
    def arc(self, x: numtype, y: numtype, radius: numtype, startAngle: numtype, endAngle: numtype):
        return self.call_method("arc", x, y, radius, startAngle, endAngle)
    
    @overload
    def arc(self, x: numtype, y: numtype, radius: numtype, startAngle: numtype, endAngle: numtype, anticlockwise: bool = False):
        return self.call_method("arc", x, y, radius, startAngle, endAngle, anticlockwise)
    
    def arcTo(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype, radius: numtype):
        return self.call_method("arcTo", x1, y1, x2, y2, radius)
    
    def beginPath(self):
        return self.call_method("beginPath")
    
    def bezierCurveTo(self, cp1x: numtype, cp1y: numtype, cp2x: numtype, cp2y: numtype, x: numtype, y: numtype):
        return self.call_method("bezierCurveTo", cp1x, cp1y, cp2x, cp2y, x, y)
    
    def clearRect(self, x: numtype, y: numtype, width: numtype, height: numtype):
        return self.call_method("clearRect", x, y, width, height)
    
    @overload
    def clip(self):
        return self.call_method("clip")
    
    @overload
    def clip(self, path: Path2D):
        return self.call_method("clip", path)
    
    @overload
    def clip(self, fillRule: fillRuleType):
        return self.call_method("clip", fillRule)

    @overload
    def clip(self, path: Path2D, fillRule: fillRuleType):
        return self.call_method("clip", path, fillRule)
    
    @overload
    def closePath(self):
        return self.call_method("closePath")
    
    def createConicGradient(self, startAngle: numtype, x: numtype, y: numtype):
        return self.call_method("createConicGradient", startAngle, x, y)
    
    @overload
    def createImageData(self, width: numtype, height: numtype):
        return self.call_method("createImageData", width, height)

    @overload
    def createImageData(self, width: numtype, height: numtype, setting: PyWebUIKitJsEvalable):
        return self.call_method("createImageData", width, height, setting)
    
    @overload
    def createImageData(self, imagedata: ImageData):
        return self.call_method("createImageData", imagedata)
    
    def createLinearGradient(self, x0: numtype, y0: numtype, x1: numtype, y1: numtype):
        return self.call_method("createLinearGradient", x0, y0, x1, y1)
    
    def createPattern(self, image: WebJsImage, repetition: repetitionType):
        return self.call_method("createPattern", image, repetition)
    
    def createRadialGradient(self, x0: numtype, y0: numtype, r0: numtype, x1: numtype, y1: numtype, r1: numtype):
        return self.call_method("createRadialGradient", x0, y0, r0, x1, y1, r1)
    
    @overload
    def drawFocusIfNeeded(self, element: Element):
        return self.call_method("drawFocusIfNeeded", element)
    
    @overload
    def drawFocusIfNeeded(self, element: Element, path: Path2D):
        return self.call_method("drawFocusIfNeeded", element, path)
    
    @overload
    def drawImage(self, image: WebJsImage, dx: numtype, dy: numtype):
        return self.call_method("drawImage", image, dx, dy)

    @overload
    def drawImage(self, image: WebJsImage, dx: numtype, dy: numtype, dWidth: numtype, dHeight: numtype):
        return self.call_method("drawImage", image, dx, dy, dWidth, dHeight)
    
    @overload
    def drawImage(self, image: WebJsImage, sx: numtype, sy: numtype, sWidth: numtype, sHeight: numtype, dx: numtype, dy: numtype, dWidth: numtype, dHeight: numtype):
        return self.call_method("drawImage", image, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight)
    
    def ellipse(self, x: numtype, y: numtype, radiusX: numtype, radiusY: numtype, rotation: numtype, startAngle: numtype, endAngle: numtype, counterclockwise: bool = False):
        return self.call_method("ellipse", x, y, radiusX, radiusY, rotation, startAngle, endAngle, counterclockwise)
    
    @overload
    def fill(self):
        return self.call_method("fill")

    @overload
    def fill(self, path: Path2D):
        return self.call_method("fill", path)
    
    @overload
    def fill(self, fillRule: fillRuleType):
        return self.call_method("fill", fillRule)
    
    @overload
    def fill(self, path: Path2D, fillRule: fillRuleType):
        return self.call_method("fill", path, fillRule)
    
    def fillRect(self, x: numtype, y: numtype, width: numtype, height: numtype):
        return self.call_method("fillRect", x, y, width, height)
    
    @overload
    def fillText(self, text: str, x: numtype, y: numtype):
        return self.call_method("fillText", text, x, y)
    
    @overload
    def fillText(self, text: str, x: numtype, y: numtype, maxWidth: numtype):
        return self.call_method("fillText", text, x, y, maxWidth)
    
    def getContextAttributes(self):
        return self.call_method("getContextAttributes")
    
    @overload
    def getImageData(self, sx: numtype, sy: numtype, sw: numtype, sh: numtype):
        return self.call_method("getImageData", sx, sy, sw, sh)
    
    @overload
    def getImageData(self, sx: numtype, sy: numtype, sw: numtype, sh: numtype, settings: PyWebUIKitJsEvalable):
        return self.call_method("getImageData", sx, sy, sw, sh, settings)
    
    def getLineDash(self):
        return self.call_method("getLineDash")
    
    def getTransform(self):
        return self.call_method("getTransform")
    
    def isContextLost(self):
        return self.call_method("isContextLost")
    
    @overload
    def isPointInPath(self, x: numtype, y: numtype):
        return self.call_method("isPointInPath", x, y)
    
    @overload
    def isPointInPath(self, x: numtype, y: numtype, fillRule: fillRuleType):
        return self.call_method("isPointInPath", x, y, fillRule)

    @overload
    def isPointInPath(self, path: Path2D, x: numtype, y: numtype):
        return self.call_method("isPointInPath", path, x, y)

    @overload
    def isPointInPath(self, path: Path2D, x: numtype, y: numtype, fillRule: fillRuleType):
        return self.call_method("isPointInPath", path, x, y, fillRule)
    
    @overload
    def isPointInStroke(self, x: numtype, y: numtype):
        return self.call_method("isPointInStroke", x, y)

    @overload
    def isPointInStroke(self, path: Path2D, x: numtype, y: numtype):
        return self.call_method("isPointInStroke", path, x, y)
    
    def lineTo(self, x: numtype, y: numtype):
        return self.call_method("lineTo", x, y)
    
    def measureText(self, text: str):
        return self.call_method("measureText", text)
    
    def moveTo(self, x: numtype, y: numtype):
        return self.call_method("moveTo", x, y)
    
    @overload
    def putImageData(self, imageData: ImageData, dx: numtype, dy: numtype):
        return self.call_method("putImageData", imageData, dx, dy)

    @overload
    def putImageData(self, imageData: ImageData, dx: numtype, dy: numtype, dirtyX: numtype, dirtyY: numtype, dirtyWidth: numtype, dirtyHeight: numtype):
        return self.call_method("putImageData", imageData, dx, dy, dirtyX, dirtyY, dirtyWidth, dirtyHeight)
    
    def quadraticCurveTo(self, cpx: numtype, cpy: numtype, x: numtype, y: numtype):
        return self.call_method("quadraticCurveTo", cpx, cpy, x, y)
    
    def rect(self, x: numtype, y: numtype, width: numtype, height: numtype):
        return self.call_method("rect", x, y, width, height)
    
    def reset(self):
        return self.call_method("reset")
    
    def resetTransform(self):
        return self.call_method("resetTransform")
    
    def restore(self):
        return self.call_method("restore")
    
    def rotate(self, angle: numtype):
        return self.call_method("rotate", angle)
    
    def roundRect(self, x: numtype, y: numtype, width: numtype, height: numtype, radii: numtype|list[numtype]):
        return self.call_method("roundRect", x, y, width, height, radii)
    
    def save(self):
        return self.call_method("save")
    
    def scale(self, x: numtype, y: numtype):
        return self.call_method("scale", x, y)
    
    def setLineDash(self, segments: list[numtype]):
        return self.call_method("setLineDash", segments)
    
    @overload
    def setTransform(self, a: numtype, b: numtype, c: numtype, d: numtype, e: numtype, f: numtype):
        return self.call_method("setTransform", a, b, c, d, e, f)
    
    @overload
    def setTransform(self, matrix: list):
        return self.call_method("setTransform", matrix)
    
    @overload
    def stroke(self):
        return self.call_method("stroke")

    @overload
    def stroke(self, path: Path2D):
        return self.call_method("stroke", path)
    
    @overload
    def strokeRect(self, x: numtype, y: numtype, width: numtype, height: numtype):
        return self.call_method("strokeRect", x, y, width, height)
    
    @overload
    def strokeText(self, text: str, x: numtype, y: numtype):
        return self.call_method("strokeText", text, x, y)
    
    @overload
    def strokeText(self, text: str, x: numtype, y: numtype, maxWidth: numtype):
        return self.call_method("strokeText", text, x, y, maxWidth)
    
    @overload
    def transform(self, a: numtype, b: numtype, c: numtype, d: numtype, e: numtype, f: numtype):
        return self.call_method("transform", a, b, c, d, e, f)
    
    def translate(self, x: numtype, y: numtype):
        return self.call_method("translate", x, y)
    
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