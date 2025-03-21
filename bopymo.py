from bopimo_types import (
    Bopimo_Color,
    Bopimo_Vector3,
    Bopimo_Vector3Array,
    Bopimo_Float32Array,
    Bopimo_Int32Array,
    Bopimo_Int64Array,
    Bopimo_ColorArray,
)

from copy import deepcopy
import datetime
from enum import IntEnum
import logging
import math
from numpy import dot
import json
import random
import time
from typing import Any, List, Self

# Change how much information you want to display on the console when you use Bopymo.
LOG_LEVEL = logging.INFO
LOG_FMT = "[%(levelname)s] - %(message)s"
logging.basicConfig(level=LOG_LEVEL, format=LOG_FMT)
# Here's a quick way to see what features are deprecated, and also ensure to only send one warning per deprecation.
DEPRECATION_WARNINGS: dict[str, bool] = {
    "Getting position_points directly": False,
    "Setting position_points directly": False,
}


class Game_Version:
    """
    This class represents the semantic versioning structure that Bopimo uses.
    This is used to not only mark the bopjson version in the metadata, but is
    integral to version checking to ensure that attributes and objects are
    being used in appropriate version.

    Attributes:
        major (int): The major number of a version
        minor (int): The minor number of a version
        micro (int): The micro (or patch) number of a version
    """

    def __init__(self, major: int, minor: int, micro: int):
        self.major = major
        self.minor = minor
        self.micro = micro

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Game_Version):
            raise TypeError()
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.micro == other.micro
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Game_Version):
            raise TypeError()
        if self.major > other.major:
            return False
        elif self.major < other.major:
            return True
        else:
            if self.minor > other.minor:
                return False
            elif self.minor < other.minor:
                return True
            else:
                return self.micro < other.micro

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Game_Version):
            raise TypeError()
        if self.major < other.major:
            return False
        elif self.major > other.major:
            return True
        else:
            if self.minor < other.minor:
                return False
            elif self.minor > other.minor:
                return True
            else:
                return self.micro > other.micro

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Game_Version):
            raise TypeError()
        return self < other or self == other

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Game_Version):
            raise TypeError()
        return self > other or self == other

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Game_Version):
            raise TypeError()
        return not (self == other)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.micro}"


# This is a constant that is used to represent the latest version of Bopimo
# If your level doesn't specify a version, this value will be used by default
GAME_VERSION = Game_Version(1, 0, 15)

### ENUMS


class Block_ID(IntEnum):
    """
    Bopimo differentiates their objects through a numeric ID. This enum makes
    it easy to see what the different IDs for objects are. Cube should be the
    default, but invalid IDs will be resolved to NULL (-1)
    """

    NULL = -1

    # PRIMITIVES
    CUBE = 0
    RAMP = 1
    CYLINDER = 2
    SPHERE = 5
    CORNER_RAMP = 7
    CONE = 8
    PYRAMID = 12
    PYRAMID_CORNER = 13
    ROUNDED_RAMP = 15
    HOLE = 20
    ARCH = 21
    HALF_ARCH = 22
    LOOP = 32

    # DECORATION
    PINE_TREE = 1000
    PINE_TREE_SNOW = 1001
    LOGO = 1002
    LOGO_ICON = 1003
    PALM_TREE = 1004
    STREET_LAMP = 1005
    FLOWER = 1006
    FENCE = 1007
    TORCH = 1008
    STRING_LIGHTS = 1009
    ROSE = 1014
    MESH = 1100
    CLOUD = 1101
    STATUE = 1102

    # ACTION
    SPRING = 2000
    WATER = 2001
    SPAWN = 2002
    CHECKPOINT = 2003
    TOKEN = 2004
    LADDER = 2005
    ICE = 2006
    COMPLETION_STAR = 2007
    LAVA = 2008
    BOOST_PANEL = 2009
    SPEED_PANEL = 2010
    GRATES = 2011
    DISAPPEARING_BLOCK = 2012
    MISSILE_LAUNCHER = 2013
    BREAKABLE_BLOCK = 2014
    CANNON = 2015
    PORTAL = 2016
    WEB = 2025

    # NPC
    BOPI_SPAWNER = 3000

    # HIDDEN
    HYACINTH = 1010
    ANALOG_CLOCK = 1012
    GLOOMLIGHT_SPAWNER = 3100
    ITEM_GRANTER = 60000
    BLEEDING_EYE = 61366


class Block_Pattern(IntEnum):
    """
    Bopimo objects with patterns will represent their patterns use a numeric
    ID. By default, objects will use the checkerboard pattern (0).

    If you are aiming for no pattern, the easiest way to do so is by matching
    the pattern color with the block color.
    """

    CHECKERBOARD = 0
    HEX = 1
    STRIPES = 2
    PLANKS = 3
    ZIG_ZAG = 4
    CIRCLES = 5
    DIAMONDS = 6
    LARGE_DIAMONDS = 7
    BRICKS = 8
    LARGE_BRICKS = 9
    WAVES = 10
    CHEVRON = 11
    GEOMETRIC = 12
    HORIZONTAL_STRIPES = 13
    VERTICAL_STRIPES = 14
    X = 15
    HEARTS = 17


class Sky(IntEnum):
    """
    Bopimo offers various different skyboxes that help set the basic atmosphere
    for the level. This is represented by a numeric ID and this contains all
    of the skyboxes you can choose from.
    """

    DAY = 0
    SUNSET = 1
    NIGHT = 2
    RAINDROP = 3
    ALIEN = 4
    DULL = 5
    WINTER = 6
    INFERNAL = 7
    FLAME = 8
    GOLDEN = 9
    VIOLET = 10
    THE_SUN = 11
    HALLOWEEN = 12
    OVERCAST = 13
    STARLIT_CITY = 14
    VOID = 15
    DESERT = 16


class Weather(IntEnum):
    """
    You can introduce weather into your Bopimo level to enhance the atmosphere
    of the level. This enum contains all of the different types of weather you
    can choose from. By default, there will be no weather (CLEAR)
    """

    CLEAR = 0
    SNOW = 1
    RAIN = 2
    VOID = 3
    AUTUMN = 4


class Music(IntEnum):
    """
    Bopimo has its own unique soundtrack that is produced by the developers.
    This enum gives you all of the different song names and their associated
    numeric IDs.
    """

    SERENE = 0
    SWAYING_DREAMS = 1
    PLAYFUL_WALTZ = 2
    SICILIAN_STREET = 3
    CONTEMPLATION = 4
    CAVE_AMBIENCE = 5
    FUNKY = 6
    DARKNESS_APPROACHES = 7
    CARNIVAL = 8
    LATE_NIGHT_FIREWORKS = 9
    I_DONT_KNOW = 10
    WINTER_FOREST = 11
    ASSAULT_ON_THE_EAR_DRUMS = 12
    BLOOD_MOON = 13
    ISAIAH_NEW_SONG = 14
    BAMBA = 15
    TORTUGA = 16
    FRIVOLOUS_FLUTES = 17
    SIXTY_FOUR = 64


### BOPIMO CLASSES


# TODO: Try and find a way to version check various Bopimo attributes, to try and incorporate backwards compatibility
class Bopimo_Property:
    def __init__(self, value: Any, min_version: Game_Version = Game_Version(1, 0, 11)):
        self.value = value
        self.min_version = min_version

    def compatible(self, level_version: Game_Version) -> bool:
        return level_version >= self.min_version


