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
DEPRECATION_WARNINGS: dict[str, bool] = {
    "Getting position_points directly": False,
    "Setting position_points directly": False,
}


class Game_Version:
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


GAME_VERSION = Game_Version(1, 0, 15)

### ENUMS


class Block_ID(IntEnum):
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
    CLEAR = 0
    SNOW = 1
    RAIN = 2
    VOID = 3
    AUTUMN = 4


class Music(IntEnum):
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
        if self._position_travel_speed is None:
            return 0
        return self._position_travel_speed

    @property
    def position_points(self) -> Bopimo_Vector3Array:
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
        self._position_travel_speed = value
        if value != 0:
            self.__refresh_constant_travel_speed_times()

    @position_points.setter
    def position_points(self, points: Bopimo_Vector3Array):
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
        return self._position_points.get_vector(index)

    def set_position_point(
        self, index: int, position: Bopimo_Vector3, time: float = 0.0
    ):
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
        if self.position_travel_speed == 0:
            return (
                self._position_points.remove_vector(index),
                self._position_travel_times.remove_float(index),
            )
        else:
            return self._position_points.remove_vector(index)

    def copy(self, deep_copy: bool = True, **kwargs: Any) -> Self:
        return self.__copy__(deep_copy, **kwargs)

    def json(self) -> dict[str, Any]:
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
        obj = super().json()
        return obj | {
            "block_pattern": self.pattern,
            "block_pattern_color": self.pattern_color.json(),
        }


class Bopimo_Level:
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
        # 0 means infinite lives
        self.lives: int = 0
        self.players_damage_players: bool = True

        # ATMOSPHERE
        self.sky: Sky | int = Sky.DAY
        self.sky_energy: float = 1  # Another way of saying "Level brightness"
        self.ambient_color: Bopimo_Color = Bopimo_Color(0, 0, 0)
        self.weather: Weather | int = Weather.CLEAR
        self.fog_enabled: bool = False
        self.fog_distance: int = 0
        self.fog_color: Bopimo_Color = Bopimo_Color(128, 128, 128)
        self.gravity: float = 105

        # MAP INFORMATION
        self.death_plane: float = -1000
        self._blocks: dict[int, Bopimo_Object] = {}

    def __block_sanity_check(self, block: Bopimo_Object):
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
        if uid not in self._blocks:
            raise KeyError(f"Bopimo Level does not contain an object with uid {uid}")
        return self._blocks.pop(uid)

    def get_object(self, uid: int) -> Bopimo_Object | None:
        if uid not in self._blocks:
            return None
        return self._blocks[uid]

    def add_object(self, obj: Bopimo_Object) -> int:
        uid: int = random.randrange(1, 2**32)
        # If we encounter collisions, regenerate the uid
        while uid in self._blocks:
            uid = random.randrange(1, 2**32)
        self.__block_sanity_check(obj)
        self._blocks[uid] = obj
        # Return the UID in case the user wants a direct reference to the object in the level
        return uid

    def add_objects(self, obj_list: List[Bopimo_Object]) -> List[int]:
        uid_list: List[int] = []
        for obj in obj_list:
            uid = self.add_object(obj)
            uid_list.append(uid)
        return uid_list

    def json(self) -> dict[str, Any]:
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
            obj["level_blocks"]["value"].append({"uid": uid} | block.json())

        return obj

    # TODO: Add a function that can import a bopjson file.

    def export(self, file_path: str):
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
        obj = super().json()
        return obj | {
            "transparency": self.transparency,
            "collision_enabled": self.collision_enabled,
            "transparency_enabled": self.transparency_enabled,
        }


## ACTION BLOCKS


class Bopimo_Spawn(Bopimo_Tilable_Object):
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
        return super().json()


class Bopimo_Checkpoint(Bopimo_Tilable_Object):
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
        return super().json()


class Bopimo_Completion_Star(Bopimo_Tilable_Object):
    _star_counter: int = 0

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
        # Star ID should NOT be changed! The id is tied to how many there are
        self._star_id: int = self._star_counter
        self._star_counter += 1

    @classmethod
    def get_star_count(cls) -> int:
        return cls._star_counter

    def json(self) -> dict[str, Any]:
        obj = super().json()
        return obj | {
            "mute": self.mute,
            "star_id": self._star_id,
            "float_height": self.float_height,
        }


class Bopimo_Spring(Bopimo_Object):
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
        obj = super().json()
        return obj | {
            "bounce_force": self.bounce_force,
            "can_ground_pound": self.can_ground_pound,
        }


class Bopimo_Lava(Bopimo_Object):
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
        self.damage_amount: float = damage

    def json(self) -> dict[str, Any]:
        obj = super().json()
        return obj | {
            "block_pattern_color": self.pattern_color.json(),
            "damage_amount": self.damage_amount,
        }


