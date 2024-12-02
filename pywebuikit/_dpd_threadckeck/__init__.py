import webview
import threading

_ct = webview.threading.current_thread

class Bypasser:
    def __enter__(self):
        self._tobj = None
        self._tn = None
        self._e = threading.Event()
        
        def bypass_ct():
            obj = _ct()
            self._tobj = obj
            self._tn = obj.name
            obj.name = "MainThread"
            self._e.set()
            return obj
        
        webview.threading.current_thread = bypass_ct
    
    def __exit__(self, *args):
        self._e.wait()
        webview.threading.current_thread = _ct
        self._tobj.name = self._tn
        