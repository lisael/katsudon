from yaml import load
from types import ModuleType
from .exceptions import ConfigurationError


class SettingsToDict:
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


class UpdateSettings:
    def __init__(self, module, schema):
        self.module = module
        self.schema = schema

    def __call__(self, data):
        # import ipdb; ipdb.set_trace()
        for k, v in data.items():
            if k in self.module.__dict__:
                if isinstance(v, dict):
                    self.module.__dict__[k]._update(v)
                else:
                    self.schema.children[k].validate(v)
                    self.module.__dict__[k] = v


def SettingsModule(schema):
    mod = ModuleType(schema.full_name)
    mod._as_dict = SettingsToDict(mod)
    mod._update = UpdateSettings(mod, schema)
    return mod


class Schema:
    type_from_name = dict(str=str, int=int, float=float, dict=dict)
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

    def validate(self, data):
        if self.type_name.startswith("list"):
            list_type = self.type_name[4:].strip(" ()")
            self._validate_list(data, list_type)
        else:
            self._validate_scalar(data, self.type_name)

    def _validate_list(self, data, list_type):
        if not isinstance(data, list):
            raise ConfigurationError("%s should be a list" % self.full_name)
        for elem in data:
            self._validate_scalar(elem, list_type)

    def _validate_scalar(self, data, type_name):
        type_names = [t.strip() for t in type_name.split("|")]
        types = tuple([self.type_from_name[t] for t in type_names])
        if not isinstance(data, types):
            raise ConfigurationError("%s should be %s" % (self.full_name, "or".join(type_names)))

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
            settings = SettingsModule(self)
            for name, val in self.children.items():
                if isinstance(val, Schema):
                    val = val.defaults()
                setattr(settings, name, val)
            return settings
        else:
            return self.default
