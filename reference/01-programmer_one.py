# Written using Bopymo 0.3 and Python 3.13.3
from typing import List
from bopymo.bopimo_types import Bopimo_Color, Bopimo_Int32Array, Bopimo_Vector3
from bopymo.classes import Bopimo_Block, Bopimo_Completion_Star, Bopimo_Level, Bopimo_Object, Bopimo_Spawn
from bopymo.enumerators import Block_ID, Music, Sky
import math


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def easeOutQuad(x: float) -> float:
    x = 1 - x
    return 1 - x * x


BASE_COLOR = Bopimo_Color(110, 110, 110)
STAR_COLOR = Bopimo_Color(255, 213, 0)


def main():
    level = Bopimo_Level(
        "Programmer's Playground #1: Gradient Fractal",
        "This level was completely generated with Python! I basically reverse engineered the Bopimo level format and used it to not only create some cool concepts, but also make a complete level using what I made.",
    )
    level.death_plane = -20
    level.sky = Sky.DULL
    level.music = Bopimo_Int32Array(
        [
            Music.SIXTY_FOUR,
            Music.SICILIAN_STREET,
            Music.CONTEMPLATION,
            Music.FUNKY,
            Music.I_DONT_KNOW,
        ]
    )

    baseplate = Bopimo_Block(
        id=Block_ID.CYLINDER,
        name="Baseplate",
        color=BASE_COLOR,
        scale=Bopimo_Vector3(250, 6, 250),
    )
    level.add_object(baseplate)

    spawns: List[Bopimo_Object] = [
        Bopimo_Spawn(position=Bopimo_Vector3(110, 3.5, 0)),
        Bopimo_Spawn(position=Bopimo_Vector3(-110, 3.5, 0)),
    ]
    level.add_objects(spawns)

    # Generate outer platforms
    for i in range(0, 18):
        # Have multiples of 8
        for r in range(0, 360, 45):
            platform = Bopimo_Block(
                id=Block_ID.CUBE,
                name="Moving Platform",
                position=Bopimo_Vector3(0, 2, 0),
                rotation=Bopimo_Vector3(0, r, 0),
                scale=Bopimo_Vector3(20, 2, 20),
            )
            color = Bopimo_Color.from_hsv(15 * i, 1, 1)
            platform.color = color
            platform.rotation_enabled = True
            platform.rotation_direction = Bopimo_Vector3(0, 1, 0)
            platform.rotation_pivot_offset = Bopimo_Vector3(130 + i * 20, 0, 0)
            platform.rotation_speed = lerp(25, 4, easeOutQuad(i / 18.0)) * (
                (i % 2) * 2 - 1
            )
            level.add_object(platform)

    # Generate inner rings
    # Platforms
    platforms: List[Bopimo_Object] = []
    for i in range(0, 4):
        diameter = 145 - 31 * i
        platform = Bopimo_Block(
            id=Block_ID.CYLINDER,
            name="Platform",
            color=BASE_COLOR,
            position=Bopimo_Vector3(0, 6.5 + i * 7, 0),
            scale=Bopimo_Vector3(diameter, 7, diameter),
        )
        platforms.append(platform)
    level.add_objects(platforms)

    # Hue cycle (Rainbow)
    for i in range(0, 360, math.floor(360 / 30)):
        platform = Bopimo_Block(
            id=Block_ID.CYLINDER,
            name="Moving Inner Platform",
            position=Bopimo_Vector3(0, 6.5, 0),
            rotation=Bopimo_Vector3(0, i, 0),
            scale=Bopimo_Vector3(10, 7, 10),
        )
        color = Bopimo_Color.from_hsv(i, 1, 1)
        platform.color = color
        platform.pattern_color = color
        platform.rotation_enabled = True
        platform.rotation_direction = Bopimo_Vector3(0, 1, 0)
        platform.rotation_pivot_offset = Bopimo_Vector3(75, 0, 0)
        platform.rotation_speed = 25
        level.add_object(platform)

    # Grayscale
    for i in range(0, 360, math.floor(360 / 24)):
        platform = Bopimo_Block(
            id=Block_ID.CYLINDER,
            name="Moving Inner Platform",
            position=Bopimo_Vector3(0, 10, 0),
            rotation=Bopimo_Vector3(0, i, 0),
            scale=Bopimo_Vector3(10, 14, 10),
        )
        color = int(math.fabs((180 - i) / 180) * 255)
        platform.color = Bopimo_Color(color, color, color)
        platform.pattern_color = platform.color
        platform.rotation_enabled = True
        platform.rotation_direction = Bopimo_Vector3(0, 1, 0)
        platform.rotation_pivot_offset = Bopimo_Vector3(60, 0, 0)
        platform.rotation_speed = -25
        level.add_object(platform)

    rgb = [Bopimo_Color(255, 0, 0), Bopimo_Color(0, 255, 0), Bopimo_Color(0, 0, 255)]
    # RGB
    for i in range(0, 18):
        platform = Bopimo_Block(
            id=Block_ID.CYLINDER,
            name="Moving Inner Platform",
            color=rgb[i % 3],
            position=Bopimo_Vector3(0, 13.5, 0),
            rotation=Bopimo_Vector3(0, i * 20, 0),
            scale=Bopimo_Vector3(10, 21, 10),
        )
        platform.pattern_color = platform.color
        platform.rotation_enabled = True
        platform.rotation_direction = Bopimo_Vector3(0, 1, 0)
        platform.rotation_pivot_offset = Bopimo_Vector3(45, 0, 0)
        platform.rotation_speed = 25
        level.add_object(platform)

    cmyk = [
        Bopimo_Color(0, 255, 255),
        Bopimo_Color(255, 0, 255),
        Bopimo_Color(255, 255, 0),
        Bopimo_Color(0, 0, 0),
    ]
    # CMYK
    for i in range(0, 12):
        platform = Bopimo_Block(
            id=Block_ID.CYLINDER,
            name="Moving Inner Platform",
            position=Bopimo_Vector3(0, 17, 0),
            rotation=Bopimo_Vector3(0, i * 30, 0),
            scale=Bopimo_Vector3(10, 28, 10),
        )
        platform.color = cmyk[i % 4]
        platform.pattern_color = platform.color
        platform.rotation_enabled = True
        platform.rotation_direction = Bopimo_Vector3(0, 1, 0)
        platform.rotation_pivot_offset = Bopimo_Vector3(30, 0, 0)
        platform.rotation_speed = -25
        level.add_object(platform)

    # Generate stars
    stars: List[Bopimo_Object] = [
        Bopimo_Completion_Star(
            color=STAR_COLOR,
            position=Bopimo_Vector3(0, 35, 0),
            scale=Bopimo_Vector3(5, 5, 5),
        ),
        Bopimo_Completion_Star(
            color=STAR_COLOR,
            position=Bopimo_Vector3(290, 7, 0),
            scale=Bopimo_Vector3(5, 5, 5),
        ),
        Bopimo_Completion_Star(
            color=STAR_COLOR,
            position=Bopimo_Vector3(470, 7, 0),
            scale=Bopimo_Vector3(5, 5, 5),
        ),
        Bopimo_Completion_Star(
            color=STAR_COLOR,
            position=Bopimo_Vector3(-290, 7, 0),
            scale=Bopimo_Vector3(5, 5, 5),
        ),
        Bopimo_Completion_Star(
            color=STAR_COLOR,
            position=Bopimo_Vector3(-470, 7, 0),
            scale=Bopimo_Vector3(5, 5, 5),
        ),
    ]
    for star in stars:
        if not isinstance(star, Bopimo_Completion_Star):
            continue
        star.float_height = 0.5

    level.add_objects(stars)

    level.export("programmer_one")


if __name__ == "__main__":
    main()
