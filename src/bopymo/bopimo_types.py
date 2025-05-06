import math
from copy import copy, deepcopy
from enum import IntEnum
import numpy as np
from numpy.typing import NDArray
from typing import Any, Iterator, List, Self

## TYPES


class Color:
    """
    A bopimo type that is meant to represent 8-bit RGB color. Responsible for
    giving objects and textures their visual color.

    Class Attributes:
        bopjson_type_name (str):
            The name of the type as detailed in the bopjson format

    Instance Attributes:
        red (int):
            The brightness of the red channel
        green (int):
            The brightness of the green channel
        blue (int):
            The brightness of the blue channel
    """

    bopjson_type_name: str = "Color8"

    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue
        self.__clamp()

    ## PRIVATE METHODS

    @classmethod
    def __from_hs(cls, h: int, s: float) -> tuple[float, float, float]:
        """
        <PRIVATE>
        A helper method for helping construct a Color object from hue and
        saturation. Given a hue and saturation, calulates the basic RGB
        values.

        Parameters:
            h (int):
                The hue attribute, given in a range of 0 - 360.
            s (float):
                A floating point representation of a color's saturation, given
                in a range of 0 - 1

        Returns:
            tuple[float, float, float]:
                A floating point representation of the equivalent RGB color
        """
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

    def __clamp(self):
        """
        <PRIVATE>
        A clamping function that serves as an internal sanity check, stopping
        attributes from having out of range values
        """
        self.red = max(0, min(self.red, 255))
        self.green = max(0, min(self.green, 255))
        self.blue = max(0, min(self.blue, 255))

    ## CLASS METHODS

    @classmethod
    def from_hsv(cls, hue: int = 0, saturation: float = 1, value: float = 1) -> Self:
        """
        <CONSTRUCTOR>
        Given HSV values, convert them to RGB and create a color object.

        Parameters:
            h (int):
                The hue attribute, given in a range of 0 - 360.
            s (float):
                A floating point representation of saturation, given in a range
                of 0 - 1
            v (float):
                A floating point representation of value, given in a range of
                0 - 1

        Returns:
            Bopimo_Color:
                A newly created color object, converted from HSV
        """
        r, g, b = cls.__from_hs(hue, saturation)
        c = cls(int(r * value * 255), int(g * value * 255), int(b * value * 255))
        c.__clamp()
        return c

    ## INSTANCE METHODS

    def copy(self) -> Self:
        """
        Creates an identical copy of itself. A dedicated method in case level
        makers don't want to import the copy module.

        Returns:
            Bopimo_Color:
                A new color object with the same attributes as the current.
        """
        return copy(self)

    def json(self) -> dict[str, Any]:
        """
        Convert the color to bopjson, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A bopjson color object
        """
        return {"type": self.bopjson_type_name, "value": self.to_obj()}

    def to_obj(self) -> dict[str, int]:
        """
        Converts the color into a more literal dictionary, compatible with
        normal JSON.

        Returns:
            dict[str, int]:
                A dictionary equivalent of the color object.
        """
        return {"r": self.red, "g": self.green, "b": self.blue}

    ## DUNDER METHODS

    def __iter__(self) -> Iterator[float]:
        return iter((self.red, self.green, self.blue))

    def __copy__(self) -> Self:
        return self.__class__(self.red, self.green, self.blue)

    def __str__(self) -> str:
        return f"{self.bopjson_type_name}({self.red}, {self.green}, {self.blue})"

    ### EQUALITY METHODS

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError()
        return (
            (self.red == other.red)
            and (self.green == other.green)
            and (self.blue == other.blue)
        )

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError()
        return not (self == other)


