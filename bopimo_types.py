import math
from copy import copy, deepcopy
from enum import IntEnum
import numpy as np
from numpy.typing import NDArray
from typing import Any, Iterator, List, Self


class Bopimo_Color:
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
    def from_hsv(
        cls, hue: int = 0, saturation: float = 1, value: float = 1
    ) -> "Bopimo_Color":
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
        c = Bopimo_Color(
            int(r * value * 255), int(g * value * 255), int(b * value * 255)
        )
        c.__clamp()
        return c

    ## INSTANCE METHODS

    def copy(self) -> "Bopimo_Color":
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
        # FIXME: Add type hints to the attributes
        self.x = x
        self.y = y
        self.z = z

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

    def copy(self) -> "Bopimo_Vector3":
        """
        Creates an identical copy of itself. A dedicated method in case level
        makers don't want to import the copy module.

        Returns:
            Bopimo_Vector3:
                A new vector object with the same attributes as the current.
        """
        return copy(self)

    def to_degrees(self) -> "Bopimo_Vector3":
        """
        Given euler angles (in radians) represented in a Vector, give an
        equivalent vector in degrees.

        Returns:
            Bopimo_Vector3:
                The vector converted to degrees.
        """
        return Bopimo_Vector3(
            math.degrees(self.x), math.degrees(self.y), math.degrees(self.z)
        )

    def to_radians(self) -> "Bopimo_Vector3":
        """
        Given euler angles (in degrees) represented in a Vector, give an
        equivalent vector in radians.

        Returns:
            Bopimo_Vector3:
                The vector converted to radians.
        """
        return Bopimo_Vector3(
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

    bopjson_type_name: str = Bopimo_Vector3.bopjson_type_name + "_Array"

    def __init__(self, vector3_list: List[Bopimo_Vector3] | None = None):
        if vector3_list is None:
            vector3_list = []
        self._list = vector3_list

    ## INSTANCE METHODS

    def add_vector(self, vector: Bopimo_Vector3):
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

    def copy(self, deep: bool = True) -> "Bopimo_Vector3Array":
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

    def get_vector(self, index: int) -> Bopimo_Vector3:
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

    def set_vector(self, index: int, vector: Bopimo_Vector3):
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

    def remove_vector(self, index: int) -> Bopimo_Vector3:
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

    ### OPERATOR METHODS

    def __add__(
        self, other: "Bopimo_Vector3Array" | List[Bopimo_Vector3]
    ) -> "Bopimo_Vector3Array":
        if isinstance(other, Bopimo_Vector3Array):
            return Bopimo_Vector3Array(self._list + other._list)
        else:
            return Bopimo_Vector3Array(self._list + other)

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

    bopjson_type_name: str = Bopimo_Color.bopjson_type_name + "_Array"

    def __init__(self, color_list: List[Bopimo_Color] | None = None):
        if color_list is None:
            color_list = []
        self._list = color_list

    ## INSTANCE METHODS
    # FIXME: Rename the parameter to the correct name
    def add_color(self, vector: Bopimo_Color):
        """
        Adds a color into the array

        Parameters:
            color (Bopimo_Color):
                The Bopimo color to be added into the array
        """
        self._list.append(vector)

    def clear(self):
        """
        Clears the array of all its elements
        """
        self._list.clear()

    def copy(self, deep: bool = True) -> "Bopimo_ColorArray":
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

    def get_color(self, index: int) -> Bopimo_Color:
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

    def set_color(self, index: int, color: Bopimo_Color):
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

    def remove_color(self, index: int) -> Bopimo_Color:
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

    ### OPERATOR METHODS

    def __add__(
        self, other: "Bopimo_ColorArray" | List[Bopimo_Color]
    ) -> "Bopimo_ColorArray":
        if isinstance(other, Bopimo_ColorArray):
            return Bopimo_ColorArray(self._list + other._list)
        else:
            return Bopimo_ColorArray(self._list + other)

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


class Bopimo_IntArray:
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

    def __add__(self, other: "Bopimo_IntArray" | List[int]) -> "Bopimo_IntArray":
        if isinstance(other, Bopimo_IntArray):
            return Bopimo_IntArray(self._list + other._list)
        else:
            return Bopimo_IntArray(self._list + other)

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
    """
    <INHERITED Bopimo_IntArray>

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


class Bopimo_Int64Array(Bopimo_IntArray):
    """
    <INHERITED Bopimo_IntArray>

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


# FIXME: Use numpy and their 32-bit float to ensure precision correctness.
class Bopimo_Float32Array:
    """
    A custom data structure that is meant to resemble an array of floating
    point numbers.

    Keep in mind that even though this data structure is meant to represent
    32-bit floating point numbers (IEEE 754 32-bit), most machines will use
    double floating point numbers in Python (IEEE 754 64-bit). As a result,
    some precision will be lost in the final conversion.

    Class Attributes:
        bopjson_type_name (str):
            The name of the type as detailed in the bopjson format

    Instance Attributes:
        list (List[float]):
            The underlying data structure that stores the floating values
    """

    bopjson_type_name: str = "Float32_Array"

    def __init__(self, float_list: List[float] | None = None):
        if float_list is None:
            float_list = []
        self._list = float_list

    ## INSTANCE METHODS

    def add_float(self, float: float):
        """
        Adds a float into the array

        Parameters:
            float (float):
                The float to be added into the array
        """
        self._list.append(float)

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
        return self._list[index]

    def set_float(self, index: int, float: float):
        """
        Replace a float in the array with a new one.

        Parameters:
            index (int):
                The position in the list to set a float in
            float (float):
                The new float to replace in the array
        """
        self._list[index] = float

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
        return self._list.pop(index)

    def json(self) -> dict[str, Any]:
        """
        Convert the array to bopjson, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A bopjson array object
        """
        values: List[float] = []
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

    def __add__(
        self, other: "Bopimo_Float32Array" | List[float]
    ) -> "Bopimo_Float32Array":
        if isinstance(other, Bopimo_Float32Array):
            return Bopimo_Float32Array(self._list + other._list)
        else:
            return Bopimo_Float32Array(self._list + other)

    ### ITERABLE METHODS

    def __iter__(self) -> Iterator[float]:
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
