import math
from copy import copy, deepcopy
from enum import IntEnum
import numpy as np
from numpy.typing import NDArray
from typing import Any, Iterator, List, Self


class Bopimo_Color:
    # Color with 8 bit depth
    bopjson_type_name: str = "Color8"

    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue
        self.__clamp()

    ## PRIVATE METHODS

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

    ## CLASS METHODS

    @classmethod
    def from_hsv(
        cls, hue: int = 0, saturation: float = 1, value: float = 1
    ) -> "Bopimo_Color":
        r, g, b = cls.__from_hs(hue, saturation)
        c = Bopimo_Color(
            int(r * value * 255), int(g * value * 255), int(b * value * 255)
        )
        c.__clamp()
        return c

    ## INSTANCE METHODS

    def copy(self) -> "Bopimo_Color":
        return copy(self)

    def json(self) -> dict[str, Any]:
        return {"type": self.bopjson_type_name, "value": self.to_obj()}

    def to_obj(self) -> dict[str, int]:
        return {"r": self.red, "g": self.green, "b": self.blue}

    ## DUNDER METHODS

    def __iter__(self) -> Iterator[float]:
        return iter((self.red, self.green, self.blue))

    def __copy__(self) -> "Bopimo_Color":
        return Bopimo_Color(self.red, self.green, self.blue)

    def __str__(self) -> str:
        return f"{self.bopjson_type_name}({self.red}, {self.green}, {self.blue})"

    ### EQUALITY METHODS

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Color):
            raise TypeError()
        return (
            (self.red == other.red)
            and (self.green == other.green)
            and (self.blue == other.blue)
        )

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Color):
            raise TypeError()
        return not (self == other)


class Bopimo_Vector3:
    bopjson_type_name: str = "Vector3F32"

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    ## PRIVATE METHODS

    @classmethod
    def __matrix_from_euler(cls, roll: float, pitch: float, yaw: float) -> NDArray[Any]:
        cos_r: float = math.cos(roll)
        sin_r: float = math.sin(roll)
        cos_p: float = math.cos(pitch)
        sin_p: float = math.sin(pitch)
        cos_y: float = math.cos(yaw)
        sin_y: float = math.sin(yaw)

        MATRIX_R: tuple[List[float], List[float], List[float]] = (
            [1, 0, 0],
            [0, cos_r, -sin_r],
            [0, sin_r, cos_r],
        )
        MATRIX_P: tuple[List[float], List[float], List[float]] = (
            [cos_p, 0, sin_p],
            [0, 1, 0],
            [-sin_p, 0, cos_p],
        )
        MATRIX_Y: tuple[List[float], List[float], List[float]] = (
            [cos_y, -sin_y, 0],
            [sin_y, cos_y, 0],
            [0, 0, 1],
        )
        return np.dot(np.dot(MATRIX_P, MATRIX_R), MATRIX_Y)

    ## CLASS METHODS

    @classmethod
    def forward(cls, roll: float, pitch: float, yaw: float) -> Self:
        rotation_matrix = cls.__matrix_from_euler(roll, pitch, yaw)

        forward_vector: tuple[float, float, float] = np.dot(
            rotation_matrix, np.array([0, 0, 1])
        )

        return cls(*forward_vector)

    @classmethod
    def up(cls, roll: float, pitch: float, yaw: float) -> Self:
        rotation_matrix = cls.__matrix_from_euler(roll, pitch, yaw)

        up_vector: tuple[float, float, float] = np.dot(
            rotation_matrix, np.array([0, 1, 0])
        )

        return cls(*up_vector)

    @classmethod
    def left(cls, roll: float, pitch: float, yaw: float) -> Self:
        rotation_matrix = cls.__matrix_from_euler(roll, pitch, yaw)

        left_vector: tuple[float, float, float] = np.dot(
            rotation_matrix, np.array([1, 0, 0])
        )

        return cls(*left_vector)

    @classmethod
    def zero(cls) -> Self:
        return cls(0, 0, 0)

    @classmethod
    def one(cls) -> Self:
        return cls(1, 1, 1)

    ## INSTANCE METHODS

    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def copy(self) -> "Bopimo_Vector3":
        return copy(self)

    def to_degrees(self) -> "Bopimo_Vector3":
        return Bopimo_Vector3(
            math.degrees(self.x), math.degrees(self.y), math.degrees(self.z)
        )

    def to_radians(self) -> "Bopimo_Vector3":
        return Bopimo_Vector3(
            math.radians(self.x), math.radians(self.y), math.radians(self.z)
        )

    def to_obj(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}

    def json(self) -> dict[str, Any]:
        return {"type": self.bopjson_type_name, "value": self.to_obj()}

    ## DUNDER METHODS

    def __copy__(self) -> "Bopimo_Vector3":
        return Bopimo_Vector3(self.x, self.y, self.z)

    def __iter__(self) -> Iterator[float]:
        return iter((self.x, self.y, self.z))

    def __str__(self) -> str:
        return f"{self.bopjson_type_name}({self.x}, {self.y}, {self.z})"

    ### OPERATOR METHODS

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

    def __truediv__(self, other: int | float) -> "Bopimo_Vector3":
        return self.__div__(other)

    def __divmod__(self, other: int | float) -> "Bopimo_Vector3":
        if other == 0:
            raise ZeroDivisionError()
        return Bopimo_Vector3(self.x % other, self.y % other, self.z % other)

    def __neg__(self) -> "Bopimo_Vector3":
        return Bopimo_Vector3(-self.x, -self.y, -self.z)

    ### EQUALITY METHODS

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Vector3):
            raise TypeError()
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Vector3):
            raise TypeError()
        return not (self == other)


