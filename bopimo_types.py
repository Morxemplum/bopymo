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
        self.__clamp()

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

    # Sanity check to stop out of range values
    def __clamp(self):
        self.red = max(0, min(self.red, 255))
        self.green = max(0, min(self.green, 255))
        self.blue = max(0, min(self.blue, 255))
        self.alpha = max(0, min(self.alpha, 255))

    @classmethod
    def from_hsv(
        cls, hue: int = 0, saturation: float = 1, value: float = 1, alpha: int = 255
    ) -> "Bopimo_Color":
        r, g, b = cls.__from_hs(hue, saturation)
        c = Bopimo_Color(
            int(r * value * 255), int(g * value * 255), int(b * value * 255), alpha
        )
        c.__clamp()
        return c

    def to_obj(self) -> dict[str, int]:
        return {"r": self.red, "g": self.green, "b": self.blue, "a": self.alpha}

    def json(self) -> dict[str, Any]:
        return {"type": self.bopjson_type_name, "value": self.to_obj()}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Color):
            raise TypeError()
        return (
            (self.red == other.red)
            and (self.green == other.green)
            and (self.blue == other.blue)
            and (self.alpha == other.alpha)
        )

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Color):
            raise TypeError()
        return not (self == other)

    def __str__(self) -> str:
        return f"{self.bopjson_type_name}({self.red}, {self.green}, {self.blue}, {self.alpha})"


class Bopimo_Vector3:
    bopjson_type_name: str = "Vector3F32"

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def to_obj(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}

    def json(self) -> dict[str, Any]:
        return {"type": self.bopjson_type_name, "value": self.to_obj()}

    def __add__(self, other: "Bopimo_Vector3") -> "Bopimo_Vector3":
        return Bopimo_Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Bopimo_Vector3") -> "Bopimo_Vector3":
        return Bopimo_Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: int | float) -> "Bopimo_Vector3":
        return Bopimo_Vector3(self.x * other, self.y * other, self.z * other)

    def __div__(self, other: int | float) -> "Bopimo_Vector3":
        if other == 0:
            raise ZeroDivisionError()
        return Bopimo_Vector3(self.x / other, self.y / other, self.z / other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Vector3):
            raise TypeError()
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Vector3):
            raise TypeError()
        return not (self == other)

    def __str__(self) -> str:
        return f"{self.bopjson_type_name}({self.x}, {self.y}, {self.z})"


class Bopimo_Vector3Array:
    bopjson_type_name: str = Bopimo_Vector3.bopjson_type_name + "_Array"

    def __init__(self, vector3_list: List[Bopimo_Vector3] = []):
        self.__list = vector3_list

    def add_vector(self, vector: Bopimo_Vector3):
        self.__list.append(vector)

    def clear(self):
        self.__list.clear()

    def get_vector(self, index: int) -> Bopimo_Vector3:
        return self.__list[index]

    def is_empty(self) -> bool:
        return len(self) == 0

    def remove_vector(self, index: int) -> Bopimo_Vector3:
        return self.__list.pop(index)

    def json(self) -> dict[str, Any]:
        obj: dict[str, Any] = {"type": self.bopjson_type_name, "value": []}
        for vector3 in self.__list:
            obj["value"].append(vector3.to_obj())
        return obj

    def __len__(self) -> int:
        return len(self.__list)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Vector3Array):
            raise TypeError()
        if len(self) != len(other):
            return False
        if self.is_empty():
            return True

        # Order matters for equality.
        for vec1, vec2 in zip(self.__list, other.__list):
            if vec1 != vec2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Vector3Array):
            raise TypeError()
        return not (self == other)

    def __str__(self) -> str:
        s = "Vector3Array("
        for vec in self.__list:
            s = s + str(vec)
            if self.__list[-1] != vec:
                s = s + ", "
        return s + ")"


class Bopimo_ColorArray:
    bopjson_type_name: str = Bopimo_Color.bopjson_type_name + "_Array"

    def __init__(self, color_list: List[Bopimo_Color] = []):
        self.__list = color_list

    def add_color(self, vector: Bopimo_Color):
        self.__list.append(vector)

    def clear(self):
        self.__list.clear()

    def get_color(self, index: int) -> Bopimo_Color:
        return self.__list[index]

    def is_empty(self) -> bool:
        return len(self.__list) == 0

    def remove_color(self, index: int) -> Bopimo_Color:
        return self.__list.pop(index)

    def json(self) -> dict[str, Any]:
        obj: dict[str, Any] = {"type": self.bopjson_type_name, "value": []}
        for color in self.__list:
            obj["value"].append(color.to_obj())
        return obj

    def __len__(self) -> int:
        return len(self.__list)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_ColorArray):
            raise TypeError()
        if len(self) != len(other):
            return False
        if self.is_empty():
            return True

        # Order matters for equality.
        for col1, col2 in zip(self.__list, other.__list):
            if col1 != col2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_ColorArray):
            raise TypeError()
        return not (self == other)

    def __str__(self) -> str:
        s = "ColorArray("
        for col in self.__list:
            s = s + str(col)
            if self.__list[-1] != col:
                s = s + ", "
        return s + ")"


# This will come up often because though integers are technically acceptable, enums are more future-proof.
type Bopimo_Integer = int | IntEnum


class Bopimo_Int32Array:
    bopjson_type_name: str = "Int32_Array"

    def __init__(self, int_list: List[Bopimo_Integer] = []):
        self.__list = int_list

    def add_int(self, vector: Bopimo_Integer):
        self.__list.append(vector)

    def clear(self):
        self.__list.clear()

    def get_int(self, index: int) -> Bopimo_Integer:
        return self.__list[index]

    def is_empty(self) -> bool:
        return len(self.__list) == 0

    def remove_int(self, index: int) -> Bopimo_Integer:
        return self.__list.pop(index)

    def json(self) -> dict[str, Any]:
        values: List[int] = []
        for value in self.__list:
            values.append(value)
        return {"type": self.bopjson_type_name, "value": values}

    def __len__(self) -> int:
        return len(self.__list)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Int32Array):
            raise TypeError()
        if len(self) != len(other):
            return False
        if self.is_empty():
            return True

        # Order matters for equality.
        for num1, num2 in zip(self.__list, other.__list):
            if num1 != num2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Int32Array):
            raise TypeError()
        return not (self == other)

    def __str__(self) -> str:
        s = "Int32Array("
        for num in self.__list:
            s = s + str(num)
            if self.__list[-1] != num:
                s = s + ", "
        return s + ")"