class Vector3:
    """
    A Bopimo type that represents a specialized three element array, used to
    represent 3D coordinates or values in 3D space, for the X, Y, and Z axes
    respectively.

    Class Attributes:
        bopjson_type_name (str):
            The name of the type as detailed in the bopjson format

    Instance Attributes:
        x (float):
            The value of the coordinate in the X axis
        y (float):
            The value of the coordinate in the Y axis
        z (float):
            The value of the coordinate in the Z axis
    """

    bopjson_type_name: str = "Vector3F32"

    def __init__(self, x: float, y: float, z: float):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    ## PRIVATE METHODS

    @classmethod
    def __matrix_from_euler(cls, roll: float, pitch: float, yaw: float) -> NDArray[Any]:
        """
        <PRIVATE>
        Given a set of euler angles (in radians), calculate a rotation matrix.
        The rotation matrix is meant to be best in line with Godot's coordinate
        system, the game engine Bopimo uses.

        Parameters:
            roll (float):
                The roll (X) euler angle
            pitch (float):
                The pitch (Y) euler angle
            yaw (float):
                The yaw (Z) euler angle

        Returns:
            NDArray[Any]:
                A Numpy rotation matrix based on the given euler angles
        """
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
        """
        <CONSTRUCTOR>

        Given a set of euler angles (in radians), calculate a normal unit
        vector that is forward relative to the rotation.

        Parameters:
            roll (float):
                The roll (X) euler angle
            pitch (float):
                The pitch (Y) euler angle
            yaw (float):
                The yaw (Z) euler angle

        Returns:
            Self:
                A normal unit vector that represents the fprward direction of
                the given direction
        """
        rotation_matrix = cls.__matrix_from_euler(roll, pitch, yaw)

        forward_vector: tuple[float, float, float] = np.dot(
            rotation_matrix, np.array([0, 0, 1])
        )

        return cls(*forward_vector)

    @classmethod
    def up(cls, roll: float, pitch: float, yaw: float) -> Self:
        """
        <CONSTRUCTOR>

        Given a set of euler angles (in radians), calculate a normal unit
        vector that is up relative to the rotation.

        Parameters:
            roll (float):
                The roll (X) euler angle
            pitch (float):
                The pitch (Y) euler angle
            yaw (float):
                The yaw (Z) euler angle

        Returns:
            Self:
                A normal unit vector that represents the up direction of the
                given direction
        """
        rotation_matrix = cls.__matrix_from_euler(roll, pitch, yaw)

        up_vector: tuple[float, float, float] = np.dot(
            rotation_matrix, np.array([0, 1, 0])
        )

        return cls(*up_vector)

    @classmethod
    def left(cls, roll: float, pitch: float, yaw: float) -> Self:
        """
        <CONSTRUCTOR>

        Given a set of euler angles (in radians), calculate a normal unit
        vector that is left relative to the rotation.

        Parameters:
            roll (float):
                The roll (X) euler angle
            pitch (float):
                The pitch (Y) euler angle
            yaw (float):
                The yaw (Z) euler angle

        Returns:
            Self:
                A normal unit vector that represents the left direction of the
                given direction
        """
        rotation_matrix = cls.__matrix_from_euler(roll, pitch, yaw)

        left_vector: tuple[float, float, float] = np.dot(
            rotation_matrix, np.array([1, 0, 0])
        )

        return cls(*left_vector)

    @classmethod
    def zero(cls) -> Self:
        """
        <CONSTRUCTOR>
        A shorthand method of creating a zero vector

        Returns:
            Self:
                A newly created zero vector
        """
        return cls(0, 0, 0)

    @classmethod
    def one(cls) -> Self:
        """
        <CONSTRUCTOR>
        A shorthand method of creating a one vector

        Returns:
            Self:
                A newly created one vector
        """
        return cls(1, 1, 1)

    ## INSTANCE METHODS

    @property
    def magnitude(self) -> float:
        """
        <READ_ONLY>
        Magnitude is the vector's distance from origin (0, 0, 0)

        Returns:
            float:
                A plain distance of the vector from origin
        """
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def copy(self) -> Self:
        """
        Creates an identical copy of itself. A dedicated method in case level
        makers don't want to import the copy module.

        Returns:
            Bopimo_Vector3:
                A new vector object with the same attributes as the current.
        """
        return copy(self)

    def to_degrees(self) -> Self:
        """
        Given euler angles (in radians) represented in a Vector, give an
        equivalent vector in degrees.

        Returns:
            Bopimo_Vector3:
                The vector converted to degrees.
        """
        return self.__class__(
            math.degrees(self.x), math.degrees(self.y), math.degrees(self.z)
        )

    def to_radians(self) -> Self:
        """
        Given euler angles (in degrees) represented in a Vector, give an
        equivalent vector in radians.

        Returns:
            Bopimo_Vector3:
                The vector converted to radians.
        """
        return self.__class__(
            math.radians(self.x), math.radians(self.y), math.radians(self.z)
        )

    def to_obj(self) -> dict[str, float]:
        """
        Converts the vector into a more literal dictionary, compatible with
        normal JSON.

        Returns:
            dict[str, float]:
                A dictionary equivalent of the vector object.
        """
        return {"x": self.x, "y": self.y, "z": self.z}

    def json(self) -> dict[str, Any]:
        """
        Convert the vector to bopjson, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A bopjson vector object
        """
        return {"type": self.bopjson_type_name, "value": self.to_obj()}

    ## DUNDER METHODS

    def __copy__(self) -> Self:
        return self.__class__(self.x, self.y, self.z)

    def __iter__(self) -> Iterator[float]:
        return iter((self.x, self.y, self.z))

    def __str__(self) -> str:
        return f"{self.bopjson_type_name}({self.x}, {self.y}, {self.z})"

    ### OPERATOR METHODS

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Self) -> Self:
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: int | float) -> Self:
        return self.__class__(self.x * other, self.y * other, self.z * other)

    def __div__(self, other: int | float) -> Self:
        if other == 0:
            raise ZeroDivisionError()
        return self.__class__(self.x / other, self.y / other, self.z / other)

    def __truediv__(self, other: int | float) -> Self:
        return self.__div__(other)

    def __divmod__(self, other: int | float) -> Self:
        if other == 0:
            raise ZeroDivisionError()
        return self.__class__(self.x % other, self.y % other, self.z % other)

    def __neg__(self) -> Self:
        return self.__class__(-self.x, -self.y, -self.z)

    ### EQUALITY METHODS

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError()
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError()
        return not (self == other)


