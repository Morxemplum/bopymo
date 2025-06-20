# Written using Bopymo 0.3 and Python 3.13.3
# Type Hinting
from typing import List

from bopymo.bopimo_types import Color, Int32Array, Vector3
from bopymo.enumerators import Shape, Block_Pattern, Music, Sky
from bopymo.classes import (
    Bopimo_Block,
    Bopimo_Cannon,
    Bopimo_Checkpoint,
    Bopimo_Completion_Star,
    Bopimo_Disappearing_Block,
    Bopimo_Grates,
    Bopimo_Ice,
    Bopimo_Level,
    Bopimo_Magma,
    Bopimo_Object,
    Bopimo_Pine_Tree,
    Bopimo_Spawn,
    Bopimo_Speed_Panel,
    Bopimo_Spring,
)


def section_one(start: Vector3) -> List[Bopimo_Object]:
    blocks: List[Bopimo_Object] = []

    PLATFORM_SIZE = 15
    GAP_SIZE = 25
    SECTION_ONE_COLOR = Color(132, 65, 35)
    start += Vector3(0, 0, PLATFORM_SIZE / 2 + GAP_SIZE)

    for i in range(0, 5):
        platform = Bopimo_Block(
            color=SECTION_ONE_COLOR,
            position=start + Vector3(0, 0, (PLATFORM_SIZE + GAP_SIZE) * i),
            scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE),
        )
        blocks.append(platform)

    return blocks


def section_two(start: Vector3) -> List[Bopimo_Object]:
    blocks: List[Bopimo_Object] = []

    NUM_PLATFORMS = 3
    PLATFORM_SIZE = 20
    PIVOT_RADIUS = 30
    GAP_SIZE = 10
    ROTATION_SPEED = 45
    COURSE_TWO_COLOR = Color(255, 155, 155)  # Pink
    turtle_pos = start + Vector3(0, 0, PLATFORM_SIZE / 2 + PIVOT_RADIUS + GAP_SIZE)

    # Part One: Rotation Platforms
    for i in range(0, NUM_PLATFORMS):
        plat_rot = Vector3(0, 180 * (i % 2), 0)
        rot_platform = Bopimo_Block(
            shape=Shape.CYLINDER,
            color=COURSE_TWO_COLOR,
            position=turtle_pos,
            rotation=plat_rot,
            scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE),
        )
        rot_platform.rotation_enabled = True
        rot_platform.rotation_direction = Vector3.up(
            *rot_platform.rotation.to_radians()
        )
        rot_platform.rotation_pivot_offset = Vector3(0, 0, PIVOT_RADIUS)
        rot_platform.rotation_speed = ROTATION_SPEED
        blocks.append(rot_platform)

        turtle_pos += Vector3(0, 0, PIVOT_RADIUS * 2 + PLATFORM_SIZE + GAP_SIZE)

    platform = Bopimo_Block(
        color=COURSE_TWO_COLOR,
        position=turtle_pos,
        scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE),
    )
    blocks.append(platform)
    turtle_pos += Vector3(0, 0, GAP_SIZE + PLATFORM_SIZE * 3 / 2)

    # Part Two: Position Kinematics at Constant Speed
    MOVE_SPEED = 10
    travel_distance = 50

    for i in range(0, NUM_PLATFORMS):
        moving_platform = platform.copy(position=turtle_pos)
        moving_platform.position_enabled = True
        moving_platform.position_travel_speed = MOVE_SPEED
        points = [Vector3.zero(), Vector3(0, 0, travel_distance)]
        if i % 2 == 1:
            points.reverse()
        moving_platform.add_position_points(points)
        blocks.append(moving_platform)

        turtle_pos = turtle_pos + Vector3(
            0, 0, travel_distance + PLATFORM_SIZE + GAP_SIZE
        )

    turtle_pos += Vector3(0, 0, PLATFORM_SIZE / 2)
    blocks.append(platform.copy(position=turtle_pos))
    turtle_pos += Vector3(0, 0, PLATFORM_SIZE + GAP_SIZE)

    # Part Three: Position Kinematics with Time Ranges
    DELAY = 4.0
    MOVEMENT_TIME = 6.0
    travel_distance = 250
    time_platform = platform.copy(position=turtle_pos)
    time_platform.position_enabled = True
    time_platform.add_position_points(
        [
            (Vector3.zero(), DELAY),
            (Vector3.zero(), MOVEMENT_TIME),
            (Vector3(0, 0, travel_distance), DELAY),
            (Vector3(0, 0, travel_distance), 0.0),
        ]
    )
    blocks.append(time_platform)

    turtle_pos += Vector3(0, 0, travel_distance + PLATFORM_SIZE + GAP_SIZE)
    blocks.append(platform.copy(position=turtle_pos))

    return blocks