class Bopimo_Water(Bopimo_Tilable_Object):
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
        # NOTE: "Foam Color" is basically "Pattern Color" with a different name
        self.pattern_color = foam_color

    def json(self) -> dict[str, Any]:
        return super().json()


class Bopimo_Ladder(Bopimo_Tilable_Object):
    def __init__(
        self,
        name: str = "Generated Ladder",
        color: Bopimo_Color = Bopimo_Color(78, 52, 46),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 1),
    ):
        super().__init__(Block_ID.LADDER, name, color, position, rotation, scale)
        # This is a hidden property and can't be found in the level editor
        self.climbing_speed: float = 1

    def json(self) -> dict[str, Any]:
        obj = super().json()
        return obj | {"climbing_speed": self.climbing_speed}


class Bopimo_Token(Bopimo_Object):
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
        # This is a hidden property and can't be found in the level editor
        self.model: int = 0

    def json(self) -> dict[str, Any]:
        obj = super().json()
        return obj | {
            "heal_amount": self.heal_amount,
            "regeneration_time": self.regeneration_time,
            "worth": self.worth,  # I have none
            "model": self.model,
        }


class Bopimo_Disappearing_Block(Bopimo_Tilable_Object):
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
        obj = super().json()
        return obj | {
            "disappears_after": self.disappears_after,
            # LOL at the inconsistent naming
            "regen_time": self.regeneration_time,
            "players_only": self.players_only,
        }


class Bopimo_Grates(Bopimo_Object):
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
        return super().json()


class Bopimo_Speed_Panel(Bopimo_Object):
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
        obj = super().json()
        return obj | {"new_speed": self.new_speed, "duration": self.duration}


class Bopimo_Boost_Panel(Bopimo_Object):
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
        obj = super().json()
        return obj | {"boost": self.boost, "vertical_boost": self.vertical_boost}


class Bopimo_Ice(Bopimo_Object):
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
        obj = super().json()
        return obj | {"slipperiness": self.slipperiness}


class Bopimo_Breakable_Block(Bopimo_Tilable_Object):
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
        obj = super().json()
        return obj | {
            "max_health": self.max_health,
            "regeneration_time": self.regeneration_time,
        }


class Bopimo_Cannon(Bopimo_Object):
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
        obj = super().json()
        return obj | {"power": self.power}


# WARNING: This is a hidden block, not available in the level editor. It is functional, but has unfinished features.
#          This class is subject to change.
class Bopimo_Portal(Bopimo_Object):
    def __init__(
        self,
        name: str = "Generated Portal",
        color: Bopimo_Color = Bopimo_Color(0, 105, 182),
        position: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        rotation: Bopimo_Vector3 = Bopimo_Vector3.zero(),
        scale: Bopimo_Vector3 = Bopimo_Vector3(10, 10, 2),
    ):
        super().__init__(Block_ID.PORTAL, name, color, position, rotation, scale)
        # Currently this attribute is non-functional. I will update it when it works properly
        self.transparency: int = 224
        # Destinations work based on Object UIDs. Bopimo_Level.add_object returns an object's UID, so use that to make this work.
        self.destinations: Bopimo_Int64Array = Bopimo_Int64Array([])

    def json(self) -> dict[str, Any]:
        obj = super().json()
        return obj | {
            "transparency": self.transparency,
            "destinations": self.destinations.json(),
        }


class Bopimo_Web(Bopimo_Object):
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
        obj = super().json()
        return obj | {"stickiness": self.stickiness}


class Bopimo_Missile_Launcher(Bopimo_Object):
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
        # This is a hidden property and can't be found in the level editor
        self.model: int = 0

    def json(self) -> dict[str, Any]:
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
        return super().json()


class Bopimo_Fence(Bopimo_Tilable_Object):
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
        return super().json()


class Bopimo_Pine_Tree(Bopimo_Tilable_Object):
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
        return super().json()


class Bopimo_Pine_Tree_Snow(Bopimo_Pine_Tree):
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
        return super().json()


class Bopimo_Palm_Tree(Bopimo_Tilable_Object):
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
        return super().json()


class Bopimo_Street_Lamp(Bopimo_Object):
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
        obj = super().json()
        return obj | {"light_range": self.light_range}


class Bopimo_Torch(Bopimo_Object):
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
        obj = super().json()
        return obj | {"light_range": self.light_range}


class Bopimo_Logo(Bopimo_Object):
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
        obj = super().json()
        return obj | {"color2": self.secondary_color, "color3": self.tertiary_color}


class Bopimo_Logo_Icon(Bopimo_Logo):
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
        return super().json()


