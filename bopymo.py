from bopimo_types import (
    Bopimo_Color,
    Bopimo_Vector3,
    Bopimo_Vector3Array,
    Bopimo_Int32Array,
    Bopimo_ColorArray,
)

import datetime
from enum import IntEnum
import json
import random
from typing import Any, List


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


GAME_VERSION = Game_Version(1, 0, 13)

### ENUMS


class Block_ID(IntEnum):
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
    MESH = 1100
    CLOUD = 1101

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
    WEB = 2025

    # NPC
    BOPI_SPAWNER = 3000


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
    def __init__(
        self,
        id: Block_ID | int = Block_ID.CUBE,
        name: str = "Object",
        color: Bopimo_Color = Bopimo_Color(0, 0, 0),
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        self.position_points: Bopimo_Vector3Array = Bopimo_Vector3Array()
        self.position_travel_speed: float = 5

        self.rotation_enabled: bool = False
        self.rotation_pivot_offset: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0)
        self.rotation_direction: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0)
        self.rotation_speed: float = 1

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
            "position_points": self.position_points.json(),
            "position_travel_speed": self.position_travel_speed,
            "rotation_enabled": self.rotation_enabled,
            "rotation_pivot_offset": self.rotation_pivot_offset.json(),
            "rotation_direction": self.rotation_direction.json(),
            "rotation_speed": self.rotation_speed,
        }


class Bopimo_Tilable_Object(Bopimo_Object):
    def __init__(
        self,
        id: Block_ID | int = Block_ID.CUBE,
        name: str = "Tilable Object",
        color: Bopimo_Color = Bopimo_Color(0, 0, 0),
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
    def __init__(
        self,
        name: str = "My Bopimo Level",
        description: str = "Autogenerated with Python!",
    ):
        # METADATA
        self.game_version: Game_Version = GAME_VERSION
        self.time_of_save: datetime.datetime = datetime.datetime.now(datetime.UTC)

        assert self.game_version >= Game_Version(
            1, 0, 11
        ), "Bopymo requires a minimum Bopjson version of 1.0.11 to work correctly."

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
        self.__blocks: dict[int, Bopimo_Object] = {}

    def remove_object(self, uid: int) -> Bopimo_Object:
        if uid not in self.__blocks:
            raise KeyError(f"Bopimo Level does not contain an object with uid {uid}")
        return self.__blocks.pop(uid)

    def get_object(self, uid: int) -> Bopimo_Object | None:
        if uid not in self.__blocks:
            return None
        return self.__blocks[uid]

    def add_object(self, obj: Bopimo_Object) -> int:
        uid: int = random.randrange(1, 2**32)
        # If we encounter collisions, regenerate the uid
        while uid in self.__blocks:
            uid = random.randrange(1, 2**32)
        self.__blocks[uid] = obj
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
        for uid, block in self.__blocks.items():
            obj["level_blocks"]["value"].append({"uid": uid} | block.json())

        return obj

    # TODO: Add a function that can import a bopjson file.

    def export(self, file_path: str):
        with open(f"{file_path}.bopjson", "w") as file:
            file.write(json.dumps(self.json()))


## BOPIMO BLOCKS


class Bopimo_Block(Bopimo_Tilable_Object):
    def __init__(
        self,
        id: Block_ID | int = Block_ID.CUBE,
        name: str = "Generated Block",
        color: Bopimo_Color = Bopimo_Color(34, 139, 34),
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 4, 2),
    ):
        super().__init__(Block_ID.CHECKPOINT, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        return super().json()


class Bopimo_Completion_Star(Bopimo_Tilable_Object):
    __star_counter: int = 0

    def __init__(
        self,
        name: str = "Generated Completion Star",
        color: Bopimo_Color = Bopimo_Color(94, 0, 176),
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        scale: Bopimo_Vector3 = Bopimo_Vector3(4, 4, 4),
    ):
        super().__init__(
            Block_ID.COMPLETION_STAR, name, color, position, rotation, scale
        )
        self.mute: bool = False
        self.float_height: float = 1.5
        # Star ID should NOT be changed! The id is tied to how many there are
        self.__star_id: int = self.__star_counter
        self.__star_counter += 1

    @classmethod
    def get_star_count(cls) -> int:
        return cls.__star_counter

    def json(self) -> dict[str, Any]:
        obj = super().json()
        return obj | {
            "mute": self.mute,
            "star_id": self.__star_id,
            "float_height": self.float_height,
        }


class Bopimo_Spring(Bopimo_Object):
    def __init__(
        self,
        name: str = "Generated Spring",
        color: Bopimo_Color = Bopimo_Color(227, 181, 4),
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        scale: Bopimo_Vector3 = Bopimo_Vector3(3, 1, 3),
    ):
        super().__init__(Block_ID.SPEED_PANEL, name, color, position, rotation, scale)
        self.new_speed: float = 30
        self.duration: float = 10

    def json(self) -> dict[str, Any]:
        obj = super().json()
        return obj | {"new_speed": self.new_speed, "duration": self.duration}


class Bopimo_Boost_Panel(Bopimo_Object):
    def __init__(
        self,
        name: str = "Generated Boost Panel",
        color: Bopimo_Color = Bopimo_Color(0, 2, 34),
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        scale: Bopimo_Vector3 = Bopimo_Vector3(2, 2, 2),
        power: float = 50,
    ):
        super().__init__(Block_ID.CANNON, name, color, position, rotation, scale)
        self.power: float = power

    def json(self) -> dict[str, Any]:
        obj = super().json()
        return obj | {"power": self.power}


class Bopimo_Web(Bopimo_Object):
    def __init__(
        self,
        name: str = "Generated Web",
        color: Bopimo_Color = Bopimo_Color(255, 255, 255),
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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


class Bopimo_Item_Mesh(Bopimo_Object):
    def __init__(
        self,
        name: str = "Generated Item Mesh",
        color: Bopimo_Color = Bopimo_Color(255, 255, 255),
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        scale: Bopimo_Vector3 = Bopimo_Vector3(8, 2, 8),
    ):
        super().__init__(Block_ID.CLOUD, name, color, position, rotation, scale)

    def json(self) -> dict[str, Any]:
        return super().json()


## NPC BLOCKS
class Bopimo_Bopi_Spawner(Bopimo_Tilable_Object):
    def __init__(
        self,
        name: str = "Generated Bopi Spawner",
        color: Bopimo_Color = Bopimo_Color(160, 30, 176),
        position: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
        rotation: Bopimo_Vector3 = Bopimo_Vector3(0, 0, 0),
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
