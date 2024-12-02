import typing

class JsApi:
    def __init__(self) -> None:
        self.things: dict[str, typing.Any] = {}
    
    def get_thing(self, name: str):
        return self.things[name]
    
    def set_thing(self, name: str, value: typing.Any):
        self.things[name] = value
    
    def get_attr(self,name: str):
        return getattr(self, name)
    
    def set_attr(self, name: str, value: typing.Any):
        setattr(self, name, value)
    
    def call_attr(self,name: str, *args, **kwargs):
        return getattr(self, name)(*args, **kwargs)
    