class Bopimo_String_Lights(Bopimo_Object):
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
        # NOTE: "Wire color" uses the "Block color" attribute
        super().__init__(
            Block_ID.STRING_LIGHTS, name, wire_color, position, rotation, scale
        )
        self.bulb_colors: Bopimo_ColorArray = bulb_colors
        self.blink_speed: float = 0

    def json(self) -> dict[str, Any]:
        obj = super().json()
        return obj | {
            "bulb_colors": self.bulb_colors.json(),
            "blink_speed": self.blink_speed,
        }


class Bopimo_Rose(Bopimo_Tilable_Object):
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
        # NOTE: "Bud_color" uses block color, while "stem_color" uses the pattern color.
        super().__init__(Block_ID.ROSE, name, bud_color, position, rotation, scale)
        self.pattern_color = stem_color
        self.damage: float = damage

    def json(self) -> dict[str, Any]:
        obj = super().json()
        return obj | {"damage": self.damage}


class Bopimo_Item_Mesh(Bopimo_Object):
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
        obj = super().json()
        return obj | {"item_id": self.item_id, "shaded": self.shaded}


class Bopimo_Cloud(Bopimo_Tilable_Object):
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
        return super().json()


# WARNING: This is a hidden block and is very likely unfinished. This class is subject to change.
class Bopimo_Statue(Bopimo_Tilable_Object):
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
        return super().json()


## NPC BLOCKS
class Bopimo_Bopi_Spawner(Bopimo_Tilable_Object):
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
        return super().json()


class Bopimo_Bleeding_Eye(Bopimo_Tilable_Object):
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
        return super().json()


class Bopimo_Hyacinth(Bopimo_Tilable_Object):
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
        return super().json()


## UNOFFICIAL BLOCKS

# WARNING: These classes are meant to incorporate concepts created by the
#          Bopimo community, and are not official blocks. These blocks can be
#          modified or removed at any time in the future, should the methods
#          behind them break or an official implementation succeed these
#          workarounds.


# Decals can be made using either shirts or pants, each with their tradeoffs
# Shirts: Has better resolution, but at the cost of warping if you rely on the corners
# Pants: Has less warping, but you'll have a lower resolution.
class Decal_Type(IntEnum):
    SHIRT = 0
    PANTS_FRONT_LEFT = 1  # Left Leg
    PANTS_FRONT_RIGHT = 2  # Right Leg


# Decals are made using transparent clothing items with images on specific faces.
class Bopimo_Decal(Bopimo_Item_Mesh):
    # The image will not match the actual object size. These constants will convert our size so it visually matches
    # Shirt aspect ratio is 16:17
    SHIRT_WIDTH_RATIO = 10 / 8
    SHIRT_HEIGHT_RATIO = 20 / 17

    PANTS_TILT_FIX = 2
    PANTS_X_ADJUST = 41 / 200
    PANTS_Y_ADJUST = 25 / 2000
    # Pants aspect ratio is 12:21
    PANTS_WIDTH_RATIO = 10 / 3
    PANTS_HEIGHT_RATIO = 40 / 21

    def __init__(
        self,
        name: str = "Generated Decal",
        type: Decal_Type = Decal_Type.SHIRT,
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
        self.type = type
        # Oftentimes, images are not properly centered. Use this to center images.
        self.offset = Bopimo_Vector3.zero()

    def calculate_size(self) -> Bopimo_Vector3:
        if self.scale.z > 0.1:
            logging.warning(
                "You set a Decal's Z scale to a non-zero value, which defeats the purpose of a Decal. "
                "Consider using a Bopimo_Item_Mesh instead."
            )
        match self.type:
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
        if self.type == Decal_Type.SHIRT:
            # Shirts are already centered
            return Bopimo_Vector3.zero()
        direction = 1
        if self.type == Decal_Type.PANTS_FRONT_RIGHT:
            direction *= -1

        x_adjust = self.PANTS_X_ADJUST * scale.x * -direction + self.offset.x
        y_adjust = self.PANTS_Y_ADJUST * scale.y + self.offset.y
        rot_matrix = self.__get_rotation_matrix(self.rotation.to_radians())
        offset: List[float] = [x_adjust, y_adjust, 0]
        x, y, z = dot(rot_matrix, offset)
        return Bopimo_Vector3(x, y, z)

    def json(self) -> dict[str, Any]:
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
        if self.type != Decal_Type.SHIRT:
            tilt_fix = (
                self.PANTS_TILT_FIX
                if self.type == Decal_Type.PANTS_FRONT_RIGHT
                else -self.PANTS_TILT_FIX
            )
            fixed_rotation = self.rotation + Bopimo_Vector3(0, 0, tilt_fix)
            obj["block_rotation"] = fixed_rotation.json()

        return obj