class Bopimo_Object:
    """
    This is the superclass that represents all Bopimo objects. Every block or
    object that you plan on putting into a level will inherit from this class,
    hence this class includes all the basic attributes and methods that you can
    call from any object.

    Class attributes:
        MIN_VERSION (Game_Version):
            A constant representing the earliest version the object can be used
            in a level.
    Instance attributes:
        id (Block_ID | int):
            The identifier that establishes the type of object the object will
            represent from.
        name (str):
            The name of the object
        nametag (bool):
            If true, displays the name of the object as text above the object.
            Useful for conveying information.
        color (Bopimo_Color):
            The color of the object
        position (Bopimo_Vector3):
            The position of the object in 3D space
        rotation (Bopimo_Vector3):
            The rotation of the object represented as euler angles. Rotation is
            in degrees.
        scale (Bopimo_Vector3):
            The size of the object in 3D space

        movement_flags (int):
            <INTERNAL> <NON-FUNCTIONAL> <UNIMPLEMENTED>
            A value that, if non-zero, can restrict what kinds of movement a
            player can make if they interact with this object.

        position_enabled (bool):
            If true, will enable position kinematics.
        position_points (Bopimo_Vector3Array):
            A sequence of position points the object will travel to in order.
            Positions are relative to the origin of the object.
        position_travel_speed (float):
            <REVERSE_COMPAT>
            A constant speed the object will move to each position point. This
            was the legacy method of position kinematics and was replaced with
            time-based kinematics in Bopimo 1.0.14. However, this has full
            reverse compatibility.
        position_travel_times (Bopimo_Float32Array):
            A sequence of durations (in seconds) it takes to get from the
            current point to the next one (or in the case of the last, getting
            back to the beginning). This is meant to stay in sync with the
            position points array, so it will have the same length as position
            points.

        rotation_enabled (bool):
            If true, will enable rotation kinematics
        rotation_pivot_offset (Bopimo_Vector3):
            Represents how much to move the center of rotation of the pivot.
            Position is relative to the origin of the object.
        rotation_direction (Bopimo_Vector3):
            A normal unit vector that represents the axis of rotation the
            object will rotate on
        rotation_speed (float):
            How fast the object will rotate, in a constant speed.
    """

    MIN_VERSION = Game_Version(1, 0, 14)

    def __init__(
        self,
        id: Block_ID | int = Block_ID.NULL,
        name: str = "Object",
        color: Bopimo_Color = Bopimo_Color(0, 0, 0),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        self.id: Block_ID | int = id
        self.name: str = name
        self.nametag: bool = False
        self.color: Bopimo_Color = color
        self.position: Bopimo_Vector3 = position
        self.rotation: Bopimo_Vector3 = rotation
        self.scale: Bopimo_Vector3 = scale

        # TODO: Add "movement_flags". They're currently in the code, but not functional at the moment.

        self.position_enabled: bool = False
        self._position_points: Bopimo_Vector3Array = Bopimo_Vector3Array()
        # As of Bopimo 1.0.14, position_travel_speed no longer exists in bopjson. This value is now None, which indicates it is disabled.
        # Setting this value to 0 will also re-enable the time-based kinematic system.
        self._position_travel_speed: float | None = None
        self._position_travel_times: Bopimo_Float32Array = Bopimo_Float32Array()

        self.rotation_enabled: bool = False
        self.rotation_pivot_offset: Bopimo_Vector3 = Bopimo_Vector3.zero()
        self.rotation_direction: Bopimo_Vector3 = Bopimo_Vector3.zero()
        self.rotation_speed: float = 1

    def __refresh_constant_travel_speed_times(self):
        """
        <PRIVATE>
        If a position_travel_speed has a declared value and non-zero, will go
        through all of the position points and calculates the travel times
        based on the given speed. This method is crucial for ensuring reverse
        compatibility with the previous speed-based kinematic system.
        """
        if self._position_travel_speed is None:
            return
        for i, position in enumerate(self._position_points):
            next_pos: Bopimo_Vector3
            if i == len(self._position_points) - 1:
                next_pos = self._position_points.get_vector(0)
            else:
                next_pos = self._position_points.get_vector(i + 1)
            distance: float = (next_pos - position).magnitude
            self._position_travel_times.set_float(
                i, distance / self._position_travel_speed
            )

    @property
    def position_travel_speed(self) -> float:
        """
        A getter method for the position_travel_speed attribute.

        Returns:
            float:
                The object's position travel speed.
        """
        if self._position_travel_speed is None:
            return 0
        return self._position_travel_speed

    @property
    def position_points(self) -> Bopimo_Vector3Array:
        """
        <DEPRECATED>
        A getter method for the position_points attribute. This getter method
        is ONLY meant to be used with speed-based kinematics, as the primary
        purpose of this function is reverse compatibility.

        Returns:
            Bopimo_Vector3Array:
                The sequence of the object's position points
        """
        if not DEPRECATION_WARNINGS["Getting position_points directly"]:
            logging.warning(
                "Getting position_points directly is deprecated. This will be removed in a future version of Bopymo. Please use methods to access position points instead."
            )
            DEPRECATION_WARNINGS["Getting position_points directly"] = True
        if self._position_travel_speed is None:
            logging.warning(
                "You are grabbing position_points directly before declaring a constant travel speed. Setting speed to 5."
            )
            self.position_travel_speed = 5
        if self._position_travel_speed != 0:
            return self._position_points
        # If you are using the new system which involve travel times, you shouldn't get the actual points as they're linked with the time points.
        return Bopimo_Vector3Array([])

    @position_travel_speed.setter
    def position_travel_speed(self, value: float):
        """
        A setter method for the position_travel_speed attribute.

        Parameters:
            value (float):
                The new value for position_travel_speed
        """
        self._position_travel_speed = value
        if value != 0:
            self.__refresh_constant_travel_speed_times()

    @position_points.setter
    def position_points(self, points: Bopimo_Vector3Array):
        """
        <DEPRECATED>
        A setter method for the position_points attribute. This setter method
        is ONLY meant to be used with speed-based kinematics, as the primary
        purpose of this function is reverse compatibility. If a position travel
        speed is not already specified, one will be provided (the previous
        default value of 5).

        Parameters:
            points (Bopimo_Vector3Array):
                A new sequence of position points
        """
        if not DEPRECATION_WARNINGS["Setting position_points directly"]:
            logging.warning(
                "Setting position_points directly is deprecated. This will be removed in a future version of Bopymo. Please use methods to set position points instead."
            )
            DEPRECATION_WARNINGS["Setting position_points directly"] = True
        # Bopimo 1.0.11-1.0.13 would implicitly declare the object's position (locally 0, 0, 0) as the starting position.
        # The times system requires this to be explicitly declared. So if the start is not (0, 0, 0), add it for reverse compatibility.
        positions: Bopimo_Vector3Array
        if not points.is_empty() and points.get_vector(0) != Bopimo_Vector3.zero():
            positions = Bopimo_Vector3Array([Bopimo_Vector3.zero()]) + points
        else:
            positions = points
        self._position_points = positions
        self._position_travel_times = Bopimo_Float32Array([0.0] * len(positions))
        # Previous default value with 1.0.11-1.0.13
        if self._position_travel_speed is None:
            self.position_travel_speed = 5
        if self._position_travel_speed != 0:
            self.__refresh_constant_travel_speed_times()

    def add_position_point(self, position: Bopimo_Vector3, time: float = 0.0):
        """
        Adds a position point to the object's position points, along with an
        associated travel time. If a position travel speed has been given to
        the object, the travel time will be ignored.

        Parameters:
            position (Bopimo_Vector3):
                A position relative to the object's origin, to be added to the
                sequence of position points.
            time (float):
                A travel time (in seconds) that will be paired with the
                position, to get from the given position to either the next
                position, or the start position if it is the last in the
                sequence. This parameter is optional. so if you're using
                speed-based kinematics you can omit this parameter.
        """
        self._position_points.add_vector(position)
        if self.position_travel_speed == 0:
            self._position_travel_times.add_float(time)
        else:
            if len(self._position_points) < 2:
                self._position_travel_times.add_float(0)
                return
            prev_pos: Bopimo_Vector3 = self._position_points.get_vector(
                len(self._position_points) - 2
            )
            distance: float = (position - prev_pos).magnitude
            self._position_travel_times.set_float(
                len(self._position_points) - 2,
                distance / self.position_travel_speed,
            )
            next_pos: Bopimo_Vector3 = self._position_points.get_vector(0)
            distance: float = (next_pos - position).magnitude
            self._position_travel_times.add_float(distance / self.position_travel_speed)

    def add_position_points(
        self, position_times: List[tuple[Bopimo_Vector3, float]] | List[Bopimo_Vector3]
    ):
        """
        Adds a list of position points to the object's position points, given
        in tuple pairs of the position, and the associated travel time. If a
        position travel speed has been given to the object, you can just give
        the stand-alone position instead of a tuple.

        If you are using speed-based kinematics and need to bulk add positions,
        it is recommended to use this method as it cuts down on redundant
        operations that would be performed to calculate the final travel time.

        Parameters:
            position_times (List[ tuple[Bopimo_Vector3, float] ]
                            | List[Bopimo_Vector3]):
                A sequence of position point and time range pairs to add to the
                object's position points and travel times. If doing speed-based
                kinematics, just a sequence of position points.
        """
        if not position_times:
            return
        e: tuple[Bopimo_Vector3, float] | Bopimo_Vector3 = position_times[-1]
        if isinstance(e, Bopimo_Vector3) and self.position_travel_speed == 0:
            raise TypeError(
                "Attempted to give a plain position, but position_travel_speed is 0. Either set a travel speed, or provide a time in seconds."
            )
        elif isinstance(e, tuple) and self.position_travel_speed != 0:
            raise TypeError(
                "Attempted to give a position and time, but position_travel_speed is non-zero. Either set position_travel_speed to 0, or remove the time."
            )
        for element in position_times:
            if isinstance(element, Bopimo_Vector3):
                # We cannot rely on add_position_point here otherwise we will be needlessly calculating the beginning point's time. That'll be saved for the end
                self._position_points.add_vector(element)
                if len(self._position_points) < 2:
                    self._position_travel_times.add_float(0)
                    continue
                prev_pos: Bopimo_Vector3 = self._position_points.get_vector(
                    len(self._position_points) - 2
                )
                distance: float = (element - prev_pos).magnitude
                self._position_travel_times.set_float(
                    len(self._position_points) - 2,
                    distance / self.position_travel_speed,
                )
                # Add a value which will be set next loop
                self._position_travel_times.add_float(0)
            else:
                self.add_position_point(*element)

        if isinstance(e, Bopimo_Vector3):
            next_pos: Bopimo_Vector3 = self._position_points.get_vector(0)
            distance: float = (next_pos - e).magnitude
            self._position_travel_times.set_float(
                len(self._position_travel_times) - 1,
                distance / self.position_travel_speed,
            )

    def get_position_point(self, index: int) -> Bopimo_Vector3:
        """
        Given an index, gets a position point of an object's position sequence

        Parameters:
            index (int):
                An index in the position point array

        Returns:
            Bopimo_Vector3:
                The position point at the given position. Position is relative
                to the origin of the object.
        """
        return self._position_points.get_vector(index)

    def set_position_point(
        self, index: int, position: Bopimo_Vector3, time: float = 0.0
    ):
        """
        Sets a position point in the object's position points, along with an
        associated travel time, at the given index. If a position travel speed
        has been given to the object, the travel time will be ignored.

        Parameters:
            index (int):
                An index in the position point array
            position (Bopimo_Vector3):
                A position relative to the object's origin, to be added to the
                sequence of position points.
            time (float):
                A travel time (in seconds) that will be paired with the
                position, to get from the given position to either the next
                position, or the start position if it is the last in the
                sequence. This parameter is optional. so if you're using
                speed-based kinematics you can omit this parameter.
        """
        self._position_points.set_vector(index, position)
        if self.position_travel_speed == 0:
            self._position_travel_times.set_float(index, time)
        else:
            if len(self._position_points) < 2:
                self._position_travel_times.set_float(index, 0)
            prev_pos: Bopimo_Vector3 = self._position_points.get_vector(index - 1)
            distance: float = (position - prev_pos).magnitude
            self._position_travel_times.set_float(
                index, distance / self.position_travel_speed
            )
            if index < len(self._position_points) - 1:
                next_pos: Bopimo_Vector3 = self._position_points.get_vector(index + 1)
                distance: float = (next_pos - position).magnitude
                self._position_travel_times.set_float(
                    index + 1, distance / self.position_travel_speed
                )

    def remove_position_point(
        self, index: int
    ) -> Bopimo_Vector3 | tuple[Bopimo_Vector3, float]:
        """
        Given an index, removes the position point and associated travel time
        of an object's position points.

        Parameters:
            index (int):
                An index in the position point array

        Returns:
            tuple[Bopimo_Vector3, float]:
                The position and travel time in a tuple pair. Position is
                relative to the origin of the object. If using speed-based
                kinematics, time is calculated based on speed and distance.
        """
        if self.position_travel_speed == 0:
            return (
                self._position_points.remove_vector(index),
                self._position_travel_times.remove_float(index),
            )
        else:
            return self._position_points.remove_vector(index)

    def clear_position_points(self):
        """
        Removes all of the position points and associated travel times of the
        object.
        """
        self._position_points.clear()
        self._position_travel_times.clear()

    def copy(self, deep_copy: bool = True, **kwargs: Any) -> Self:
        """
        Makes a copy of the Bopimo object, retaining the instance attributes.
        This method allows level makers to copy objects without the need to
        import the copy module.

        Parameters:
            deep_copy (bool):
                Takes mutable attributes and deep copies them. This is enabled
                by default as it is much more intuitive to level makers to
                deep copy. However, if you want a true shallow copy, set this
                to False.
            **kwargs (Any):
                Any available object attributes can be specified to quickhand
                modifications to a copy.

        Returns:
            Self:
                A copied object, with the exact same attributes as the original
        """
        return self.__copy__(deep_copy, **kwargs)

    def json(self) -> dict[str, Any]:
        """
        Converts the object to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the Bopimo Object
        """
        return {
            "block_id": self.id,
            "block_name": self.name,
            "nametag": self.nametag,
            "block_color": self.color.json(),
            "block_position": self.position.json(),
            "block_rotation": self.rotation.json(),
            "block_scale": self.scale.json(),
            "position_enabled": self.position_enabled,
            "position_points": self._position_points.json(),
            "position_travel_times": self._position_travel_times.json(),
            "rotation_enabled": self.rotation_enabled,
            "rotation_pivot_offset": self.rotation_pivot_offset.json(),
            "rotation_direction": self.rotation_direction.json(),
            "rotation_speed": self.rotation_speed,
        }

    # Only keyword arguments are supported, because you should be using keyword arguments anyway when quickhanding Bopymo objects
    def __copy__(self, deep_copy: bool = True, **kwargs: Any) -> Self:
        copied_object = self.__class__()
        dictionary = self.__dict__
        # While this goes against convention to make deepcopying the default behavior, I am doing this for multiple reasons:
        # 1. It is much more intuitive for the level maker for everything to be deep copied,
        #    as new programmers will have a harder time figuring out bugs related to shallow copying
        # 2. In the event that Bopimo adds a feature where Objects can have Parent-Child relationships,
        #    __deepcopy__ should be reserved for that use case. __copy__ will ONLY copy the object invoked,
        #    while __deepcopy__ will also make new copies of the object's children.
        # If performance is really *that* much of a concern to you, you can set deep_copy to false
        if deep_copy:
            dictionary = deepcopy(self.__dict__)
        copied_object.__dict__.update(dictionary)

        # Overwrite copied attributes with custom provided arguments
        for attribute, value in kwargs.items():
            # Sanity checks, making debugging a lot easier
            if attribute.startswith("_"):
                raise AttributeError(
                    f'Can not quickhand "{attribute}", a private attribute. This value either can not be modified, or requires methods to change values.'
                )
            if not attribute in self.__dict__:
                raise KeyError(
                    f"{attribute} is not a valid attribute of {self.__class__}. To quickhand non-standard attributes, make sure they are declared in the object you're copying."
                )
            if not isinstance(value, copied_object.__dict__[attribute].__class__):
                raise TypeError(
                    f'Quickhanded "{attribute}" attribute has an incompatible type. Expected {copied_object.__dict__[attribute].__class__}, got {value.__class__}'
                )
            copied_object.__dict__[attribute] = value

        return copied_object


class Bopimo_Tilable_Object(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>
    Inherited from Bopimo_Object, this is also meant to be a superclass that
    encompasses nearly all Bopimo Objects. What makes this class different is
    the addition of pattern related attributes that many Bopimo objects have.
    If the Bopimo object has a tilable pattern or contains pattern attributes,
    the object will inherit from this class instead of Bopimo_Object.

    Instance Attributes:
        pattern (Block_Pattern | int):
            The tilable pattern that the object uses.
        pattern_color (Bopimo_Color):
            The color of the tilable pattern
    """

    def __init__(
        self,
        id: Block_ID | int = Block_ID.CUBE,
        name: str = "Tilable Object",
        color: Bopimo_Color = Bopimo_Color(0, 0, 0),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(id, name, color, position, rotation, scale)
        self.pattern: Block_Pattern | int = Block_Pattern.CHECKERBOARD
        self.pattern_color: Bopimo_Color = Bopimo_Color(0, 0, 0)

    def json(self) -> dict[str, Any]:
        """
        Converts the object to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the Bopimo Object
        """
        obj = super().json()
        return obj | {
            "block_pattern": self.pattern,
            "block_pattern_color": self.pattern_color.json(),
        }


class Bopimo_Level:
    """
    This class represents the entire Bopimo level, and the highest order of
    information. All your level information is encapsulated in this class. In
    addition, this class has additional responsibilities, including handling
    block UIDs, performing higher level sanity checks, and performing the I/O
    of the module.

    Class Attributes:
        SERVER_BLOCK_LIMIT (int):
            A constant integer representing the block limit imposed by Bopimo's
            servers. While you are allowed to generate levels that pass this
            limit, you will not be able to import it in an online session and
            publish the level. In addition, some functionality may not work as
            intended past this limit.

            A warning will be thrown in the console if you export a level past
            this limit.

    Instance Attributes:
        game_version (Game_Version):
            The Bopimo version that the level will report when importing into
            Bopimo. By default, this will try to keep up-to-date with the
            latest version, but if you have a bunch of code that relies on
            older Bopimo features, set this attribute to the desired version.
        time_of_save (datetime.datetime):
            The time that this file was created. The time is determined upon
            generation of the file and written there.
        name (str):
            The name of the level
        description (str):
            The description describing the level
        music (Bopimo_Int32Array):
            An array of different integers representing various Bopimo tracks.
            It is highly recommended that you use the Music enum for choosing
            tracks, as this is more readable and future-proof.
        lives (int):
            The amount of lives that a player will have when starting an
            attempt. Each time a player dies, they will lose a life. If a
            player runs out of lives, they fail their attempt and the level
            completely restarts. Set this to 0 for infinite lives.
        player_damage_players (bool):
            If true, PvP is enabled and players can damage each other, directly
            or indirectly. By default, this is set to true.
        sky (int | Sky):
            The skybox that the level will use. It is highly recommended to use
            the Sky enum for choosing a skybox, as this is more readable and
            future-proof.
        sky_energy (float):
            A positive value that represents the level's gamma/brightness. A
            higher energy will lead to a brighter level
        ambient_color (Bopimo_Color):
            A color that represents the final color of a level's shadows. Be
            wary that the ambient color takes slight influence from a level's
            sky.
        weather (int | Weather):
            The weather that the level uses, represented by client-side
            particles. Set to clear to have no particles. It is highly
            recommended to use the Weather enum for choosing weather, as this
            is more readable and future-proof.
        fog_enabled (bool):
            If enabled, will set the level in a fog, limiting the player's
            vision
        fog_distance (int):
            Set how far the fog will end. A smaller value resembles a closer
            fog.
        fog_color (Bopimo_Color):
            Set the color of the fog. Ideally, you'd want to match the fog to
            compliment your skybox.
        gravity (float):
            <INTERNAL>
            Set's the gravity of the level.
        death_plane (float):
            A (usually negative) value that, if a player's Y position falls
            below, will instantly kill them (unless a builder has enabled
            Invincibility).
        blocks (dict[int, Bopimo_Object])
            <PRIVATE>
            A dictionary that contains all of a level's objects. The keys are
            the UIDs of an object, a unique randomly-generated integer that
            allows to identify an object. UIDs are not meant to be set by the
            level maker.
        star_amount (int)
            <READ_ONLY>
            An attribute detailing how many completion stars are in the level.
        completion_stars (List[int])
            <PRIVATE>
            A list that contains UID references to all of the level's
            completion stars. The order that the stars are in are associated
            with their "star ID" in a level.
    """

    SERVER_BLOCK_LIMIT = 2048

    def __init__(
        self,
        name: str = "My Bopimo Level",
        description: str = "Autogenerated with Python!",
    ):
        # METADATA
        self.game_version: Game_Version = GAME_VERSION
        self.time_of_save: datetime.datetime = datetime.datetime.now(datetime.UTC)

        assert self.game_version >= Game_Version(
            1, 0, 14
        ), "Bopymo 0.2 requires a minimum Bopjson version of 1.0.14 to work correctly."

        # LEVEL INFORMATION
        self.name: str = name
        self.description: str = description
        self.music: Bopimo_Int32Array = Bopimo_Int32Array(
            [Music.SERENE, Music.SWAYING_DREAMS, Music.PLAYFUL_WALTZ]
        )
        self.lives: int = 0
        self.players_damage_players: bool = True

        # ATMOSPHERE
        self.sky: Sky | int = Sky.DAY
        self.sky_energy: float = 1
        self.ambient_color: Bopimo_Color = Bopimo_Color(0, 0, 0)
        self.weather: Weather | int = Weather.CLEAR
        self.fog_enabled: bool = False
        self.fog_distance: int = 0
        self.fog_color: Bopimo_Color = Bopimo_Color(128, 128, 128)
        self.gravity: float = 105

        # MAP INFORMATION
        self.death_plane: float = -1000
        self._blocks: dict[int, Bopimo_Object] = {}

        # COMPLETION STAR MANAGEMENT
        self._completion_stars: List[int] = []

    @property
    def star_amount(self) -> int:
        """
        Retrieves the total number of stars in a level
        """
        return len(self._completion_stars)

    def __block_sanity_check(self, block: Bopimo_Object):
        """
        <PRIVATE>
        This method is meant to encompass all of the additional sanity checks
        that can not easily be performed within the object itself. This ensures
        there are no logical errors in the final export.

        Parameters:
            block (Bopimo_Object):
                The object to perform sanity checks on.
        """
        assert (
            self.game_version >= block.MIN_VERSION
        ), f'You are attempting to add a {block.__class__} instance, which requires a minimum Bopimo version of {block.MIN_VERSION}. Change your level\'s "game_version" (currently {self.game_version}) to match the version, or update Bopymo for the latest changes.'
        # Portal destinations sanity check
        if isinstance(block, Bopimo_Portal):
            for dest in block.destinations:
                if dest not in self._blocks:
                    raise KeyError(
                        f'A destination in Portal "{block.name}" has a destination ({dest}) that does not exist in the level. Did you forget to call add_object?'
                    )
                if not isinstance(self._blocks[dest], Bopimo_Portal):
                    raise TypeError(
                        f'A destination in Portal "{block.name}" has a destination (Name: {self._blocks[dest].name}, UID: {dest}) that is NOT a Portal object (Got {self._blocks[dest].__class__})'
                    )

    def remove_object(self, uid: int) -> Bopimo_Object:
        """
        Removes an object with the associated UID from the level

        Parameters:
            uid (int):
                The UID of the object to delete

        Returns:
            Bopimo_Object:
                The object found with the given UID, and removed from the level
        """
        if uid not in self._blocks:
            raise KeyError(f"Bopimo Level does not contain an object with uid {uid}")
        if isinstance(self._blocks[uid], Bopimo_Completion_Star):
            self._completion_stars.remove(uid)
        return self._blocks.pop(uid)

    def get_object(self, uid: int) -> Bopimo_Object | None:
        """
        Gets an object with the associated UID from the level, if it exists.

        Parameters:
            uid (int):
                The UID to search for an object

        Returns:
            Bopimo_Object:
                The object found with the given UID
            None:
                If no object was found
        """
        if uid not in self._blocks:
            return None
        return self._blocks[uid]

    def add_object(self, obj: Bopimo_Object) -> int:
        """
        Adds an object to the level.

        Parameters:
            obj (Bopimo_Object):
                The object that will be added to the level

        Returns:
            int:
                The newly generated UID associated with the object
        """
        uid: int = random.randrange(1, 2**32)
        # If we encounter collisions, regenerate the uid
        while uid in self._blocks:
            uid = random.randrange(1, 2**32)
        self.__block_sanity_check(obj)
        self._blocks[uid] = obj
        if isinstance(obj, Bopimo_Completion_Star):
            self._completion_stars.append(uid)
        return uid

    def add_objects(self, obj_list: List[Bopimo_Object]) -> List[int]:
        """
        Adds multiple objects to the level.

        Parameters:
            obj_list (List[Bopimo_Object]):
                A list of objects that will be added to the level

        Returns:
            List[int]:
                A list of newly generated UIDs, ordered by the objects in the
                input list
        """
        uid_list: List[int] = []
        for obj in obj_list:
            uid = self.add_object(obj)
            uid_list.append(uid)
        return uid_list

    def json(self) -> dict[str, Any]:
        """
        Converts the level to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the level
        """
        obj: dict[str, Any] = {
            "GAME_VERSION": str(self.game_version),
            "TIME_OF_SAVE": self.time_of_save.strftime("%Y-%m-%d %H:%M:%S"),
            "level_name": self.name,
            "level_description": self.description,
            "level_music": self.music.json(),
            "level_lives": self.lives,
            "level_players_damage_players": self.players_damage_players,
            "level_sky": self.sky,
            "level_sky_energy": self.sky_energy,
            "level_ambient_color": self.ambient_color.json(),
            "level_weather": self.weather,
            "level_fog_enabled": self.fog_enabled,
            "level_fog_distance": self.fog_distance,
            "level_fog_color": self.fog_color.json(),
            "level_gravity": self.gravity,
            "level_death_plane": self.death_plane,
            "level_blocks": {"type": "Container_Array", "value": []},
        }
        # Append all the blocks in JSON
        uid: int
        block: Bopimo_Object
        for uid, block in self._blocks.items():
            self.__block_sanity_check(block)
            match block:
                # Completion Stars are a special case as they have an additional ID system
                case Bopimo_Completion_Star():
                    star_id: int = self._completion_stars.index(uid)
                    obj["level_blocks"]["value"].append(
                        {"uid": uid} | block.json(star_id)
                    )
                case _:
                    obj["level_blocks"]["value"].append({"uid": uid} | block.json())

        return obj

    # TODO: Add a function that can import a bopjson file.

    def export(self, file_path: str):
        """
        Exports the Bopimo level to a bopjson file. This function will perform
        level-wide sanity checks, and also time the exporting process.

        Parameters:
            file_path (str):
                The file path, including the file name, of the bopjson file.
        """
        start = time.perf_counter()
        if len(self._blocks) > Bopimo_Level.SERVER_BLOCK_LIMIT:
            logging.warning(
                f"Your level has {len(self._blocks)} blocks, which exceeds the server block limit of {Bopimo_Level.SERVER_BLOCK_LIMIT}. "
                "You will still be able to play your level offline, but it can not be imported in an online building session and you can "
                "not publish your level online."
            )
        with open(f"{file_path}.bopjson", "w") as file:
            file.write(json.dumps(self.json()))
        end = time.perf_counter()
        export_time: int = int((end - start) * 1000)
        logging.info(
            f'"{self.name}" successfully exported to {file_path}.bopjson in {export_time} ms'
        )


## BOPIMO BLOCKS


class Bopimo_Block(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    The class that embodies all Bopimo primitives. Whether it's cubes, ramps,
    cylinders, or anything similar, you'll declare them with this class.

    This is the only class where a Block ID can be explicitly declared upon
    instantiation, meant to declare IDs for primitives.

    Instance Attributes:
        transparency_enabled (bool):
            If enabled, turns on transparency, allowing users to see partially
            or completely through the block
        transparency (int):
            The level of transparency of the block. Lower values indicate
            higher transparency, with 0 being the lowest value (full
            transparency)
        collision_enabled (bool):
            Toggles collision with other objects. If disabled, objects will
            clip through them.
    """

    def __init__(
        self,
        id: Block_ID | int = Block_ID.CUBE,
        name: str = "Generated Block",
        color: Bopimo_Color = Bopimo_Color(34, 139, 34),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(id, name, color, position, rotation, scale)
        # Block exclusive attributes
        self.transparency_enabled: bool = False
        self.transparency: int = 7
        self.collision_enabled: bool = True

    def json(self) -> dict[str, Any]:
        """
        Converts the block to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the level
        """
        obj = super().json()
        return obj | {
            "transparency": self.transparency,
            "collision_enabled": self.collision_enabled,
            "transparency_enabled": self.transparency_enabled,
        }


## ACTION BLOCKS


class Bopimo_Spawn(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A plate-shaped object that players will spawn above at the beginning of a
    new attempt, or respawn if the player has not touched a checkpoint. If a
    level has multiple spawn objects, a spawn is picked at random for a player
    to (re)spawn
    """

    def __init__(
        self,
        name: str = "Generated Spawn",
        color: Bopimo_Color = Bopimo_Color(160, 30, 176),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(4, 1, 4),
    ):
        super().__init__(Block_ID.SPAWN, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the spawn to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the spawn
        """
        return super().json()


class Bopimo_Checkpoint(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A flag-shaped object that players will respawn above if they touch it.
    Respawning at a checkpoint will not reset the attempt. If a player chooses
    to restart the level, runs out of lives, or they touch another checkpoint,
    they will no longer respawn at their previous checkpoint.
    """

    def __init__(
        self,
        name: str = "Generated Checkpoint",
        color: Bopimo_Color = Bopimo_Color(160, 30, 176),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 4, 2),
    ):
        super().__init__(Block_ID.CHECKPOINT, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the checkpoint to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the checkpoint
        """
        return super().json()


class Bopimo_Completion_Star(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    An object resembling the main objective of a game mode "Star Collection",
    where players must collect all stars to complete the level. Players obtain
    a star by touching it. In "Free Roam", stars have no functionality and are
    purely decorative.

    Completion stars are also unique because alongside a UID, they also have a
    "Star ID", a sequential ID system to uniquely identify a star in a level.
    Star IDs are managed by Bopimo_Level.

    Instance Attributes:
        mute (bool):
            By default, stars emit a sound when a player is nearby. Enabling
            this will mute that sound and make them silent.
        float_height (float):
            Stars have a movement animation that helps distinguish them from
            regular objects. Changing this value will affect how much the star
            will move with the animation.
    """

    def __init__(
        self,
        name: str = "Generated Completion Star",
        color: Bopimo_Color = Bopimo_Color(94, 0, 176),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(4, 4, 4),
    ):
        super().__init__(
            Block_ID.COMPLETION_STAR, name, color, position, rotation, scale
        )
        self.mute: bool = False
        self.float_height: float = 1.5

    def json(self, star_id: int = 0) -> dict[str, Any]:
        """
        Convert the star to JSON, as part of the exporting process.

        Parameters:
            star_id (int):
                An internal ID that uniquely identifies the completion star
                to the level

        Returns:
            dict[str, Any]:
                A JSON object of the star
        """
        obj = super().json()
        return obj | {
            "mute": self.mute,
            "star_id": star_id,
            "float_height": self.float_height,
        }


class Bopimo_Spring(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    An object that propels players in the upwards direction of the spring upon
    contact. If a player is holding the jump key, they will get a slight boost
    from the spring. If a player is performing a long jump, a spring will
    greatly assist them in covering long distances.

    Instance Attributes:
        bounce_force (float):
            Affects how much the spring will propel the player. A higher value
            will propel the player farther.
        can_ground_pound (bool):
            Determines whether a player's ground pound will cancel the effects
            of a spring. If set to false, the player will bounce while ground
            pounding.
    """

    def __init__(
        self,
        name: str = "Generated Spring",
        color: Bopimo_Color = Bopimo_Color(227, 181, 4),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(Block_ID.SPRING, name, color, position, rotation, scale)
        # Spring exclusive attributes
        self.bounce_force: float = 50
        self.can_ground_pound: bool = True

    def json(self) -> dict[str, Any]:
        """
        Convert the spring to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the spring
        """
        obj = super().json()
        return obj | {
            "bounce_force": self.bounce_force,
            "can_ground_pound": self.can_ground_pound,
        }


class Bopimo_Lava(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    One of the primary avoidances of a player. Upon touching lava, players will
    take damage and will repeatedly take damage until either the player ceases
    contact, or the player dies.

    While it is inherited from Bopimo_Object, Lava does have a pattern_color
    attribute which is only seen in a Tilable_Object. However, lava has a
    custom block pattern that can not be replicated or modified.

    Instance Attributes:
        pattern_color (Bopimo_Color):
            The color of the lava pattern
        damage_amount (float):
            The amount of damage that will be dealt to a player upon contact.
            Setting this value to 100 or more will make the lava immediately
            kill the player upon contact.
    """

    def __init__(
        self,
        name: str = "Generated Lava",
        color: Bopimo_Color = Bopimo_Color(183, 14, 0),
        pattern_color: Bopimo_Color = Bopimo_Color(255, 162, 73),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
        damage: float = 25,
    ):
        super().__init__(Block_ID.LAVA, name, color, position, rotation, scale)
        self.pattern_color: Bopimo_Color = pattern_color
        self._damage_amount: float = damage
        self.__clamp()

    @property
    def damage_amount(self) -> float:
        return self._damage_amount

    @damage_amount.setter
    def damage_amount(self, value: float):
        self._damage_amount = value
        self.__clamp()

    def __clamp(self):
        """
        <PRIVATE>
        A clamping function that serves as an internal sanity check, stopping
        attributes from having out of range values
        """
        self._damage_amount = max(0, self.damage_amount)

    def json(self) -> dict[str, Any]:
        """
        Convert the lava to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the lava
        """
        obj = super().json()
        return obj | {
            "block_pattern_color": self.pattern_color.json(),
            "damage_amount": self.damage_amount,
        }


class Bopimo_Water(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A fluid whose primary purpose is to let the player swim inside. While
    swimming, movement is heavily dampened, and certain movements are
    restricted (e.g. jumping, crouching, ground pounding).

    Players can choose to dive in the water, which gives them a small speed
    boost which lets them swim faster. Players cannot drown in water and take
    damage.

    Similar to Lava, water has a custom block pattern which can not be
    replicated or modified. The block_pattern attribute will be ignored.

    Instance Attributes:
        foam_color (Bopimo_Color):
            <ALIAS pattern_color>
            The color of the foam pattern in the water.
    """

    def __init__(
        self,
        name: str = "Generated Water",
        color: Bopimo_Color = Bopimo_Color(71, 130, 255),
        foam_color: Bopimo_Color = Bopimo_Color(255, 255, 255),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(4, 4, 4),
    ):
        super().__init__(Block_ID.WATER, name, color, position, rotation, scale)
        self.pattern_color = foam_color

    def json(self) -> dict[str, Any]:
        """
        Convert the water to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the water
        """
        return super().json()


class Bopimo_Ladder(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A specialized mesh object where players can climb upwards upon touching the
    ladder and moving, or downwards by not moving. Useful for getting up tall
    surfaces.

    Instance Attributes:
        climbing_speed (float):
            <INTERNAL> <NON-FUNCTIONAL>
            A speed multiplier of how fast the player climbs up the ladder
            compared to their walking speed.
    """

    def __init__(
        self,
        name: str = "Generated Ladder",
        color: Bopimo_Color = Bopimo_Color(78, 52, 46),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 1),
    ):
        super().__init__(Block_ID.LADDER, name, color, position, rotation, scale)
        self.climbing_speed: float = 1

    def json(self) -> dict[str, Any]:
        """
        Convert the ladder to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the ladder
        """
        obj = super().json()
        return obj | {"climbing_speed": self.climbing_speed}


class Bopimo_Token(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A coin-shaped object that players can collect. On the bottom left screen, a
    token counter is present that shows how many tokens a player has collected
    in their current attempt.

    The primary function of a token is that collecting them will heal the
    player any lost health. Tokens can also be used by level makers to help
    guide players around a level (e.g. through a line of coins).

    Instance Attributes:
        heal_amount (float):
            How much HP to heal the player upon collection
        regeneration_time (float):
            How much time (in seconds) it takes for the token to respawn after
            being collected.
        worth (int):
            How many tokens are granted to the player when collected.
        model (int):
            <INTERNAL> <NON-FUNCTIONAL>
            The mesh ID that the token's appearance will mimic
    """

    def __init__(
        self,
        name: str = "Generated Token",
        color: Bopimo_Color = Bopimo_Color(236, 126, 0),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(Block_ID.TOKEN, name, color, position, rotation, scale)
        self.heal_amount: float = 5
        self.regeneration_time: float = 45
        self.worth: int = 1
        self.model: int = 0

    def json(self) -> dict[str, Any]:
        """
        Convert the token to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the token
        """
        obj = super().json()
        return obj | {
            "heal_amount": self.heal_amount,
            "regeneration_time": self.regeneration_time,
            "worth": self.worth,  # I have none
            "model": self.model,
        }


class Bopimo_Disappearing_Block(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A special type of block where after prolonged contact, will "fall" and
    disable collision, making anything fall through it. Disappearing blocks are
    usually indicated by the shaky animation they play while they are being
    touched.

    Instance Attributes:
        disappears_after (float):
            A duration (in seconds) of how long they can be touched before they
            disappear.
        regeneration_time (float):
            A duration (in seconds) of how long it takes for the block to
            reappear after disappearing.
        players_only (bool):
            Determines whether only players will trigger the block and make it
            disappear. If false, NPCs can also trigger the block.
    """

    def __init__(
        self,
        name: str = "Generated Disappearing Block",
        color: Bopimo_Color = Bopimo_Color(122, 9, 0),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(
            Block_ID.DISAPPEARING_BLOCK, name, color, position, rotation, scale
        )
        self.pattern = Block_Pattern.X
        self.disappears_after: float = 2
        self.regeneration_time: float = 5
        self.players_only: bool = False

    def json(self) -> dict[str, Any]:
        """
        Convert the disappearing block to JSON, as part of the exporting
        process

        Returns:
            dict[str, Any]:
                A JSON object of the disappearing block
        """
        obj = super().json()
        return obj | {
            "disappears_after": self.disappears_after,
            # LOL at the inconsistent naming
            "regen_time": self.regeneration_time,
            "players_only": self.players_only,
        }


class Bopimo_Grates(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A see-through block that is meant to resemble a set of grates. Grates
    can be grabbed from underneath by players; they can hang and move while
    gripped.

    Grates use their own block pattern which cannot be replicated or modified,
    making them not tilable.
    """

    def __init__(
        self,
        name: str = "Generated Grates",
        color: Bopimo_Color = Bopimo_Color(0, 10, 18),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(4, 1, 4),
    ):
        super().__init__(Block_ID.GRATES, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the grates to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the grates
        """
        return super().json()


class Bopimo_Speed_Panel(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A panel that players can step on to temporarily alter their speed (usually
    making them move faster).

    Instance Attributes:
        new_speed (float):
            The new speed that is granted to the player upon collision.
        duration (float):
            How long (in seconds) the granted speed will last before reverting
            back to normal. This can be set to a high value for an indefinite
            speed change.
    """

    def __init__(
        self,
        name: str = "Generated Speed Panel",
        color: Bopimo_Color = Bopimo_Color(27, 0, 32),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(3, 1, 3),
        speed: float = 30,
        duration: float = 10,
    ):
        super().__init__(Block_ID.SPEED_PANEL, name, color, position, rotation, scale)
        self.new_speed: float = speed
        self.duration: float = duration

    def json(self) -> dict[str, Any]:
        """
        Convert the speed panel to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the speed panel
        """
        obj = super().json()
        return obj | {"new_speed": self.new_speed, "duration": self.duration}


class Bopimo_Boost_Panel(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A panel that players can step on, and similar to a spring, will propel the
    user forward and upwards. Jumping does NOT grant an additional boost on a
    boost panel.

    Boost panels are often used in the context of rolling, where you can
    jumpstart a roll and design obstacles based on rolling.

    Instance Attributes:
        boost (float):
            How much the player should be boosted forward
        vertical_boost (float):
            How much the player should be boosted upward
    """

    def __init__(
        self,
        name: str = "Generated Boost Panel",
        color: Bopimo_Color = Bopimo_Color(0, 2, 34),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(3, 1, 3),
    ):
        super().__init__(Block_ID.BOOST_PANEL, name, color, position, rotation, scale)
        self.boost: float = 75
        self.vertical_boost: float = 15

    def json(self) -> dict[str, Any]:
        """
        Convert the boost panel to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the boost panel
        """
        obj = super().json()
        return obj | {"boost": self.boost, "vertical_boost": self.vertical_boost}


class Bopimo_Ice(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A reflective, slightly transparent surface notable for its slipperiness,
    which can often make movement more difficult for players. Most slipperiness
    can be counteracted by jumping, so use wisely.

    Instance Attributes:
        slipperiness (float):
            A positive number that indicates how slippery the ice is upon
            contact. 0 will cancel out the slipperiness completely, while a
            high value will further reduce friction and dampen movement.
    """

    def __init__(
        self,
        name: str = "Generated Ice",
        color: Bopimo_Color = Bopimo_Color(138, 220, 223),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(Block_ID.ICE, name, color, position, rotation, scale)
        self.slipperiness: float = 1

    def json(self) -> dict[str, Any]:
        """
        Convert the ice to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the ice
        """
        obj = super().json()
        return obj | {"slipperiness": self.slipperiness}


class Bopimo_Breakable_Block(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A special block where the block is destructable. The block is typically
    destroyed by having players deal damage to it through punching, diving,
    or ground pounding. The block tends to be used to separate sections of
    a level or can be hidden in plain sight.

    Instance Attributes:
        max_health (float):
            The health of the block. The higher the health, the more hits and
            damage players will have to deal to break the block.
        regeneration_time (float):
            A duration (in seconds) for how the block will take after it has
            been destroyed before it regenerates.
    """

    def __init__(
        self,
        name: str = "Generated Breakable Block",
        color: Bopimo_Color = Bopimo_Color(129, 0, 40),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(
            Block_ID.BREAKABLE_BLOCK, name, color, position, rotation, scale
        )
        self.pattern = Block_Pattern.BRICKS
        self.max_health: float = 40
        self.regeneration_time: float = 10

    def json(self) -> dict[str, Any]:
        """
        Convert the breakable block to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the breakable block
        """
        obj = super().json()
        return obj | {
            "max_health": self.max_health,
            "regeneration_time": self.regeneration_time,
        }


class Bopimo_Cannon(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    An object where players can enter, and be launched in the air. Cannons are
    typically used by level makers to help back track, make one-way routes,
    or send players to a specific point. Trajectories are created by a cannon's
    rotation and power.

    Cannons are especially useful because while being launched, players can not
    move in the air and most movements are restricted to stop players from
    diverging from the cannon's trajectory. The only way for a player to cancel
    a cannon's effects is by ground pounding.

    Instance attributes:
        power (float):
            How much distance a cannon can launch a player. A higher value will
            shoot the player much faster, covering larger distances.
    """

    def __init__(
        self,
        name: str = "Generated Cannon",
        color: Bopimo_Color = Bopimo_Color(42, 2, 47),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
        power: float = 50,
    ):
        super().__init__(Block_ID.CANNON, name, color, position, rotation, scale)
        self.power: float = power

    def json(self) -> dict[str, Any]:
        """
        Convert the cannon to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the cannon
        """
        obj = super().json()
        return obj | {"power": self.power}


class Bopimo_Portal(Bopimo_Object):
    """
    <INHERITED Bopimo_Object> <UPCOMING>

    An object where players can enter and be instantaneously teleported from
    one place to another. Portals often fulfill many of the previous roles of a
    cannon more efficiently and effectively.

    Portals can be one-way or two-way; portals can also have multiple
    destinations. If a portal has multiple destinations, a random one is chosen
    whenever a player enters a portal.

    Portals are the only object without a visible mesh; they rely on particles
    for their visibility.

    Instance Attributes:
        transparency (int):
            <NON-FUNCTIONAL>
            The underlying transparency of the portal object. This attribute
            may be scrapped.
        destinations (Bopimo_Int64Array):
            <INTERNAL>
            A list of destinations the player may teleport to upon entering.
            Destinations are linked through a portal's corresponding UID, which
            can be obtained through Bopimo_Level.add_object.
    """

    def __init__(
        self,
        name: str = "Generated Portal",
        color: Bopimo_Color = Bopimo_Color(0, 105, 182),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(10, 10, 2),
    ):
        super().__init__(Block_ID.PORTAL, name, color, position, rotation, scale)
        self.transparency: int = 224
        self.destinations: Bopimo_Int64Array = Bopimo_Int64Array([])

    def json(self) -> dict[str, Any]:
        """
        Convert the portal to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the portal
        """
        obj = super().json()
        return obj | {
            "transparency": self.transparency,
            "destinations": self.destinations.json(),
        }


class Bopimo_Web(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    An object that inhibits player movement upon contact. Often used to stop
    movement or deter players from pursuing a particular direction.

    Instance Attributes:
        stickiness (float):
            How much should be movement be inhibited by the web. A higher value
            will be more effective at stopping movement, but will make overall
            movement slower.
    """

    def __init__(
        self,
        name: str = "Generated Web",
        color: Bopimo_Color = Bopimo_Color(255, 255, 255),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(6, 1, 6),
    ):
        super().__init__(Block_ID.WEB, name, color, position, rotation, scale)
        self.stickiness: float = 0.5

    def json(self) -> dict[str, Any]:
        """
        Convert the web to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the web
        """
        obj = super().json()
        return obj | {"stickiness": self.stickiness}


class Bopimo_Missile_Launcher(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A weapon that shoots missiles in a given direction. Upon contact with a
    surface or player, the missile will explode and deal damage to any nearby
    players.

    The missile launcher is often used as another avoidance that can kill the
    player. However, since missiles only explode whenever the front collides,
    players can stand on missiles and use them as a method of transportation
    not involving kinematics.

    Instance Attributes:
        delay (float):
            A duration (in seconds) that the launcher waits between shooting
            missiles
        missile_size (float):
            The size of the missile compared to the launcher
        explosion_damage (float):
            The amount of damage to deal to players upon contact or being in
            the explosion's area of effect
        explosion_force (float):
            How much force the explosion pushes back the player if they are in
            the explosion's area of effect
        explosion_size (float):
            The size of the area of effect of a missile's explosion. A bigger
            size leads to a bigger area of effect.
        model (int):
            <INTERNAL> <NON-FUNCTIONAL>
            The mesh ID that the missile's appearance will mimic
    """

    def __init__(
        self,
        name: str = "Generated Missile Launcher",
        color: Bopimo_Color = Bopimo_Color(160, 30, 176),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(
            Block_ID.MISSILE_LAUNCHER, name, color, position, rotation, scale
        )
        self.delay: float = 5
        self.missile_size: float = 1
        self.missile_speed: float = 15
        self.explosion_damage: float = 50
        self.explosion_force: float = 10
        self.explosion_size: float = 5
        self.model: int = 0

    def json(self) -> dict[str, Any]:
        """
        Convert the missile launcher to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the missile launcher
        """
        obj = super().json()
        return obj | {
            "delay": self.delay,
            "missile_size": self.missile_size,
            "missile_speed": self.missile_speed,
            "explosion_damage": self.explosion_damage,
            "explosion_force": self.explosion_force,
            "explosion_size": self.explosion_size,
            "model": self.model,
        }


## DECORATION BLOCKS


class Bopimo_Flower(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A simple flower with petals, reminiscent of a daisy or dandelion.
    """

    def __init__(
        self,
        name: str = "Generated Flower",
        color: Bopimo_Color = Bopimo_Color(160, 30, 176),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(Block_ID.FLOWER, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the flower to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the flower
        """
        return super().json()


class Bopimo_Fence(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A tiling mesh object that resembles a wooden picket fence.
    """

    def __init__(
        self,
        name: str = "Generated Fence",
        color: Bopimo_Color = Bopimo_Color(121, 85, 72),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 4, 1),
    ):
        super().__init__(Block_ID.FENCE, name, color, position, rotation, scale)
        self.pattern = Block_Pattern.PLANKS

    def json(self) -> dict[str, Any]:
        """
        Convert the fence to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the fence
        """
        return super().json()


class Bopimo_Pine_Tree(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A pine tree with leaves that resemble a cone-like structure.
    """

    def __init__(
        self,
        name: str = "Generated Pine Tree",
        color: Bopimo_Color = Bopimo_Color(0, 88, 36),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(5, 10, 5),
    ):
        super().__init__(Block_ID.PINE_TREE, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the pine tree to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the pine tree
        """
        return super().json()


class Bopimo_Pine_Tree_Snow(Bopimo_Pine_Tree):
    """
    <INHERITED Bopimo_Pine_Tree>

    A snowy variant of the pine tree. Usually used in cold or winter levels.
    """

    def __init__(
        self,
        name: str = "Generated Pine Tree Snow",
        color: Bopimo_Color = Bopimo_Color(0, 88, 36),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(5, 10, 5),
    ):
        super().__init__(name, color, position, rotation, scale)
        self.id = Block_ID.PINE_TREE_SNOW

    def json(self) -> dict[str, Any]:
        """
        Convert the pine tree to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the pine tree
        """
        return super().json()


class Bopimo_Palm_Tree(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A tall palm tree. Usually best used in a desert or beach setting.
    """

    def __init__(
        self,
        name: str = "Generated Palm Tree",
        color: Bopimo_Color = Bopimo_Color(94, 214, 0),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(8, 8, 8),
    ):
        super().__init__(Block_ID.PINE_TREE, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the palm tree to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the palm tree
        """
        return super().json()


class Bopimo_Street_Lamp(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A street light that is reminiscent of a vintage, germanic lantern hung on a
    pole. This decoration emits a point light, which can be useful to light
    dark areas.

    Considering the dark mesh, it is an ideal candidate if you want to pull off
    standalone point lights in Bopimo. To do this, set the street lamp size to
    the smallest size allowed in Bopimo.

    Instance Attributes:
        light_range (float):
            How far the light should illuminate from its source.
    """

    def __init__(
        self,
        name: str = "Generated Street Lamp",
        color: Bopimo_Color = Bopimo_Color(255, 160, 30),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 10, 2),
    ):
        super().__init__(Block_ID.STREET_LAMP, name, color, position, rotation, scale)
        self.light_range: float = 25

    def json(self) -> dict[str, Any]:
        """
        Convert the street lamp to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the street lamp
        """
        obj = super().json()
        return obj | {"light_range": self.light_range}


class Bopimo_Torch(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A torch that is remiscent of a handheld torch. This decoration emits a
    point light, which can be usef to light dark areas.

    This mesh includes a customizable fire animation, which can be configured
    through its "pattern_color" attribute. The torch's file can be utilized for
    other purposes outside of a torch. It would not make a great candidate for
    a standalone point light.

    Instance Attributes:
        flame_color (float):
            <ALIAS pattern_color>
            The color of the fire burning in the torch
        light_range (float):
            How far the light should illuminate from its source.
    """

    def __init__(
        self,
        name: str = "Generated Torch",
        color: Bopimo_Color = Bopimo_Color(73, 48, 42),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(1, 2, 1),
    ):
        super().__init__(Block_ID.TORCH, name, color, position, rotation, scale)
        self.pattern_color: Bopimo_Color = Bopimo_Color(255, 68, 0)
        self.light_range: float = 25

    def json(self) -> dict[str, Any]:
        """
        Convert the torch to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the torch
        """
        obj = super().json()
        return obj | {"light_range": self.light_range}


class Bopimo_Logo(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A specialized mesh resembling the "Bopimo!" logo. By default, it is colored
    in their signature purple shades, but it can be customly colored.

    Instance Attributes:
        primary_color (Bopimo_Color):
            <ALIAS color>
            The outline color of the logo mesh.
        secondary_color (Bopimo_Color):
            The fill color of the logo's letters
        tertiary_color (Bopimo_Color):
            The fill color of the exclamation point
    """

    def __init__(
        self,
        name: str = "Generated Logo",
        primary_color: Bopimo_Color = Bopimo_Color(130, 12, 155),
        secondary_color: Bopimo_Color = Bopimo_Color(175, 85, 217),
        tertiary_color: Bopimo_Color = Bopimo_Color(141, 62, 229),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(6, 2.5, 2),
    ):
        super().__init__(Block_ID.LOGO, name, primary_color, position, rotation, scale)
        self.secondary_color: Bopimo_Color = secondary_color
        self.tertiary_color: Bopimo_Color = tertiary_color

    def json(self) -> dict[str, Any]:
        """
        Convert the logo to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the logo
        """
        obj = super().json()
        return obj | {"color2": self.secondary_color, "color3": self.tertiary_color}


class Bopimo_Logo_Icon(Bopimo_Logo):
    """
    <INHERITED Bopimo_Logo>

    A variant of the "Bopimo!" logo where it closely resembles the iconized
    version (b!). Similar to the logo mesh, it is also recolorable.
    """

    def __init__(
        self,
        name: str = "Generated Logo Icon",
        primary_color: Bopimo_Color = Bopimo_Color(130, 12, 155),
        secondary_color: Bopimo_Color = Bopimo_Color(175, 85, 217),
        tertiary_color: Bopimo_Color = Bopimo_Color(141, 62, 229),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(6, 2.5, 2),
    ):
        super().__init__(
            name,
            primary_color,
            secondary_color,
            tertiary_color,
            position,
            rotation,
            scale,
        )
        self.id = Block_ID.LOGO_ICON

    def json(self) -> dict[str, Any]:
        """
        Convert the icon to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the icon
        """
        return super().json()


class Bopimo_String_Lights(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A set of colored lights that are meant to resemble Christmas lights. This
    item was added to Bopimo 1.0.9 during the holidays, and is a tilable mesh.

    Contrary to their name, this decoration does NOT emit a point light, and
    can't be used to illuminate dark areas. Lights can cycle colors through
    "blinking"

    Instance Attributes:
        wire_color (Bopimo_Color):
            <ALIAS color>
            The color of the wire attaching all the string lights
        bulb_colors (Bopimo_ColorArray):
            An ordered sequence of the colors that the string lights will
            illuminate. The sequence is looped through when rendering
            individual bulbs, and when the lights "blink" through the sequence.
        blink_speed (float):
            The speed at which individual bulbs cycle through the bulb colors.
    """

    def __init__(
        self,
        name: str = "Generated String Lights",
        wire_color: Bopimo_Color = Bopimo_Color(0, 67, 27),
        bulb_colors: Bopimo_ColorArray = Bopimo_ColorArray(
            [
                Bopimo_Color(255, 0, 0),
                Bopimo_Color(255, 215, 0),
                Bopimo_Color(50, 205, 50),
                Bopimo_Color(0, 0, 255),
                Bopimo_Color(255, 0, 255),
            ]
        ),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(6, 2.5, 2),
    ):
        super().__init__(
            Block_ID.STRING_LIGHTS, name, wire_color, position, rotation, scale
        )
        self.bulb_colors: Bopimo_ColorArray = bulb_colors
        self.blink_speed: float = 0

    def json(self) -> dict[str, Any]:
        """
        Convert the string lights to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the string lights
        """
        obj = super().json()
        return obj | {
            "bulb_colors": self.bulb_colors.json(),
            "blink_speed": self.blink_speed,
        }


class Bopimo_Rose(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A special type of flower that resembles a rose. Roses were added in Bopimo
    1.0.15 as part of the Bopimo Valentine's Day event. Considering the thorns
    that are attached to roses, players that touch them will take 1 HP worth of
    damage upon contacting them by default.

    Roses possess a unique use case. Since roses only have a damage collider
    and players can walk through them, they can be used as a method of
    un-collidable lava. They also can be modified to heal the player instead of
    damaging them, offering an alternative method of healing.

    Instance attributes:
        bud_color (Bopimo_Color):
            <ALIAS color>
            The color of the rose petals
        stem_color (Bopimo_Color):
            <ALIAS pattern_color>
            The color of the rose's stem (and by extension thorns)
        damage (float):
            The amount of damage that can be dealt to a player upon contact.
            Set this to 0 if you don't want players taking damage from touching
            roses. Set this to a negative value if you want players to heal
            upon contact.
    """

    MIN_VERSION = Game_Version(1, 0, 15)

    def __init__(
        self,
        name: str = "Generated Rose",
        bud_color: Bopimo_Color = Bopimo_Color(255, 0, 0),
        stem_color: Bopimo_Color = Bopimo_Color(0, 153, 0),
        damage: float = 1,
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(1, 3, 1),
    ):
        super().__init__(Block_ID.ROSE, name, bud_color, position, rotation, scale)
        self.pattern_color = stem_color
        self.damage: float = damage

    def json(self) -> dict[str, Any]:
        """
        Convert the rose to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the rose
        """
        obj = super().json()
        return obj | {"damage": self.damage}


class Bopimo_Item_Mesh(Bopimo_Object):
    """
    <INHERITED Bopimo_Object>

    A customizable mesh object that level makers can use to insert items into
    their levels. The mesh ID can contain the ID based on any item in the
    Bopimo catalog, including hats, toys, faces, and even user-made clothing.

    For faces and user clothing, bopi models do not render when selecting these
    types of assets.

    Instance attributes:
        item_id (int):
            The ID the mesh will be using. Visit this link to reference assets:
            (https://www.bopimo.com/shop?category=all&order=oldest)
        shaded (bool):
            Whether the mesh is can receive shadow maps. This does NOT stop the
            mesh from casting shadows.
    """

    def __init__(
        self,
        name: str = "Generated Item Mesh",
        color: Bopimo_Color = Bopimo_Color(255, 255, 255),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(Block_ID.MESH, name, color, position, rotation, scale)
        self.item_id: int = 1
        self.shaded: bool = True

    def json(self) -> dict[str, Any]:
        """
        Convert the item mesh to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the item mesh
        """
        obj = super().json()
        return obj | {"item_id": self.item_id, "shaded": self.shaded}


class Bopimo_Cloud(Bopimo_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    An animated mesh that resembles a cloud.
    """

    def __init__(
        self,
        name: str = "Generated Cloud",
        color: Bopimo_Color = Bopimo_Color(255, 255, 255),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(8, 2, 8),
    ):
        super().__init__(Block_ID.CLOUD, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the cloud to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the cloud
        """
        return super().json()


class Bopimo_Statue(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object> <INTERNAL>

    A standstill mesh of the default Bopi character, the character which all
    players are based from.

    This decoration is likely unfinished and may be subject to additional
    changes.
    """

    def __init__(
        self,
        name: str = "Generated Analog Clock",
        color: Bopimo_Color = Bopimo_Color(246, 156, 0),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(3, 5, 2),
    ):
        super().__init__(Block_ID.STATUE, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the statue to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the statue
        """
        return super().json()


## NPC BLOCKS
class Bopimo_Bopi_Spawner(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object>

    A spawner that is bound to spawn a customizable Bopi NPC. The NPC by
    default will try to path find and attack players who come near it. However,
    the spawner can be modified as a standstill representation of custom Bopis.

    By default, NPCs will have their names visible, and will have an icon next
    to their name to indicate they are an NPC. Players can attack NPCs and deal
    damage to them, allowing players to fight back and kill attackers. Upon
    dying, NPCs will respawn above their respective spawner.

    Spawners will only permit one NPC at a time, and cannot spawn multiple
    Bopis simultaneously.

    Instance Attributes:
        max_health (float):
            The maximum health that an NPC can start out with. A higher health
            will make the NPC harder to kill
        attack_damage (float):
            How much damage the NPC will deal to players when punching them.
        move_speed (float):
            How fast the NPC can walk. A higher value leads to a faster NPC
            and can be more difficult to out maneuver.
        targeting_radius (float):
            How far a player has to be from the NPC to start chasing the player
            and dealing damage. It is specifically from the NPC, not the
            spawner!
        stun_time (float):
            When stunned as a result of being ground pounded by a player,
            how long (in seconds) the NPC will remain stunned until they
            recover.
        return_to_spawner (bool):
            If the player goes outside the targeting radius, determines whether
            the NPC will return to their spawner. If false, the NPC will stand
            still in their last chasing position.
        sleep_time (float):
            A threshold (in seconds). If the NPC has been standing still past
            this threshold, the NPC will start falling asleep. Useful to give
            players a headstart on a chase.

        head_color (Bopimo_Color):
            The skin color of the NPC's head
        torso_color (Bopimo_Color):
            The skin color of the NPC's torso
        left_arm_color (Bopimo_Color):
            The skin color of the NPC's left arm
        left_hand_color (Bopimo_Color):
            The skin color of the NPC's left hand
        right_arm_color (Bopimo_Color):
            The skin color of the NPC's right arm
        right_hand_color (Bopimo_Color):
            The skin color of the NPC's right hand
        left_leg_color (Bopimo_Color):
            The skin color of the NPC's left leg
        left_foot_color (Bopimo_Color):
            The skin color of the NPC's left foot
        right_leg_color (Bopimo_Color):
            The skin color of the NPC's right leg
        right_foot_color (Bopimo_Color):
            The skin color of the NPC's right foot
        hats (Bopimo_Int32Array):
            A list of IDs of valid hats that the NPC will wear
        face (int):
            An ID of a valid face the NPC will have
        shirt (int):
            An ID of a valid shirt the NPC will wear
        pants (int):
            An ID of valid pants the NPC will wear
        shoes (int):
            An ID of valid shoes the NPC will wear
        toy (int):
            An ID of a valid toy the NPC will be holding
    """

    def __init__(
        self,
        name: str = "Generated Bopi Spawner",
        color: Bopimo_Color = Bopimo_Color(160, 30, 176),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 0.5, 2),
    ):
        super().__init__(Block_ID.BOPI_SPAWNER, name, color, position, rotation, scale)
        self.max_health: float = 75
        self.attack_damage: float = 10
        self.move_speed: float = 15
        self.targeting_radius: float = 75
        self.stun_time: float = 3.5
        self.return_to_spawner: bool = False
        self.sleep_time: float = 60

        self.head_color: Bopimo_Color = Bopimo_Color(246, 156, 0)
        self.torso_color: Bopimo_Color = Bopimo_Color(156, 156, 156)
        self.left_arm_color: Bopimo_Color = Bopimo_Color(246, 156, 0)
        self.left_hand_color: Bopimo_Color = Bopimo_Color(246, 156, 0)
        self.right_arm_color: Bopimo_Color = Bopimo_Color(246, 156, 0)
        self.right_hand_color: Bopimo_Color = Bopimo_Color(246, 156, 0)
        self.left_leg_color: Bopimo_Color = Bopimo_Color(49, 51, 53)
        self.left_foot_color: Bopimo_Color = Bopimo_Color(17, 17, 17)
        self.right_leg_color: Bopimo_Color = Bopimo_Color(49, 51, 53)
        self.right_foot_color: Bopimo_Color = Bopimo_Color(17, 17, 17)
        self.hats: Bopimo_Int32Array = Bopimo_Int32Array()
        self.face: int = -1
        self.shirt: int = -1
        self.pants: int = -1
        self.shoes: int = -1
        self.toy: int = -1

    # TODO: Add a function that recreates the level editor feature of putting in a username to resolve the avatar

    def json(self) -> dict[str, Any]:
        """
        Convert the Bopi spawner to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the Bopi spawner
        """
        obj = super().json()
        return obj | {
            "max_health": self.max_health,
            "attack_damage": self.attack_damage,
            "move_speed": self.move_speed,
            "targeting_radius": self.targeting_radius,
            "stun_time": self.stun_time,
            "return_to_spawner": self.return_to_spawner,
            "sleep_time": self.sleep_time,
            "head_color": self.head_color.json(),
            "torso_color": self.torso_color.json(),
            "left_arm_color": self.left_arm_color.json(),
            "left_hand_color": self.left_hand_color.json(),
            "right_arm_color": self.right_arm_color.json(),
            "right_hand_color": self.right_hand_color.json(),
            "left_leg_color": self.left_leg_color.json(),
            "left_foot_color": self.left_foot_color.json(),
            "right_leg_color": self.right_leg_color.json(),
            "right_foot_color": self.right_foot_color.json(),
            "hats": self.hats.json(),
            "face": self.face,
            "shirt": self.shirt,
            "pants": self.pants,
            "shoes": self.shoes,
            "toy": self.toy,
        }


## HIDDEN BLOCKS

# WARNING: These classes incorporate blocks that are not available in the editor,
#          and typically for good reason. These are blocks that were never meant
#          to be accessed by level makers. While I will allow hidden blocks that
#          are functional and finished, Bopymo does not guarantee that these blocks
#          will remain and removal of such blocks won't be considered a breaking
#          change. Use at your own risk!


class Bopimo_Analog_Clock(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object> <INTERNAL>

    A mesh that will render the second, minute, and hour hands of a physical
    clock. The hands will animate, and try to align with the user's system
    time.
    """

    def __init__(
        self,
        name: str = "Generated Analog Clock",
        color: Bopimo_Color = Bopimo_Color(160, 29, 175),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(Block_ID.ANALOG_CLOCK, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the analog clock to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the analog clock
        """
        return super().json()


class Bopimo_Bleeding_Eye(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object> <INTERNAL>

    A 2D sprite of a bleeding hand-drawn eye, which will always orient itself
    to face the player's camera. While it is non-collidable and has no
    functionality, it will constantly emit a low humming sound whenever a
    player is near it.
    """

    def __init__(
        self,
        name: str = "Generated Bleeding Eye",
        color: Bopimo_Color = Bopimo_Color(237, 0, 8),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(Block_ID.STATUE, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the bleeding eye to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the bleeding eye
        """
        return super().json()


class Bopimo_Hyacinth(Bopimo_Tilable_Object):
    """
    <INHERITED Bopimo_Tilable_Object> <INTERNAL>

    A flower decoration that is almost identical to Bopimo_Flower. However,
    the Hyacinth has a different default color. This decoration is very likely
    a placeholder for another flower type and unfinished.
    """

    def __init__(
        self,
        name: str = "Generated Hyacinth Flower",
        color: Bopimo_Color = Bopimo_Color(20, 126, 172),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
    ):
        super().__init__(Block_ID.HYACINTH, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        """
        Convert the hyacinth to JSON, as part of the exporting process.

        Returns:
            dict[str, Any]:
                A JSON object of the hyacinth
        """
        return super().json()


## UNOFFICIAL BLOCKS

# WARNING: These classes are meant to incorporate concepts created by the
#          Bopimo community, and are not official blocks. These blocks can be
#          modified or removed at any time in the future, should the methods
#          behind them break or an official implementation succeed these
#          workarounds.


class Decal_Type(IntEnum):
    """
    Decal uploaders will often upload their textures in three popular formats.
    The two major articles of clothing, shirts and pants, both have their own
    pros and cons.

    Shirts will have a better pixel resolution and should be the case if
    resolution is important. However, be careful with the corners, as the
    corners will warp in the final decal.

    Pants have significantly less warping artifacts, but they will have a lower
    resolution. In addition, there are two variants of pants decals, depending
    on which leg the decal maker chooses to put their texture. Make sure to
    select the appropriate leg so the transformations will apply correctly.
    """

    SHIRT = 0
    PANTS_FRONT_LEFT = 1  # Left Leg
    PANTS_FRONT_RIGHT = 2  # Right Leg


# Decals are made using transparent clothing items with images on specific faces.
class Bopimo_Decal(Bopimo_Item_Mesh):
    """
    <INHERITED Bopimo_Item_Mesh> <NONSTANDARD>

    Taking advantage of bopis not rendering with their clothing items and alpha
    channels in textures, you are able to recreate custom decals in the game and
    use it to pull off custom aesthetics that you can't achieve with Bopimo's
    official objects.

    Class Attributes:
        SHIRT_WIDTH_RATIO (float):
            The calculated value that will have a texture's width equal a
            block's width.
        SHIRT_HEIGHT_RATIO (float):
            The calculated value that will have a texture's height equal a
            block's height.
        PANTS_TILT_FIX (int):
            The rotation (in degrees) that will be applied to a pants decal to
            correct rotation warping
        PANTS_X_ADJUST (float):
            The adjustment of the position of a pants decal to center its
            texture in the X axis.
        PANTS_Y_ADJUST (float):
            The adjustment of the position of a pants decal to center its
            tecture in the Y axis.
        PANTS_WIDTH_RATIO (float):
            The calculated value that will have a texture's width equal a
            block's width.
        PANTS_HEIGHT_RATIO (float):
            The calculated value that will have a texture's height equal a
            block's height.

    Instance Attributes:
        width (float):
            The width of the texture, in units
        height (float):
            The height of the texture, in units
        image_id (int):
            <ALIAS item_id>
            The ID of the decal texture
        type (Decal_Type):
            The type of clothing the texture is hosted on
        offset (Bopimo_Vector3):
            How much offset in the X and Y position to shift the texture.
            Useful if the decal maker didn't properly center their decal.
            The Z attribute will be ignored.
    """

    # Shirt aspect ratio is 16:17
    SHIRT_WIDTH_RATIO: float = 10 / 8
    SHIRT_HEIGHT_RATIO: float = 20 / 17

    PANTS_TILT_FIX: float = 2
    PANTS_X_ADJUST: float = 41 / 200
    PANTS_Y_ADJUST: float = 25 / 2000
    # Pants aspect ratio is 12:21
    PANTS_WIDTH_RATIO: float = 10 / 3
    PANTS_HEIGHT_RATIO: float = 40 / 21

    def __init__(
        self,
        name: str = "Generated Decal",
        decal_type: Decal_Type = Decal_Type.SHIRT,
        image_id: int = 3372,
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        width: float = 2,
        height: float = 2,
    ):
        super().__init__(
            name,
            Bopimo_Color(255, 255, 255),
            position,
            rotation,
            # The Z axis must ideally be 0. By changing the Z value, you defeat the purpose of a decal
            Bopimo_Vector3(width, height, 0.01),
        )
        self.item_id = image_id
        self.decal_type: Decal_Type = decal_type
        # Oftentimes, images are not properly centered. Use this to center images.
        self.offset: Bopimo_Vector3 = Bopimo_Vector3.zero()

    def calculate_size(self) -> Bopimo_Vector3:
        """
        Take the decal's texture size, and calculate the mesh's size.

        Returns:
            Bopimo_Vector3:
                The mesh size needed for the texture to match its size.
        """
        if self.scale.z > 0.1:
            logging.warning(
                "You set a Decal's Z scale to a non-zero value, which defeats the purpose of a Decal. "
                "Consider using a Bopimo_Item_Mesh instead."
            )
        match self.decal_type:
            case Decal_Type.SHIRT:
                return Bopimo_Vector3(
                    self.scale.x * self.SHIRT_WIDTH_RATIO,
                    self.scale.y * self.SHIRT_HEIGHT_RATIO,
                    self.scale.z,
                )
            case _:
                return Bopimo_Vector3(
                    self.scale.x * self.PANTS_WIDTH_RATIO,
                    self.scale.y * self.PANTS_HEIGHT_RATIO,
                    self.scale.z,
                )

    def __get_rotation_matrix(self, rotation: Bopimo_Vector3) -> List[List[float]]:
        """
        <PRIVATE>
        Given euler angles represented by a Vector3, calculate the rotation
        matrix behind the rotation.

        Parameters:
            rotation (Bopimo_Vector3):
                A Vector3 of the euler angles to calculate a rotation matrix

        Returns:
            List[List[float]]:
                A rotation matrix of the input rotation
        """
        MATRIX_X: tuple[List[float], List[float], List[float]] = (
            [1, 0, 0],
            [0, math.cos(rotation.x), -math.sin(rotation.x)],
            [0, math.sin(rotation.x), math.cos(rotation.x)],
        )
        MATRIX_Y: tuple[List[float], List[float], List[float]] = (
            [math.cos(rotation.y), 0, math.sin(rotation.y)],
            [0, 1, 0],
            [-math.sin(rotation.y), 0, math.cos(rotation.y)],
        )
        MATRIX_Z: tuple[List[float], List[float], List[float]] = (
            [math.cos(rotation.z), -math.sin(rotation.z), 0],
            [math.sin(rotation.z), math.cos(rotation.z), 0],
            [0, 0, 1],
        )

        return dot(dot(MATRIX_Y, MATRIX_X), MATRIX_Z)

    def calculate_center_vector(self, scale: Bopimo_Vector3) -> Bopimo_Vector3:
        """
        Given an input scale (usually the fixed mesh size), calculate the
        vector that will be used to translate the texture into a mesh position.

        If the decal is based on a shirt, this method returns a zero vector,
        as decals don't need their position shifted.

        Parameters:
            scale (Bopimo_Vector3):
                The input scale of the final mesh. This is needed as it needs
                the mesh scale, not the texture scale.

        Returns:
            Bopimo_Vector3:
                The translation vector needed to convert texture position into
                mesh position.
        """
        if self.decal_type == Decal_Type.SHIRT:
            return Bopimo_Vector3.zero()
        direction = 1
        if self.decal_type == Decal_Type.PANTS_FRONT_RIGHT:
            direction *= -1

        x_adjust = self.PANTS_X_ADJUST * scale.x * -direction + self.offset.x
        y_adjust = self.PANTS_Y_ADJUST * scale.y + self.offset.y
        rot_matrix = self.__get_rotation_matrix(self.rotation.to_radians())
        offset: List[float] = [x_adjust, y_adjust, 0]
        x, y, z = dot(rot_matrix, offset)
        return Bopimo_Vector3(x, y, z)

    def json(self) -> dict[str, Any]:
        """
        Convert the decal to JSON, as part of the exporting process. This
        process involves taking the texture transformations and converting them
        to mesh transformations, so they can be perfectly displayed in-game.

        Returns:
            dict[str, Any]:
                A JSON object of the decal
        """
        obj = super().json()
        fixed_scale = self.calculate_size()
        obj["block_scale"] = fixed_scale.json()
        translation = self.calculate_center_vector(fixed_scale)
        if self.rotation_enabled:
            # The pivot gets the translation instead of the position
            fixed_pivot = self.rotation_pivot_offset + translation
            obj["rotation_pivot_offset"] = fixed_pivot.json()
        else:
            fixed_position = self.position + translation
            obj["block_position"] = fixed_position.json()
        if self.decal_type != Decal_Type.SHIRT:
            tilt_fix = (
                self.PANTS_TILT_FIX
                if self.decal_type == Decal_Type.PANTS_FRONT_RIGHT
                else -self.PANTS_TILT_FIX
            )
            fixed_rotation = self.rotation + Bopimo_Vector3(0, 0, tilt_fix)
            obj["block_rotation"] = fixed_rotation.json()

        return obj