class Vector3Array:
    """
    A custom data structure that is meant to resemble an array of Vector
    objects. This is primarily done to abstract away any underlying details
    of the data structure, in the event that the array changes implementation.

    Class Attributes:
        bopjson_type_name (str):
            The name of the type as detailed in the bopjson format

    Instance Attributes:
        list (List[Bopimo_Vector3]):
            The underlying data structure that stores the vectors
    """

    bopjson_type_name: str = Vector3.bopjson_type_name + "_Array"

    def __init__(self, vector3_list: List[Vector3] | None = None):
        if vector3_list is None:
            vector3_list = []
        self._list = vector3_list

    ## INSTANCE METHODS

    def add_vector(self, vector: Vector3):
        """
        Adds a vector into the array

        Parameters:
            vector (Bopimo_Vector3):
                The Bopimo vector to be added into the array
        """
        self._list.append(vector)

    def clear(self):
        """
        Clears the array of all its elements.
        """
        self._list.clear()

    def copy(self, deep: bool = True) -> Self:
        """
        Copies all of the elements in a new array without having to import
        the copy module.

        By default, this method will deep copy the elements.

        Parameters:
            deep (bool):
                Whether to deep copy the elements. For a true shallow copy, set
                this to False.

        Returns:
            Bopimo_Vector3Array:
                A newly created array containing identical elements
        """
        if deep:
            return deepcopy(self)
        return copy(self)

    def get_vector(self, index: int) -> Vector3:
        """
        Get a vector from the array, given an index

        Parameters:
            index (int):
                The position in the list to grab a vector from.

        Returns:
            Bopimo_Vector3:
                The vector at the given index
        """
        return self._list[index]

    def set_vector(self, index: int, vector: Vector3):
        """
        Replace a vector in the array with a new one.

        Parameters:
            index (int):
                The position in the list to set a vector in
            vector (Bopimo_Vector3):
                The new vector to replace in the array
        """
        self._list[index] = vector

    def is_empty(self) -> bool:
        """
        Determines whether the array is empty or not

        Returns:
            bool:
                Whether the list is empty
        """
        return len(self) == 0

    def remove_vector(self, index: int) -> Vector3:
        """
        Removes a vector from the array, given an index

        Parameters:
            index (int):
                The position in the list to remove a vector from

        Returns:
            Bopimo_Vector3:
                The removed vector from the list
        """
        return self._list.pop(index)

    def json(self) -> dict[str, Any]:
        """
        Convert the array to bopjson, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A bopjson array object
        """
        obj: dict[str, Any] = {"type": self.bopjson_type_name, "value": []}
        for vector3 in self._list:
            obj["value"].append(vector3.to_obj())
        return obj

    ## DUNDER METHODS

    def __copy__(self) -> Self:
        return self.__class__(copy(self._list))

    def __deepcopy__(self, memo: dict[Any, Any]) -> Self:
        return self.__class__(deepcopy(self._list, memo))

    def __str__(self) -> str:
        s = "Vector3Array("
        for vec in self._list:
            s = s + str(vec)
            if self._list[-1] != vec:
                s = s + ", "
        return s + ")"

    ### OPERATOR METHODS

    def __add__(self, other: "Vector3Array" | List[Vector3]) -> "Vector3Array":
        if isinstance(other, Vector3Array):
            return Vector3Array(self._list + other._list)
        else:
            return Vector3Array(self._list + other)

    ### ITERABLE METHODS

    def __iter__(self) -> Iterator[Vector3]:
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
        for vec1, vec2 in zip(self._list, other._list):
            if vec1 != vec2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError()
        return not (self == other)


