import json

OUT = """
\"\"\"
Class object for {classname}
Documentation: {documentation}
API Path: {path}
\"\"\"
from aiogithubapi.objects.base import AIOGitHubAPIBase

{inherit}

"""

CLASS = """
class {classname}(AIOGitHubAPIBase):
{properties}
"""

PROP = """
    @property
    def {key}(self):
        return self.attributes.get("{key}", {default})
"""
PROPCLASS = """
    @property
    def {key}(self):
        return {name}(self.attributes.get("{key}", {default}))
"""

INHERIT = []


def get_input():
    with open("generate/input.json", "r") as inputdata:
        return json.loads(inputdata.read())


def generateclass(name, data, primary=False):
    properties = []
    for key in data:
        if key.startswith("_"):
            continue
        if isinstance(data[key], list):
            continue
        if isinstance(data[key], dict):
            _name = key.split("_")
            _name = "".join([x.title() for x in _name])
            _name = f"_{_name}"
            INHERIT.append(generateclass(_name, data[key]))
            properties.append(PROPCLASS.format(name=_name, key=key, default={}))
            continue
        if isinstance(data[key], bool):
            properties.append(PROP.format(key=key, default=data[key]))
            continue
        if isinstance(data[key], str):
            properties.append(PROP.format(key=key, default='""'))
            continue
        properties.append(PROP.format(key=key, default=None))

    if not primary:
        return CLASS.format(classname=name, properties="".join(properties))
    docs = input("Documentation URL: ")
    path = input("API path: ")
    name = input("Main Classname: ")
    INHERIT.append(CLASS.format(classname=name, properties="".join(properties)))
    return OUT.format(
        classname=f"AIOGitHubAPI{name}",
        properties=properties,
        documentation=docs,
        path=path,
        inherit="".join(INHERIT),
    )


def add_object():
    data = get_input()
    with open("test.py", "w") as test:
        test.write(generateclass("", data, True))


add_object()