class Bopimo_Vector3Array:
    bopjson_type_name: str = Bopimo_Vector3.bopjson_type_name + "_Array"

    def __init__(self, vector3_list: List[Bopimo_Vector3] = []):
        self._list = vector3_list

    ## INSTANCE METHODS

    def add_vector(self, vector: Bopimo_Vector3):
        self._list.append(vector)

    def clear(self):
        self._list.clear()

    # To make this more intuitive, this method will deep copy by default.
    def copy(self, deep: bool = True) -> "Bopimo_Vector3Array":
        if deep:
            return deepcopy(self)
        return copy(self)

    def get_vector(self, index: int) -> Bopimo_Vector3:
        return self._list[index]

    def set_vector(self, index: int, vector: Bopimo_Vector3):
        self._list[index] = vector

    def is_empty(self) -> bool:
        return len(self) == 0

    def remove_vector(self, index: int) -> Bopimo_Vector3:
        return self._list.pop(index)

    def json(self) -> dict[str, Any]:
        obj: dict[str, Any] = {"type": self.bopjson_type_name, "value": []}
        for vector3 in self._list:
            obj["value"].append(vector3.to_obj())
        return obj

    ## DUNDER METHODS

    def __copy__(self) -> "Bopimo_Vector3Array":
        return Bopimo_Vector3Array(copy(self._list))

    def __deepcopy__(self, memo: dict[Any, Any]) -> "Bopimo_Vector3Array":
        return Bopimo_Vector3Array(deepcopy(self._list, memo))

    def __str__(self) -> str:
        s = "Vector3Array("
        for vec in self._list:
            s = s + str(vec)
            if self._list[-1] != vec:
                s = s + ", "
        return s + ")"

    ### ITERABLE METHODS

    def __iter__(self) -> Iterator[Bopimo_Vector3]:
        return iter(self._list)

    def __next__(self):
        return next(self.__iter__())

    def __len__(self) -> int:
        return len(self._list)

    ### EQUALITY METHODS

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Vector3Array):
            raise TypeError()
        if len(self) != len(other):
            return False
        if self.is_empty():
            return True

        # Order matters for equality.
        for vec1, vec2 in zip(self._list, other._list):
            if vec1 != vec2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_Vector3Array):
            raise TypeError()
        return not (self == other)


class Bopimo_ColorArray:
    bopjson_type_name: str = Bopimo_Color.bopjson_type_name + "_Array"

    def __init__(self, color_list: List[Bopimo_Color] = []):
        self._list = color_list

    ## INSTANCE METHODS

    def add_color(self, vector: Bopimo_Color):
        self._list.append(vector)

    def clear(self):
        self._list.clear()

    def copy(self, deep: bool = True) -> "Bopimo_ColorArray":
        if deep:
            return deepcopy(self)
        return copy(self)

    def get_color(self, index: int) -> Bopimo_Color:
        return self._list[index]

    def set_color(self, index: int, color: Bopimo_Color):
        self._list[index] = color

    def is_empty(self) -> bool:
        return len(self._list) == 0

    def remove_color(self, index: int) -> Bopimo_Color:
        return self._list.pop(index)

    def json(self) -> dict[str, Any]:
        obj: dict[str, Any] = {"type": self.bopjson_type_name, "value": []}
        for color in self._list:
            obj["value"].append(color.to_obj())
        return obj

    ## DUNDER METHODS

    def __copy__(self) -> "Bopimo_ColorArray":
        return Bopimo_ColorArray(copy(self._list))

    def __deepcopy__(self, memo: dict[Any, Any]) -> "Bopimo_ColorArray":
        return Bopimo_ColorArray(deepcopy(self._list, memo))

    def __str__(self) -> str:
        s = "ColorArray("
        for col in self._list:
            s = s + str(col)
            if self._list[-1] != col:
                s = s + ", "
        return s + ")"

    ### ITERABLE METHODS

    def __iter__(self) -> Iterator[Bopimo_Color]:
        return iter(self._list)

    def __next__(self):
        return next(self.__iter__())

    def __len__(self) -> int:
        return len(self._list)

    ### EQUALITY METHODS

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_ColorArray):
            raise TypeError()
        if len(self) != len(other):
            return False
        if self.is_empty():
            return True

        # Order matters for equality.
        for col1, col2 in zip(self._list, other._list):
            if col1 != col2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Bopimo_ColorArray):
            raise TypeError()
        return not (self == other)


