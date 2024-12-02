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

class Canvas:
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
        
        winlength = len(webview.windows)
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
        
        while winlength != len(webview.windows):
            time.sleep(1 / 60)
        
        webview.windows.remove(self.web)