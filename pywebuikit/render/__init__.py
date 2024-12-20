from __future__ import annotations

import typing
import math
import time
import random
from abc import abstractmethod

from .. import webwindow
from .. import jscodes
from .. import jsbridge
from .. import public_objects
from ..render import render_items
from .._real_overload import overload, OverloadMeta

_TV_RENDERITEM = typing.TypeVar("_TV_RENDERITEM", covariant=True)

numtype = public_objects.numtype
fillRuleType = typing.Literal["nonzero", "evenodd"]
repetitionType = typing.Literal["repeat", "repeat-x", "repeat-y", "no-repeat"]
    
@typing.runtime_checkable
class RenderItem(typing.Protocol[_TV_RENDERITEM]):
    @abstractmethod
    def update(self, t: numtype) -> typing.Any: ...
    
    @abstractmethod
    def itemType(self) -> str: ...

class Canvas2D_SaveState:
    def __init__(self, ctx: Context2DRender): self.ctx = ctx
    def __enter__(self): self.ctx.save()
    def __exit__(self, *args): self.ctx.restore()

class BaseRender:
    def __init__(self, window: webwindow.WebWindow, ctx: str|jsbridge.CanvasRenderingContext2D = "ctx"):
        self.window = window
        self.ctx = jsbridge.CanvasRenderingContext2D(ctx) if isinstance(ctx, str) else ctx
        self.call_hooks: dict[str, typing.Callable[[tuple[jsbridge.pyobj_sifytype]], typing.Any]] = {}
    
    def call_method(self, method: str, *args: tuple[jsbridge.pyobj_sifytype]):
        hook_do, hook_value = self.call_hooks[method](args) if method in self.call_hooks else (None, None)
        code = f"{jsbridge.stringify_pyobj(self)}.{method}({jsbridge.iterable2jsarray(args, False)});"
        
        match hook_do:
            case None: ...
            case "cancel": return
            case "change_code": code = hook_value(code)
        
        return self.window.evaluate_js(code)
    
    def create_canvasRef(self):
        vn = f"cvref__{random.randint(0, 2 << 31)}"
        self.window.evaluate_js(f"{vn} = {jsbridge.stringify_pyobj(self)}.canvas;")
        return jsbridge.Element(vn)
    
    def __pywebuikit_jseval__(self):
        return jsbridge.stringify_pyobj(self.ctx)
    