class ColorArray:
    """
    A custom data structure that is meant to resemble an array of Color
    objects. This is primarily done to abstract away any underlying details
    of the data structure, in the event that the array changes implementation.

    Class Attributes:
        bopjson_type_name (str):
            The name of the type as detailed in the bopjson format

    Instance Attributes:
        list (List[Bopimo_Color]):
            The underlying data structure that stores the color
    """

    bopjson_type_name: str = Color.bopjson_type_name + "_Array"

    def __init__(self, color_list: List[Color] | None = None):
        if color_list is None:
            color_list = []
        self._list = color_list

    ## INSTANCE METHODS
    def add_color(self, color: Color):
        """
        Adds a color into the array

        Parameters:
            color (Bopimo_Color):
                The Bopimo color to be added into the array
        """
        self._list.append(color)

    def clear(self):
        """
        Clears the array of all its elements
        """
        self._list.clear()

    def copy(self, deep: bool = True) -> Self:
        """
        Copies all of the elements in a new array without having to import
        the copy module.

        By default, this method will deep copy the elements.

        Parameters:
            deep (bool):
                Whether to deep copy the elements. For a true shallow copy, set
                this to False.

        Returns:
            Bopimo_ColorArray:
                A newly created array containing identical elements
        """
        if deep:
            return deepcopy(self)
        return copy(self)

    def get_color(self, index: int) -> Color:
        """
        Get a color from the array, given an index

        Parameters:
            index (int):
                The position in the list to grab a color from.

        Returns:
            Bopimo_Color:
                The color object at the given index
        """
        return self._list[index]

    def set_color(self, index: int, color: Color):
        """
        Replace a color in the array with a new one.

        Parameters:
            index (int):
                The position in the list to set a color in
            color (Bopimo_Vector3):
                The new color to replace in the array
        """
        self._list[index] = color

    def is_empty(self) -> bool:
        """
        Determines whether the array is empty or not

        Returns:
            bool:
                Whether the list is empty
        """
        return len(self._list) == 0

    def remove_color(self, index: int) -> Color:
        """
        Removes a color from the array, given an index

        Parameters:
            index (int):
                The position in the list to remove a color from

        Returns:
            Bopimo_Vector3:
                The removed color from the list
        """
        return self._list.pop(index)

    def json(self) -> dict[str, Any]:
        """
        Convert the array to bopjson, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A bopjson array object
        """
        obj: dict[str, Any] = {"type": self.bopjson_type_name, "value": []}
        for color in self._list:
            obj["value"].append(color.to_obj())
        return obj

    ## DUNDER METHODS

    def __copy__(self) -> Self:
        return self.__class__(copy(self._list))

    def __deepcopy__(self, memo: dict[Any, Any]) -> Self:
        return self.__class__(deepcopy(self._list, memo))

    def __str__(self) -> str:
        s = "ColorArray("
        for col in self._list:
            s = s + str(col)
            if self._list[-1] != col:
                s = s + ", "
        return s + ")"

    ### OPERATOR METHODS

    def __add__(self, other: "ColorArray" | List[Color]) -> "ColorArray":
        if isinstance(other, ColorArray):
            return ColorArray(self._list + other._list)
        else:
            return ColorArray(self._list + other)

    ### ITERABLE METHODS

    def __iter__(self) -> Iterator[Color]:
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
        for col1, col2 in zip(self._list, other._list):
            if col1 != col2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError()
        return not (self == other)


# This will come up often because though integers are technically acceptable, enums are more future-proof.
type Bopimo_Integer = int | IntEnum