# This will come up often because though integers are technically acceptable, enums are more future-proof.
type Bopimo_Integer = int | IntEnum


# NOT A REAL TYPE. THIS IS A SUPERCLASS TO DEDUPLICATE CODE
# The great thing about Python: Integers can be both 32 AND 64 bit.
class Bopimo_IntArray:
    bopjson_type_name: str = "Int_Array"

    def __init__(self, int_list: List[Bopimo_Integer] = []):
        self._list = int_list

    ## INSTANCE METHODS

    def add_int(self, integer: Bopimo_Integer):
        self._list.append(integer)

    def clear(self):
        self._list.clear()

    def copy(self, deep: bool = True) -> Self:
        if deep:
            return deepcopy(self)
        return copy(self)

    def get_int(self, index: int) -> Bopimo_Integer:
        return self._list[index]

    def set_int(self, index: int, integer: Bopimo_Integer):
        self._list[index] = integer

    def is_empty(self) -> bool:
        return len(self._list) == 0

    def remove_int(self, index: int) -> Bopimo_Integer:
        return self._list.pop(index)

    def json(self) -> dict[str, Any]:
        values: List[int] = []
        for value in self._list:
            values.append(value)
        return {"type": self.bopjson_type_name, "value": values}

    ## DUNDER METHODS

    def __copy__(self) -> Self:
        return self.__class__(copy(self._list))

    def __deepcopy__(self, memo: dict[Any, Any]) -> Self:
        return self.__class__(deepcopy(self._list, memo))

    def __str__(self) -> str:
        s = f"{self.bopjson_type_name}("
        for num in self._list:
            s = s + str(num)
            if self._list[-1] != num:
                s = s + ", "
        return s + ")"

    ### ITERABLE METHODS

    def __iter__(self) -> Iterator[int]:
        return iter(self._list)

    def __next__(self):
        return next(self.__iter__())

    def __len__(self) -> int:
        return len(self._list)

    ### EQUALITY METHODS

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError()
        if len(self) != len(other):
            return False
        if self.is_empty():
            return True

        # Order matters for equality.
        for num1, num2 in zip(self._list, other._list):
            if num1 != num2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError()
        return not (self == other)


class Bopimo_Int32Array(Bopimo_IntArray):
    bopjson_type_name: str = "Int32_Array"

    def __init__(self, int_list: List[Bopimo_Integer] = []):
        self._list = int_list
        self.signed = False

    def json(self) -> dict[str, Any]:
        values: List[int] = []
        lower_bound = 0 if not self.signed else -(2**31)
        upper_bound = 2**32 if not self.signed else (2**31) - 1
        for value in self._list:
            if value < lower_bound or value > upper_bound:
                raise OverflowError(
                    f"You have ran into an overflow/underflow in a 32-bit array with {value}."
                )
            values.append(value)
        return {"type": self.bopjson_type_name, "value": values}


class Bopimo_Int64Array(Bopimo_IntArray):
    bopjson_type_name: str = "Int64_Array"

    def __init__(self, int_list: List[Bopimo_Integer] = []):
        self._list = int_list
        self.signed = False

    def json(self) -> dict[str, Any]:
        values: List[int] = []
        lower_bound = 0 if not self.signed else -(2**63)
        upper_bound = 2**64 if not self.signed else (2**63) - 1
        for value in self._list:
            if value < lower_bound or value > upper_bound:
                raise OverflowError(
                    f"You have ran into an overflow/underflow in a 64-bit array with {value}."
                )
            values.append(value)
        return {"type": self.bopjson_type_name, "value": values}