class Context2DRender(BaseRender, metaclass=OverloadMeta):
    def create_mainCanvas(self):
        return self.window.evaluate_js(jscodes.create_2DCanvas)
    
    def setAttribute(self, name: str, value: jsbridge.pyobj_sifytype):
        return self.window.evaluate_js(f"{jsbridge.stringify_pyobj(self)}.{name} = ({jsbridge.stringify_pyobj(value)});")
    
    def getAttribute(self, name: str):
        return self.window.evaluate_js(f"{jsbridge.stringify_pyobj(self)}.{name};")
    
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
    def clip(self, path: jsbridge.Path2D):
        return self.call_method("clip", path)
    
    @overload
    def clip(self, fillRule: fillRuleType):
        return self.call_method("clip", fillRule)

    @overload
    def clip(self, path: jsbridge.Path2D, fillRule: fillRuleType):
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
    def createImageData(self, width: numtype, height: numtype, setting: jsbridge.PyWebUIKitJsEvalable):
        return self.call_method("createImageData", width, height, setting)
    
    @overload
    def createImageData(self, imagedata: jsbridge.ImageData):
        return self.call_method("createImageData", imagedata)
    
    def createLinearGradient(self, x0: numtype, y0: numtype, x1: numtype, y1: numtype):
        return self.call_method("createLinearGradient", x0, y0, x1, y1)
    
    def createPattern(self, image: jsbridge.drawable_type, repetition: repetitionType):
        return self.call_method("createPattern", image, repetition)
    
    def createRadialGradient(self, x0: numtype, y0: numtype, r0: numtype, x1: numtype, y1: numtype, r1: numtype):
        return self.call_method("createRadialGradient", x0, y0, r0, x1, y1, r1)
    
    @overload
    def drawFocusIfNeeded(self, element: jsbridge.Element):
        return self.call_method("drawFocusIfNeeded", element)
    
    @overload
    def drawFocusIfNeeded(self, element: jsbridge.Element, path: jsbridge.Path2D):
        return self.call_method("drawFocusIfNeeded", element, path)
    
    @overload
    def drawImage(self, image: jsbridge.drawable_type, dx: numtype, dy: numtype):
        return self.call_method("drawImage", image, dx, dy)

    @overload
    def drawImage(self, image: jsbridge.drawable_type, dx: numtype, dy: numtype, dWidth: numtype, dHeight: numtype):
        return self.call_method("drawImage", image, dx, dy, dWidth, dHeight)
    
    @overload
    def drawImage(self, image: jsbridge.drawable_type, sx: numtype, sy: numtype, sWidth: numtype, sHeight: numtype, dx: numtype, dy: numtype, dWidth: numtype, dHeight: numtype):
        return self.call_method("drawImage", image, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight)
    
    def ellipse(self, x: numtype, y: numtype, radiusX: numtype, radiusY: numtype, rotation: numtype, startAngle: numtype, endAngle: numtype, counterclockwise: bool = False):
        return self.call_method("ellipse", x, y, radiusX, radiusY, rotation, startAngle, endAngle, counterclockwise)
    
    @overload
    def fill(self):
        return self.call_method("fill")

    @overload
    def fill(self, path: jsbridge.Path2D):
        return self.call_method("fill", path)
    
    @overload
    def fill(self, fillRule: fillRuleType):
        return self.call_method("fill", fillRule)
    
    @overload
    def fill(self, path: jsbridge.Path2D, fillRule: fillRuleType):
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
    def getImageData(self, sx: numtype, sy: numtype, sw: numtype, sh: numtype, settings: jsbridge.PyWebUIKitJsEvalable):
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
    def isPointInPath(self, path: jsbridge.Path2D, x: numtype, y: numtype):
        return self.call_method("isPointInPath", path, x, y)

    @overload
    def isPointInPath(self, path: jsbridge.Path2D, x: numtype, y: numtype, fillRule: fillRuleType):
        return self.call_method("isPointInPath", path, x, y, fillRule)
    
    @overload
    def isPointInStroke(self, x: numtype, y: numtype):
        return self.call_method("isPointInStroke", x, y)

    @overload
    def isPointInStroke(self, path: jsbridge.Path2D, x: numtype, y: numtype):
        return self.call_method("isPointInStroke", path, x, y)
    
    def lineTo(self, x: numtype, y: numtype):
        return self.call_method("lineTo", x, y)
    
    def measureText(self, text: str):
        return self.call_method("measureText", text)
    
    def moveTo(self, x: numtype, y: numtype):
        return self.call_method("moveTo", x, y)
    
    @overload
    def putImageData(self, imageData: jsbridge.ImageData, dx: numtype, dy: numtype):
        return self.call_method("putImageData", imageData, dx, dy)

    @overload
    def putImageData(self, imageData: jsbridge.ImageData, dx: numtype, dy: numtype, dirtyX: numtype, dirtyY: numtype, dirtyWidth: numtype, dirtyHeight: numtype):
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
    def stroke(self, path: jsbridge.Path2D):
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

