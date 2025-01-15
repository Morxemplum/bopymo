import math
from enum import Enum


def attribute(attr):
    return {"__gdtype": "StringName", "name": attr}


def godot_kv_pair(key, value):
    return {"key": key, "value": value}


class Godot_Color:
    # Values are 0 - 1
    def __init__(self, red, green, blue, alpha=1.0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __from_hs(self, h, s):
        # Find a color from hue and saturation.
        h = (h % 360) / 60
        f, i = math.modf(h)
        g = 1 - f  # For descending gradients
        t = 1 - s  # Minimum color intensity based on saturation
        f, g = s * f + t, s * g + t  # Apply saturation

        if i == 0:
            return (1, f, t)
        elif i == 1:
            return (g, 1, t)
        elif i == 2:
            return (t, 1, f)
        elif i == 3:
            return (t, g, 1)
        elif i == 4:
            return (f, t, 1)
        elif i == 5:
            return (1, t, g)
        return (1, 1, 1)  # Fallback

    @classmethod
    def from_hsv(cls, hue=0, saturation=1, value=1, alpha=1):
        r, g, b = cls.__from_hs(hue, saturation)
        return Godot_Color(r * value, g * value, b * value, alpha)

    def to_json_object(self):
        return {
            "__gdtype": "Color",
            "values": [self.red, self.green, self.blue, self.alpha],
        }


class Godot_Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Godot_Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Godot_Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iadd__(self, other):
        return self.__add__(other)

    def __isub__(self, other):
        return self.__sub__(other)

    def to_json_object(self):
        return {"__gdtype": "Vector3", "values": [self.x, self.y, self.z]}


class Godot_PackedVector3Array:
    # List is made of Godot_Vector3 instances
    def __init__(self, vector3_list=[]):
        self.list = vector3_list

    def is_empty(self):
        return len(self.list) == 0

    def to_json_object(self):
        # PackedArrays are weird where they just straight up list the numbers
        obj = {"__gdtype": "PackedVector3Array", "values": []}
        for vector3 in self.list:
            obj["values"].append(vector3.x)
            obj["values"].append(vector3.y)
            obj["values"].append(vector3.z)
        return obj


class Godot_PackedColorArray:
    # List is made of Godot_Color instances
    def __init__(self, color_list=[]):
        self.list = color_list

    def is_empty(self):
        return len(self.list) == 0

    def to_json_object(self):
        obj = {"__gdtype": "PackedColorArray", "values": []}
        for color in self.list:
            obj["values"].append(color.red)
            obj["values"].append(color.green)
            obj["values"].append(color.blue)
            obj["values"].append(color.alpha)
        return obj


class Godot_PackedInt32Array:
    # List is just integers
    def __init__(self, int_list=[]):
        self.list = int_list

    def is_empty(self):
        return len(self.list) == 0

    def to_json_object(self):
        values = []
        for value in self.list:
            if isinstance(value, Enum):
                values.append(value.value)
            else:
                values.append(value)
        return {"__gdtype": "PackedInt32Array", "values": values}
