import os
import os.path
import threading
import typing
import random
import time
import http.server
import importlib.resources as resources
from ctypes import windll

import webview

from .. import _dpd_threadckeck
from .. import jsapi
from .. import fserver

HTML_PATH = os.environ.get("PYWEBUIKIT_HTML_PATH", "./user_pywebuikit.html")

if not (os.path.exists(HTML_PATH) and os.path.isfile(HTML_PATH)):
    htmlcontent = resources.read_text(__package__, "builtin_pywebuikit.html")
    with open(HTML_PATH, "w") as f:
        f.write(htmlcontent)

class StringProcesser:
    def __new__(cls):
        raise NotImplementedError("This class is not instantiable")
    
    @staticmethod
    def replaceEscape(s: str) -> str:
        return (
            s
            .replace("\\", "\\\\")
            .replace("'", "\\'")
            .replace("\"", "\\\"")
            .replace("`", "\\`")
            .replace("\n", "\\n")
        )
    
    @staticmethod
    def replaceString2CodeEval(s: str) -> str:
        return f"\"{StringProcesser.replaceEscape(s)}\""

class WebWindow:
    def __init__(
        self,
        width: int, height: int,
        x: int, y: int,
        debug: bool = False,
        title: str = "PyWebUIKit",
        resizable: bool = True,
        fullscreen: bool = False,
        frameless: bool = False,
        min_size: tuple[int, int] = (0, 0),
        minimized: bool = False,
        maximized: bool = False,
        htmlpath: str = HTML_PATH,
        webkwargs: typing.Optional[dict[str, typing.Any]] = None
    ):
        self.jsapi = jsapi.JsApi()
        self._destroy_event = threading.Event()
        self._jscodes: list[str] = []
        self._waitting_jscodes: bool = False
        
        self.web: webview.Window = webview.create_window(
            title = title,
            url = os.path.abspath(htmlpath),
            resizable = resizable,
            js_api = self.jsapi,
            frameless = frameless,
            width = width, height = height,
            x = x, y = y,
            fullscreen = fullscreen,
            min_size = min_size,
            minimized = minimized, maximized = maximized,
            **(webkwargs or {})
        )
        
        with _dpd_threadckeck.Bypasser():
            threading.Thread(target=webview.start, kwargs={"debug": debug}, daemon=True).start()
        
        self.web.events.closed += self._destroy_event.set
        
        title = self.web.title
        temp_title = title + " " * random.randint(0, 4096)
        self.web.set_title(temp_title)
        
        self.hwnd = 0
        while not self.hwnd:
            self.hwnd = windll.user32.FindWindowW(None, temp_title)
            time.sleep(1 / 60)
        self.web.set_title(title)
        
        self.fserver_res: dict[str, bytes] = {}
        self.fserver_port = int(self.web._server.address.split(":")[2].split("/")[0]) + 1
        self.fserver_hander = fserver.make_fsh(self)
        self.fserver = http.server.HTTPServer(("localhost", self.fserver_port), self.fserver_hander)
        threading.Thread(target=self.fserver.serve_forever, daemon=True).start()
        
        self.web.evaluate_js("null;")
        webview.windows.remove(self.web)
        
        if not fullscreen:
            webdpr = self.evaluate_js("window.devicePixelRatio;")
            w_legacy, h_legacy = self.getLegacyWindowWidth(), self.getLegacyWindowHeight()
            dw_legacy, dh_legacy = width - w_legacy, height - h_legacy
            dw_legacy *= webdpr; dh_legacy *= webdpr
            dw_legacy, dh_legacy = int(dw_legacy), int(dh_legacy)
            self.resize(width + dw_legacy, height + dh_legacy)
            self.move(int(x - dw_legacy / 2), int(y - dh_legacy / 2))
    
    def getWidth(self) -> int:
        return self.web.width
    
    def getHeight(self) -> int:
        return self.web.height
    
    def getHwnd(self) -> int:
        return self.hwnd
    
    def getTitle(self) -> str:
        return self.web.title
    
    def getLegacyWindowWidth(self) -> int:
        return self.web.evaluate_js("window.innerWidth;")
    
    def getLegacyWindowHeight(self) -> int:
        return self.web.evaluate_js("window.innerHeight;")
    
    def desotroy(self) -> None:
        self.web.destroy()
    
    def resize(self, w: int, h: int):
        self.web.resize(w, h)
    
    def move(self, x: int, y: int):
        self.web.move(x, y)
    
    def waitClose(self) -> None:
        self._destroy_event.wait()
        self.fserver.shutdown()
        
    def setWaitingState(self, state: bool) -> None:
        self._waitting_jscodes = state
        
        if not state:
            self.web.evaluate_js(f"{self._jscodes}.forEach(r2eval);")
            self._jscodes.clear()
    
    def evaluate_js(self, js: str) -> typing.Any:
        if self._waitting_jscodes:
            self._jscodes.append(js)
            return
        return self.web.evaluate_js(f"r2eval({StringProcesser.replaceString2CodeEval(js)});")
    