class Context2DRender_Extended(Context2DRender):
    def __init__(self, window):
        super().__init__(window)
        
        self.savestate = Canvas2D_SaveState(self)
        self.window.evaluate_js(jscodes.c2d_extend)
    
    def pos2size(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype):
        return (
            min(x1, x2),
            min(y1, y2),
            abs(x1 - x2),
            abs(y1 - y2)
        )
    
    def clear(self):
        return self.clearRect(
            0, 0,
            jsbridge.JavaScriptVariable(f"{jsbridge.stringify_pyobj(self)}.canvas.width"),
            jsbridge.JavaScriptVariable(f"{jsbridge.stringify_pyobj(self)}.canvas.height")
        )
    
    def rotateByDegrees(self, deg: numtype):
        return self.rotate(deg * math.pi / 180)
    
    def drawLineEx(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype, width: numtype, color: str):
        with self.savestate:
            self.setAttribute("strokeStyle", color)
            self.setAttribute("lineWidth", width)
            self.beginPath()
            self.moveTo(x1, y1)
            self.lineTo(x2, y2)
            self.stroke()
    
    def drawImageCenter(self, image: jsbridge.drawable_type, x: numtype, y: numtype, width: numtype, height: numtype):
        return self.drawImage(image, x - width / 2, y - height / 2, width, height)
    
    def drawRotateImageCenter(self, image: jsbridge.drawable_type, x: numtype, y: numtype, width: numtype, height: numtype, deg: numtype):
        with self.savestate:
            if deg != 0.0:
                self.translate(x, y)
                self.rotateByDegrees(deg)
                return self.drawImage(image, -width / 2, -height / 2, width, height)
            
            return self.drawImage(image, x - width / 2, y - height / 2, width, height)
    
    def drawAlphaImage(self, image: jsbridge.drawable_type, x: numtype, y: numtype, width: numtype, height: numtype, alpha: numtype):
        with self.savestate:
            self.setAttribute("globalAlpha", alpha)
            return self.drawImage(image, x, y, width, height)
    
    def drawTextEx(self, text: str, x: numtype, y: numtype, font: str, color: str, baseLine: str, align: str):
        with self.savestate:
            self.setAttribute("fillStyle", color)
            self.setAttribute("textAlign", align)
            self.setAttribute("textBaseline", baseLine)
            self.setAttribute("font", font)
            self.fillText(text, x, y)
    
    def drawRotateText(self, text: str, x: numtype, y: numtype, deg: numtype, font: str, color: str):
        with self.savestate:
            self.translate(x, y)
            self.rotateByDegrees(deg)
            return self.drawTextEx(text, 0, 0, font, color, "middle", "center")
    
    def fillRectEx_BySize(self, x: numtype, y: numtype, width: numtype, height: numtype, color: str):
        with self.savestate:
            self.setAttribute("fillStyle", color)
            return self.fillRect(x, y, width, height)
    
    def fillRectEx_ByPos(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype, color: str):
        x, y, width, height = self.pos2size(x1, y1, x2, y2)
        return self.fillRectEx_BySize(x, y, width, height, color)
    
    def roundRectEx_BySize(self, x: numtype, y: numtype, width: numtype, height: numtype, r: numtype | list[numtype], color: str):
        with self.savestate:
            self.setAttribute("fillStyle", color)
            self.beginPath()
            self.roundRect(x, y, width, height, r)
            self.fill()
    
    def roundRectEx_ByPos(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype, r: numtype | list[numtype], color: str):
        x, y, width, height = self.pos2size(x1, y1, x2, y2)
        return self.roundRectEx_BySize(x, y, width, height, r, color)
    
    def diagonalRect_BySize(self, x: numtype, y: numtype, width: numtype, height: numtype, power: numtype):
        self.moveTo(x + width * power, y)
        self.lineTo(x + width, y)
        self.lineTo(x + width - width * power, y + height)
        self.lineTo(x, y + height)
        self.lineTo(x + width * power, y)
    
    def diagonalRect_ByPos(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype, power: numtype):
        x, y, width, height = self.pos2size(x1, y1, x2, y2)
        return self.diagonalRect_BySize(x, y, width, height, power)
    
    def clipDiagonalRect_BySize(self, x: numtype, y: numtype, width: numtype, height: numtype, power: numtype):
        self.beginPath()
        self.diagonalRect_BySize(x, y, width, height, power)
        self.clip()
    
    def clipDiagonalRect_ByPos(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype, power: numtype):
        x, y, width, height = self.pos2size(x1, y1, x2, y2)
        return self.clipDiagonalRect_BySize(x, y, width, height, power)
    
    def clipRect_BySize(self, x: numtype, y: numtype, width: numtype, height: numtype):
        self.beginPath()
        self.rect(x, y, width, height)
        self.clip()

    def clipRect_ByPos(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype):
        x, y, width, height = self.pos2size(x1, y1, x2, y2)
        return self.clipRect_BySize(x, y, width, height)
    
    def drawDiagonalRect_BySize(self, x: numtype, y: numtype, width: numtype, height: numtype, power: numtype, color: str):
        with self.savestate:
            self.setAttribute("fillStyle", color)
            self.beginPath()
            self.diagonalRect_BySize(x, y, width, height, power)
            self.fill()

    def drawDiagonalRect_ByPos(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype, power: numtype, color: str):
        x, y, width, height = self.pos2size(x1, y1, x2, y2)
        return self.drawDiagonalRect_BySize(x, y, width, height, power, color)

    def drawTriangle(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype, x3: numtype, y3: numtype, color: str):
        with self.savestate:
            self.setAttribute("fillStyle", color)
            self.beginPath()
            self.moveTo(x1, y1)
            self.lineTo(x2, y2)
            self.lineTo(x3, y3)
            self.lineTo(x1, y1)
            self.fill()
    
    def drawTriangleFrame(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype, x3: numtype, y3: numtype, color: str, width: numtype):
        with self.savestate:
            self.setAttribute("strokeStyle", color)
            self.setAttribute("lineWidth", width)
            self.beginPath()
            self.moveTo(x1, y1)
            self.lineTo(x2, y2)
            self.lineTo(x3, y3)
            self.lineTo(x1, y1)
            self.stroke()

