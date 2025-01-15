import math
from enum import IntEnum
from typing import Any, List


class Bopimo_Color:
    # Color with 8 bit depth with alpha channel
    bopjson_type_name: str = "Color8A"

    def __init__(self, red: int, green: int, blue: int, alpha: int = 255):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    @classmethod
    def __from_hs(cls, h: int, s: float) -> tuple[float, float, float]:
        # Find a color from hue and saturation.
        hue: float = (h % 360) / 60
        f: float
        i: float
        f, i = math.modf(hue)
        g: float = 1 - f  # For descending gradients
        t: float = 1 - s  # Minimum color intensity based on saturation
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
    def from_hsv(
        cls, hue: int = 0, saturation: float = 1, value: float = 1, alpha: int = 255
    ) -> "Bopimo_Color":
        r, g, b = cls.__from_hs(hue, saturation)
        return Bopimo_Color(
            int(r * value * 255), int(g * value * 255), int(b * value * 255), alpha
        )

    def to_obj(self) -> dict[str, int]:
        return {"r": self.red, "g": self.green, "b": self.blue, "a": self.alpha}

    def json(self) -> dict[str, Any]:
        return {"type": self.bopjson_type_name, "value": self.to_obj()}


class Bopimo_Vector3:
    bopjson_type_name: str = "Vector3F32"

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: "Bopimo_Vector3") -> "Bopimo_Vector3":
        return Bopimo_Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Bopimo_Vector3") -> "Bopimo_Vector3":
        return Bopimo_Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iadd__(self, other: "Bopimo_Vector3") -> "Bopimo_Vector3":
        return self.__add__(other)

    def __isub__(self, other: "Bopimo_Vector3") -> "Bopimo_Vector3":
        return self.__sub__(other)

    def to_obj(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}

    def json(self) -> dict[str, Any]:
        return {"type": self.bopjson_type_name, "value": self.to_obj()}


class Bopimo_Vector3Array:
    bopjson_type_name: str = Bopimo_Vector3.bopjson_type_name + "_Array"

    def __init__(self, vector3_list: List[Bopimo_Vector3] = []):
        self.list = vector3_list

    def is_empty(self) -> bool:
        return len(self.list) == 0

    def json(self) -> dict[str, Any]:
        obj: dict[str, Any] = {"type": self.bopjson_type_name, "value": []}
        for vector3 in self.list:
            obj["value"].append(vector3.to_obj())
        return obj


class Bopimo_ColorArray:
    bopjson_type_name: str = Bopimo_Color.bopjson_type_name + "_Array"

    def __init__(self, color_list: List[Bopimo_Color] = []):
        self.list = color_list

    def is_empty(self) -> bool:
        return len(self.list) == 0

    def json(self) -> dict[str, Any]:
        obj: dict[str, Any] = {"type": self.bopjson_type_name, "value": []}
        for color in self.list:
            obj["value"].append(color.to_obj())
        return obj


class Bopimo_Int32Array:
    bopjson_type_name: str = "Int32_Array"

    def __init__(self, int_list: List[int | IntEnum] = []):
        self.list = int_list

    def is_empty(self) -> bool:
        return len(self.list) == 0

    def json(self) -> dict[str, Any]:
        values: List[int] = []
        for value in self.list:
            values.append(value)
        return {"type": self.bopjson_type_name, "value": values}