def section_three(start_block: Bopimo_Object) -> List[Bopimo_Object]:
    blocks: List[Bopimo_Object] = []

    # Part One: Slippery Lava Pillars
    platform_length = 200
    PLATFORM_SIZE = 20
    MAGMA_HEIGHT = 50
    turtle_pos = start_block.position + Vector3(
        0, 0, start_block.scale.z / 2 + platform_length / 2
    )

    ice = Bopimo_Ice(
        position=turtle_pos, scale=Vector3(PLATFORM_SIZE, 2, platform_length)
    )
    blocks.append(ice)
    turtle_pos -= Vector3(0, 0, platform_length / 2)

    for i in range(1, 4):
        magma = Bopimo_Magma(
            position=turtle_pos
            + Vector3(0, MAGMA_HEIGHT / 2 + 1, platform_length * i / 4),
            scale=Vector3(PLATFORM_SIZE, MAGMA_HEIGHT, PLATFORM_SIZE),
            damage=50,
        )
        blocks.append(magma)
    turtle_pos += Vector3(0, 0, platform_length)

    # Part Two: Disappearing Platforms
    platform_length = 50
    SECTION_THREE_COLOR = Color(144, 31, 31)  # Red Carpet
    GAP_SIZE = 15

    part_two_plat = Bopimo_Block(
        color=SECTION_THREE_COLOR,
        position=turtle_pos + Vector3(0, 0, platform_length / 2),
        scale=Vector3(PLATFORM_SIZE, 2, platform_length),
    )
    blocks.append(part_two_plat)

    spring = Bopimo_Spring(
        position=turtle_pos + Vector3(0, 2, platform_length - PLATFORM_SIZE / 2),
        scale=Vector3(PLATFORM_SIZE / 4, 2, PLATFORM_SIZE / 4),
    )
    spring.bounce_force = 150
    blocks.append(spring)

    turtle_pos += Vector3(0, spring.bounce_force * 2 / 3, platform_length)
    blocks.append(
        Bopimo_Grates(
            position=turtle_pos, scale=Vector3(PLATFORM_SIZE, 2, platform_length)
        )
    )
    turtle_pos += Vector3(0, -25, platform_length / 2 - PLATFORM_SIZE / 2)

    for _ in range(0, 5):
        platform = Bopimo_Disappearing_Block(
            color=SECTION_THREE_COLOR,
            position=turtle_pos,
            scale=Vector3(PLATFORM_SIZE / 2, 2, PLATFORM_SIZE / 2),
        )
        platform.disappears_after = 0.5
        blocks.append(platform)
        turtle_pos += Vector3(0, 0, (PLATFORM_SIZE / 2 + GAP_SIZE))
    turtle_pos += Vector3(0, -spring.bounce_force * 2 / 3 + 25, 114)

    # Part Three: Speeding Revolution
    platform_intermission = Bopimo_Block(
        color=SECTION_THREE_COLOR,
        position=turtle_pos,
        scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE),
    )
    blocks.append(platform_intermission)

    blocks.append(
        Bopimo_Speed_Panel(
            position=platform_intermission.position + Vector3(0, 1.5, 0),
            scale=Vector3(5, 1, 5),
            speed=50,
            duration=15,
        )
    )

    platform_length = 150
    ROTATION_SPEED = 45
    turtle_pos += Vector3(0, 0, PLATFORM_SIZE / 2 + platform_length / 2 + GAP_SIZE)
    for i in range(0, 5):
        platform_rot = Bopimo_Block(
            color=SECTION_THREE_COLOR,
            position=turtle_pos,
            rotation=Vector3(0, 90 * i, 0),
            scale=Vector3(PLATFORM_SIZE, 2, platform_length),
        )
        platform_rot.rotation_enabled = True
        platform_rot.rotation_direction = Vector3.up(
            *platform_rot.rotation.to_radians()
        )
        platform_rot.rotation_speed = ROTATION_SPEED
        blocks.append(platform_rot)
        turtle_pos += Vector3(0, 0, (platform_length + GAP_SIZE))
    turtle_pos -= Vector3(0, 0, platform_length / 2)

    # Ending
    cannon = Bopimo_Cannon(
        position=turtle_pos,
        rotation=Vector3(45, 0, 0),
        scale=Vector3(PLATFORM_SIZE / 3, PLATFORM_SIZE / 3, PLATFORM_SIZE / 3),
        power=150,
    )
    blocks.append(cannon)

    STAR_OFFSET = Vector3(0, 56, 109)
    STAR_SIZE = 7
    blocks.append(
        Bopimo_Completion_Star(
            position=cannon.position + STAR_OFFSET,
            scale=Vector3(STAR_SIZE, STAR_SIZE, STAR_SIZE),
        )
    )

    PLATE_OFFSET = Vector3(0, 0, 250)
    PLATE_SIZE = 75
    plate = Bopimo_Block(
        shape=Shape.CYLINDER,
        position=cannon.position + PLATE_OFFSET,
        scale=Vector3(PLATE_SIZE, 2, PLATE_SIZE),
    )
    blocks.append(plate)
    blocks.append(Bopimo_Pine_Tree(position=plate.position + Vector3(0, 6, 0)))

    return blocks