class IntArray:
    """
    A custom data structure that is meant to resemble an array of integers.
    This is primarily done to abstract away any underlying details of the data
    structure, in the event that the array changes implementation.

    Due to Python's integers not having a bit limit, this class functions as a
    superclass that both the 32 and 64 bit variants inherit from to deduplicate
    code.

    Class Attributes:
        bopjson_type_name (str):
            The name of the type as detailed in the bopjson format

    Instance Attributes:
        list (List[Bopimo_Integer]):
            The underlying data structure that stores the integers
    """

    bopjson_type_name: str = "Int_Array"

    def __init__(self, int_list: List[Bopimo_Integer] | None = None):
        if int_list is None:
            int_list = []
        self._list = int_list

    ## INSTANCE METHODS

    def add_int(self, integer: Bopimo_Integer):
        """
        Adds an integer into the array

        Parameters:
            integer (Bopimo_Integer):
                The integer to be added into the array
        """
        self._list.append(integer)

    def clear(self):
        """
        Clears the array of all its elements.
        """
        self._list.clear()

    def copy(self, deep: bool = True) -> Self:
        """
        Copies all of the elements in a new array without having to import
        the copy module.

        By default, this method will deep copy the elements.

        Parameters:
            deep (bool):
                Whether to deep copy the elements. For a true shallow copy, set
                this to False.

        Returns:
            Bopimo_IntArray:
                A newly created array containing identical elements
        """
        if deep:
            return deepcopy(self)
        return copy(self)

    def get_int(self, index: int) -> Bopimo_Integer:
        """
        Get an integer from the array, given an index

        Parameters:
            index (int):
                The position in the list to grab a integer from.

        Returns:
            Bopimo_Integer:
                The integer object at the given index
        """
        return self._list[index]

    def set_int(self, index: int, integer: Bopimo_Integer):
        """
        Replace an integer in the array with a new one.

        Parameters:
            index (int):
                The position in the list to set an integer in
            integer (Bopimo_Integer):
                The new integer to replace in the array
        """
        self._list[index] = integer

    def is_empty(self) -> bool:
        """
        Determines whether the array is empty or not

        Returns:
            bool:
                Whether the list is empty
        """
        return len(self._list) == 0

    def remove_int(self, index: int) -> Bopimo_Integer:
        """
        Removes a integer from the array, given an index

        Parameters:
            index (int):
                The position in the list to remove an integer from

        Returns:
            Bopimo_Integer:
                The removed integer from the list
        """
        return self._list.pop(index)

    def json(self) -> dict[str, Any]:
        """
        Convert the array to bopjson, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A bopjson array object
        """
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

    ### OPERATOR METHODS

    def __add__(self, other: "IntArray" | List[int]) -> "IntArray":
        if isinstance(other, IntArray):
            return IntArray(self._list + other._list)
        else:
            return IntArray(self._list + other)

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


class Int32Array(IntArray):
    """
    <INHERITED IntArray>

    The 32-bit variant of an integer array that is meant to resemble 32-bit
    integers.

    Instance Attributes:
        signed (bool):
            Determines whether to use signed or unsigned integers
    """

    bopjson_type_name: str = "Int32_Array"

    def __init__(self, int_list: List[Bopimo_Integer] | None = None):
        if int_list is None:
            int_list = []
        self._list = int_list
        self.signed = False

    def json(self) -> dict[str, Any]:
        """
        Convert the array to bopjson, as part of the exporting process. In
        addition, each number will be checked to ensure it is inside the 32-bit
        range. If it is overflowing or underflowing, this method will raise an
        error.

        Returns:
            dict[str, Any]:
                A bopjson array object
        """
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


class Int64Array(IntArray):
    """
    <INHERITED IntArray>

    The 64-bit variant of an integer array that is meant to resemble 64-bit
    integers.

    Instance Attributes:
        signed (bool):
            Determines whether to use signed or unsigned integers
    """

    bopjson_type_name: str = "Int64_Array"

    def __init__(self, int_list: List[Bopimo_Integer] | None = None):
        if int_list is None:
            int_list = []
        self._list = int_list
        self.signed = False

    def json(self) -> dict[str, Any]:
        """
        Convert the array to bopjson, as part of the exporting process. In
        addition, each number will be checked to ensure it is inside the 64-bit
        range. If it is overflowing or underflowing, this method will raise an
        error.

        Returns:
            dict[str, Any]:
                A bopjson array object
        """
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


