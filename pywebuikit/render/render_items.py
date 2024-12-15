from .. import public_objects
from .._real_overload import overload, OverloadMeta

numtype = public_objects.numtype

class Rectangle(metaclass=OverloadMeta):
    update = lambda self, t: None
    fillColor = public_objects.Color(0, 0, 0, 0)
    strokeColor = public_objects.Color(0, 0, 0, 0)
    is_fill = True
    strokeLineWidth = 0.0
    
    @overload
    def __init__(self, x: numtype, y: numtype, width: numtype, height: numtype):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    @overload
    def __init__(self, x1: numtype, y1: numtype, x2: numtype, y2: numtype):
        self.x = min(x1, x2)
        self.y = min(y1, y2)
        self.width = abs(x2 - x1)
        self.height = abs(y2 - y1)
    
    def itemType(self):
        return "builtin-rectangle"
    