class Timer:
    def __init__(self, max: numtype|None = None, maxdo: typing.Literal["tozero", "stop"] = "tozero"):
        self.max = max
        self.maxdo = maxdo
        self.tozero()
    
    def tozero(self):
        self.st = time.time()
    
    def now(self):
        t = time.time() - self.st
        
        if self.max is not None and t > self.max:
            match self.maxdo:
                case "tozero":
                    self.tozero()
                case "stop":
                    t = self.max
                    
        return t

class Canvas2DRenderManager:
    def __init__(self, canvas_render: Context2DRender_Extended, items: list[RenderItem]|None = None):
        self.timer = Timer()
        self.canvas_render = canvas_render
        self.items: list[RenderItem] = [] if items is None else items.copy()
        self.renderMethods: dict[str, typing.Callable[[
            Context2DRender_Extended,
            RenderItem,
            float
        ], typing.Any]] = {}
    
    def render(self):
        t = self.timer.now()
        cvr = self.canvas_render
        
        for item in self.items:
            item.update(t)
        
        for item in self.items:
            itype = item.itemType()
            
            match itype:
                case "builtin-rectangle":
                    item: render_items.Rectangle
                    
                    with cvr.savestate:
                        if item.is_fill:
                            cvr.setAttribute("fillStyle", item.fillColor)
                            endMethod = cvr.fill
                        else:
                            cvr.setAttribute("strokeStyle", item.strokeColor)
                            cvr.setAttribute("lineWidth", item.strokeLineWidth)
                            endMethod = cvr.stroke
                        
                        cvr.beginPath()
                        cvr.rect(item.x, item.y, item.width, item.height)
                        endMethod()
                            
                case _:
                    if itype in self.renderMethods:
                        self.renderMethods[itype](cvr, item, t)
                    else:
                        raise ValueError(f"Unknown render item type: {itype}")
