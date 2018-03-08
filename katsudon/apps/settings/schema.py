from yaml import load
from types import ModuleType


class ModToDict:
    def __init__(self, module):
        self.module = module

    def __call__(self):
        result = {}
        for k, v in self.module.__dict__.items():
            if k.startswith("_"):
                continue
            if isinstance(v, ModuleType):
                result[k] = v._as_dict()
            else:
                result[k] = v
        return result

class Schema:
    def __init__(self, name="", parent=None, data=None, yaml=None):
        self.children = None
        self.type_name = None
        self.help = None
        self.default = None
        self.priority = 2
        self.args = None
        self.name = name
        self.parent = parent
        if data is not None:
            self.load_data(data)
        if yaml is not None:
            self.load_yaml(yaml)

    @property
    def full_name(self):
        if self.parent is not None:
            return ".".join([self.parent.full_name, self.name])
        return self.name

    def load_yaml(self, stream):
        return self.load_data(load(stream))

    def guess_type(self, data):
        if isinstance(data, str):
            self.type_name = "str"
        elif isinstance(data, int):
            self.type_name = "int"
        elif isinstance(data, float):
            self.type_name = "float"
        elif isinstance(data, dict):
            self.type_name = "dict"
        # TODO: raise here

    def load_data(self, data):
        if isinstance(data, dict):
            if "default" in data:
                try:
                    self.type_name = data["type"]
                except KeyError:
                    self.guess_type(data["default"])
                self.priority = data.get("priority")
                self.help = data.get("help")
                if isinstance(data["default"], dict):
                    self.children = {k:Schema(data=v, name=k, parent=self) for k, v in data["default"].items()}
                else:
                    self.default = data["default"]
            else:
                self.children = {k:Schema(data=v, name=k, parent=self) for k, v in data.items()}
        else:
            self.guess_type(data)
            self.default = data

    def merge(self, other):
        pass

    def defaults(self):
        if self.children is not None:
            settings = ModuleType(self.full_name)
            settings._as_dict = ModToDict(settings)
            for name, val in self.children.items():
                if isinstance(val, Schema):
                    val = val.defaults()
                setattr(settings, name, val)
            return settings
        else:
            return self.default