class Float32Array:
    """
    A custom data structure that is meant to resemble an array of floating
    point numbers.

    While this class will accept Python floats for construction and arguments,
    all Python floats will be converted to Numpy's 32-bit floating point number
    type. This is to ensure correctness with the precision when translating to
    JSON, as most machines will make Python floats "double-precision floating
    point numbers" (IEEE 754 64-bit). During this conversion, some precision
    may be lost.

    In addition, when retrieving a value from this structure, you will always get
    a Python float to ensure the best compatibility.

    Class Attributes:
        bopjson_type_name (str):
            The name of the type as detailed in the bopjson format

    Instance Attributes:
        list (List[float]):
            The underlying data structure that stores the floating values
    """

    bopjson_type_name: str = "Float32_Array"

    def __init__(
        self,
        float_list: List[float] | List[np.float32] | NDArray[np.float32] | None = None,
    ):
        self._list: List[np.float32]
        if float_list is None:
            float_list = []
        if isinstance(float_list, List):
            self._list = []
            for f in float_list:
                # I would write this more cleanly to distinguish numpy floats from Python floats, but Pylance sucks
                if isinstance(f, float) or isinstance(f, int):
                    self._list.append(np.float32(f))
                else:
                    self._list.append(f)
        else:
            self._list = float_list.tolist()

    ## INSTANCE METHODS

    def add_float(self, f: float | np.float32):
        """
        Adds a float into the array

        Parameters:
            f (float | numpy.float32):
                The float to be added into the array
        """
        if isinstance(f, float) or isinstance(f, int):
            f = np.float32(f)
        self._list.append(f)

    def clear(self):
        """
        Clears the array of all its elements.
        """
        self._list.clear()

    def copy(self, deep: bool = True) -> Self:
        """
        Copies all of the elements in a new array without having to import
        the copy module.

        By default, this method will deep copy the elements.

        Parameters:
            deep (bool):
                Whether to deep copy the elements. For a true shallow copy, set
                this to False.

        Returns:
            Bopimo_Float32Array:
                A newly created array containing identical elements
        """
        if deep:
            return deepcopy(self)
        return copy(self)

    def get_float(self, index: int) -> float:
        """
        Get a float from the array, given an index

        Parameters:
            index (int):
                The position in the list to grab a float from.

        Returns:
            float:
                The float at the given index
        """
        return self._list[index].item()

    def set_float(self, index: int, f: float | np.float32):
        """
        Replace a float in the array with a new one.

        Parameters:
            index (int):
                The position in the list to set a float in
            f (float | numpy.float32):
                The new float to replace in the array
        """
        if isinstance(f, float) or isinstance(f, int):
            f = np.float32(f)
        self._list[index] = f

    def is_empty(self) -> bool:
        """
        Determines whether the array is empty or not

        Returns:
            bool:
                Whether the list is empty
        """
        return len(self._list) == 0

    def remove_float(self, index: int) -> float:
        """
        Removes a float from the array, given an index

        Parameters:
            index (int):
                The position in the list to remove a float from

        Returns:
            float:
                The removed float from the list
        """
        return self._list.pop(index).item()

    def json(self) -> dict[str, Any]:
        """
        Convert the array to bopjson, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A bopjson array object
        """
        values: List[float] = []
        for value in self._list:
            values.append(value.item())
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

    ### OPERATOR METHODS

    def __add__(
        self,
        other: "Float32Array" | List[float] | List[np.float32] | NDArray[np.float32],
    ) -> Self:
        if isinstance(other, Float32Array):
            return self.__class__(self._list + other._list)
        elif isinstance(other, List):
            o: List[np.float32] = []
            for f in other:
                if isinstance(f, float) or isinstance(f, int):
                    o.append(np.float32(f))
                else:
                    o.append(f)
            return self.__class__(self._list + o)
        else:
            return self.__class__(np.append(arr=self._list, values=other))

    ### ITERABLE METHODS

    def __iter__(self) -> Iterator[np.float32]:
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


## ALIASES FOR REVERSE COMPATIBILITY

Bopimo_Color = Color
Bopimo_Vector3 = Vector3
Bopimo_Vector3Array = Vector3Array
Bopimo_ColorArray = ColorArray
Bopimo_IntArray = IntArray
Bopimo_Int32Array = Int32Array
Bopimo_Int64Array = Int64Array
Bopimo_Float32Array = Float32Array
