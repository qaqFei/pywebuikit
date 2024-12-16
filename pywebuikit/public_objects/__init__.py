from __future__ import annotations

import threading
import typing

from .._real_overload import overload, OverloadMeta

pythonPromise_ValueType = typing.TypeVar("pythonPromise_ValueType")
numtype = int|float

def _hsl2rgb(h: numtype, s: numtype, l: numtype):
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    
    if 0 <= h < 60: r, g, b = c, x, 0
    elif 60 <= h < 120: r, g, b = x, c, 0
    elif 120 <= h < 180: r, g, b = 0, c, x
    elif 180 <= h < 240: r, g, b = 0, x, c
    elif 240 <= h < 300: r, g, b = x, 0, c
    elif 300 <= h < 360: r, g, b = c, 0, x
    else: raise ValueError("Invalid HSL value")
    
    return (
        (r + m) * 255,
        (g + m) * 255,
        (b + m) * 255
    )

class pythonPromise(typing.Generic[pythonPromise_ValueType]):
    def __init__(self):
        self.e = threading.Event()
        
    def resolve(self, value: pythonPromise_ValueType):
        self.value = value
        self.e.set()
    
    def wait(self):
        self.e.wait()

class iteratingRemoveableCurrentList_Iterator:
    def __init__(self, list: iteratingRemoveableCurrentList):
        self.list = list
        self.index = 0
    
    def __next__(self):
        if self.index >= len(self.list):
            raise StopIteration
        
        value = self.list[self.index]
        self.index += 1
        return (self.remove, value)
    
    def remove(self):
        self.list.pop(self.index - 1)
        self.index -= 1

class iteratingRemoveableCurrentList(list):
    def __iter__(self):
        return iteratingRemoveableCurrentList_Iterator(self)
    
class Color(metaclass=OverloadMeta):
    checkvalue: bool = False
    jstoint: bool = False
    
    @overload
    def __init__(self, r: numtype, g: numtype, b: numtype, a: numtype = 1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    
    @overload
    def __init__(self, string: str):
        if (
            string.startswith("rgb")
            or string.startswith("rgba")
            or string.startswith("hsl")
            or string.startswith("hsla")
        ):
            self._loadFunc(string)
            return
        
        if string.startswith("#"): string = string[1:]
        elif string.startswith("0x"): string = string[2:]
        
        if len(string) == 3 or len(string) == 4: string = "".join(x * 2 for x in string)
        
        r = int(string[0:2], 16)
        g = int(string[2:4], 16)
        b = int(string[4:6], 16)
        a = 1.0 if len(string) < 8 else int(string[6:8], 16) / 255
        self.__init__(r, g, b, a)
    
    def _loadFunc(self, rgbFunc: str):
        rgbFunc = rgbFunc.replace(" ", "")
        
        if rgbFunc.startswith("rgb(") and rgbFunc.endswith(")"):
            rgbFunc = rgbFunc[4:-1]
            rgbFunc = rgbFunc.split(",")

            r = int(float(rgbFunc[0]))
            g = int(float(rgbFunc[1]))
            b = int(float(rgbFunc[2]))
            a = 1.0
            
        elif rgbFunc.startswith("rgba(") and rgbFunc.endswith(")"):
            rgbFunc = rgbFunc[5:-1]
            rgbFunc = rgbFunc.split(",")
            
            r = int(float(rgbFunc[0]))
            g = int(float(rgbFunc[1]))
            b = int(float(rgbFunc[2]))
            a = float(rgbFunc[3])
        
        elif rgbFunc.startswith("hsl(") and rgbFunc.endswith(")"):
            rgbFunc = rgbFunc[4:-1]
            rgbFunc = rgbFunc.split(",")

            h = float(rgbFunc[0])
            s = float(rgbFunc[1])
            l = float(rgbFunc[2])

            r, g, b, a = _hsl2rgb(h, s, l) + (1.0, )
        
        elif rgbFunc.startswith("hsla(") and rgbFunc.endswith(")"):
            rgbFunc = rgbFunc[5:-1]
            rgbFunc = rgbFunc.split(",")

            h = float(rgbFunc[0])
            s = float(rgbFunc[1])
            l = float(rgbFunc[2])
            a = float(rgbFunc[3])

            r, g, b = _hsl2rgb(h, s, l)
        
        else:
            raise ValueError("Invalid rgbFunc")
        
        self.__init__(r, g, b, a)

    def __pywebuikit_jseval__(self):
        return (
            f"'rgba({self.r}, {self.g}, {self.b}, {self.a})'"
            
            if not self.jstoint
            else
            
            f"'rgba({int(self.r)}, {int(self.g)}, {int(self.b)}, {self.a})'"
        )
    
    def __setattr__(self, n, v):
        if not self.checkvalue:
            return super().__setattr__(n, v)
            
        if n in ("r", "g", "b"):
            v = v if (0 <= v <= 255) else (255 if v > 255 else 0)
        elif n == "a":
            v = v if (0 <= v <= 1) else (1 if v > 1 else 0)
        
        return super().__setattr__(n, v)