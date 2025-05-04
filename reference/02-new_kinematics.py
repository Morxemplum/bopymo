# Written using Bopymo 0.3 and Python 3.13.3
import math
from bopymo.bopimo_types import Bopimo_Vector3
from bopymo.classes import Bopimo_Block, Bopimo_Level, Game_Version, Bopimo_Rose
from bopymo.enumerators import Block_ID


def main():
    level = Bopimo_Level(
        "New Kinematics Test",
        "This is a quick demonstration of the new time-based kinematic system in Bopimo 1.0.14",
    )

    baseplate = Bopimo_Block(
        id=Block_ID.CYLINDER,
        name="Baseplate",
        position=Bopimo_Vector3(0, -6, 0),
        scale=Bopimo_Vector3(250, 6, 250),
    )

    level.add_object(baseplate)

    block = Bopimo_Block(
        name="Old Kinematics With Backwards Compat", position=Bopimo_Vector3(0, 10, 0)
    )

    block.nametag = True
    block.position_enabled = True
    block.position_travel_speed = 10
    block.add_position_points(
        [Bopimo_Vector3.zero(), Bopimo_Vector3(0, 0, 10), Bopimo_Vector3(10, 0, 10)]
    )

    block_two = Bopimo_Block(name="New Kinematics", position=Bopimo_Vector3(0, 5, 0))

    block_two.nametag = True
    block_two.position_enabled = True
    block_two.add_position_points(
        [
            (Bopimo_Vector3.zero(), 0.2),
            (Bopimo_Vector3(0, 0, 10), 0.2),
            (Bopimo_Vector3(10, 0, 10), 0.2 * math.sqrt(2)),
            (Bopimo_Vector3.zero(), 5),
        ]
    )

    rose = Bopimo_Rose()

    level.add_object(block)
    level.add_object(block_two)
    level.add_object(rose)

    level.export("new_kinematics")


if __name__ == "__main__":
    main()
