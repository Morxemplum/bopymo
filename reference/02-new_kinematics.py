# Written using Bopymo 0.3 and Python 3.13.3
import math
from bopymo.bopimo_types import Vector3
from bopymo.classes import Bopimo_Block, Bopimo_Level, Game_Version, Bopimo_Rose
from bopymo.enumerators import Shape


def main() -> None:
    level = Bopimo_Level(
        "New Kinematics Test",
        "This is a quick demonstration of the new time-based kinematic system in Bopimo 1.0.14",
    )

    baseplate = Bopimo_Block(
        shape=Shape.CYLINDER,
        name="Baseplate",
        position=Vector3(0, -6, 0),
        scale=Vector3(250, 6, 250),
    )

    level.add_object(baseplate)

    block = Bopimo_Block(
        name="Old Kinematics With Backwards Compat", position=Vector3(0, 10, 0)
    )

    block.nametag = True
    block.position_enabled = True
    block.position_travel_speed = 10
    block.add_position_points([Vector3.zero(), Vector3(0, 0, 10), Vector3(10, 0, 10)])

    block_two = Bopimo_Block(name="New Kinematics", position=Vector3(0, 5, 0))

    block_two.nametag = True
    block_two.position_enabled = True
    block_two.add_position_points(
        [
            (Vector3.zero(), 0.2),
            (Vector3(0, 0, 10), 0.2),
            (Vector3(10, 0, 10), 0.2 * math.sqrt(2)),
            (Vector3.zero(), 5),
        ]
    )

    rose = Bopimo_Rose()

    level.add_object(block)
    level.add_object(block_two)
    level.add_object(rose)

    level.export("new_kinematics")


if __name__ == "__main__":
    main()
