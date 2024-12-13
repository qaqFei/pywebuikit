import threading

from pywebuikit import webwindow, render

def main():
    import random
    
    rd = render.Context2DRender(cv)
    rd.create_mainCanvas()
    
    w, h = 800, 600
    r, g, b = (random.randint(0, 255) for _ in range(3))
    t, l = 0, 0
    sx, sy = w / 500, h / 650
    six, siy = w / 4, h / 4
    sr, sg, sb = 1, 2, 3
    
    while not cv._destroy_event.isSet():
        cv.setWaitingState(True)
        
        rd.clearRect(0, 0, w, h)
        r += sr
        g += sg
        b += sb
        
        if not (0 < r < 255):
            sr *= -1
        elif not (0 < g < 255):
            sg *= -1
        elif not (0 < b < 255):
            sb *= -1
        
        l += sx
        t += sy

        if not (0 < l < w and 0 < l + six < w):
            l -= sx
            sx *= -1
        elif not (0 < t < h and 0 < t + siy < h):
            t -= sy
            sy *= -1
        
        rd.setAttribute("fillStyle", f"rgb({r}, {g}, {b})")
        rd.fillRect(l, t, six, siy)
        
        cv.setWaitingState(False)

cv = webwindow.WebWindow(800, 600, 100, 100, debug=True)
threading.Thread(target=main, daemon=True).start()
cv.waitClose()