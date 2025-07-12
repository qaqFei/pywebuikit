import threading

from pywebuikit import *

def main():
    import random
    
    rd = render.Context2DRender_Extended(wind)
    rd.create_mainCanvas()
    rdm = render.Canvas2DRenderManager(rd)
    
    wfilter_blur = jsbridge.WebFilterFunc_Blur(0.0)
    wfilter_gray = jsbridge.WebFilterFunc_Grayscale(0.0)
    
    filterSet = jsbridge.WebFilterSet(
        wfilter_blur,
        wfilter_gray
    )
    
    cvref = rd.create_canvasRef()
    
    w, h = 800, 600
    r, g, b = (random.randint(0, 255) for _ in range(3))
    sx, sy = w / 500, h / 650
    six, siy = w / 4, h / 4
    sp = 5
    sr, sg, sb = 1 / sp, 2 / sp, 3 / sp
    
    rect = render.render_items.Rectangle(0, 0, six, siy)
    rdm.items.append(rect)
    
    while not wind._destroy_event.is_set():
        wind.setWaitingState(True)
        rd.clearRect(0, 0, w, h)
        
        r += sr
        g += sg
        b += sb
        
        if not (0 < r < 255):
            r = 255 if r > 255 else 0
            sr *= -1
        elif not (0 < g < 255):
            g = 255 if g > 255 else 0
            sg *= -1
        elif not (0 < b < 255):
            b = 255 if b > 255 else 0
            sb *= -1
        
        rect.fillColor = public_objects.Color(f"rgba({r}, {g}, {b}, {(r + g + b) / 765})")
        rect.x += sx
        rect.y += sy
        
        if not (0 < rect.x < w and 0 < rect.x + six < w):
            rect.x = w - six if rect.x > 0 else 0
            sx *= -1
        elif not (0 < rect.y < h and 0 < rect.y + siy < h):
            rect.y = h - siy if rect.y > 0 else 0
            sy *= -1
            sy = -25
        
        sy += 1
        
        wfilter_blur.setvalue((rect.x + rect.y) / 75)
        wfilter_gray.setvalue((r + g + b) / 765 * 1.25)
        
        jsbridge.setFilter(wind, filterSet, cvref)
        rdm.render()
        
        wind.setWaitingState(False)

wind = webwindow.WebWindow(800, 600, 100, 100, debug=True)
threading.Thread(target=main, daemon=True).start()
wind.waitClose()