def main() -> None:
    ## CONFIGURATION

    level = Bopimo_Level(
        name="Bopymo Starter's Guide Level",
        description="This is the reference level for the level that you write as part of the Bopymo Starter's Guide. "
        "This is a simple obstacle course that goes over various Bopimo mechanics and how they can be written in Python.",
    )
    level.death_plane = -100
    level.sky = Sky.SUNSET
    level.music = Int32Array(
        [
            Music.SERENE,
            Music.SICILIAN_STREET,
            Music.LATE_NIGHT_FIREWORKS,
        ]
    )

    ## LEVEL CODE

    baseplate = Bopimo_Block(
        shape=Shape.CYLINDER,
        position=Vector3(0, -6, 0),
        scale=Vector3(32, 2, 32),
        color=Color(232, 182, 118),
    )
    baseplate.pattern = Block_Pattern.WAVES
    level.add_object(baseplate)

    # Generate our spawn
    SPAWN_OFFSET = Vector3(0, baseplate.scale.y / 2 + 0.5, 0)
    level.add_object(Bopimo_Spawn(position=baseplate.position + SPAWN_OFFSET))

    c_one = section_one(start=baseplate.position + Vector3(0, 0, baseplate.scale.z / 2))
    level.add_objects(c_one)

    last_pos = c_one[-1].position + Vector3(0, 0, c_one[-1].scale.z / 2)
    c_two = section_two(start=last_pos)
    level.add_objects(c_two)

    # Generate checkpoint for player to go back to
    last_block = c_two[-1]
    CHECKPOINT_OFFSET = Vector3(0, last_block.scale.y / 2 + 2, 0)
    level.add_object(
        Bopimo_Checkpoint(position=last_block.position + CHECKPOINT_OFFSET)
    )

    level.add_objects(section_three(last_block))

    level.export("starter_guide")


if __name__ == "__main__":
    main()
