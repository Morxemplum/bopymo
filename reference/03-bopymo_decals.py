# Written using Bopymo 0.3 and Python 3.13.3
from time import perf_counter
from typing import List
from bopymo.bopimo_types import Color, Vector3
from bopymo.classes import Bopimo_Block, Bopimo_Decal, Bopimo_Level, Bopimo_Object
from bopymo.enumerators import Block_ID, Decal_Type

# CHANGE THESE TO VALID CLOTHING IDS, AND SEE THEM CHANGE UPON GENERATION
SHIRT_ID = 3915
PANTS_RIGHT_ID = 3566


def main():
    level = Bopimo_Level(
        "Bopymo Decal Demonstration",
        "Experience making decals more intuitively and simpler in Bopymo.",
    )

    baseplate = Bopimo_Block(
        id=Block_ID.CYLINDER,
        name="Baseplate",
        position=Vector3(0, -6, 0),
        scale=Vector3(1024, 6, 1024),
    )
    level.add_object(baseplate)

    # This first one is a shirt decal, which should be pretty intuitive.
    shirt_decal = Bopimo_Decal(
        name=f"Shirt Decal (ID: {SHIRT_ID})",
        decal_type=Decal_Type.SHIRT,
        image_id=SHIRT_ID,
        position=Vector3(10, 5, 0),
        width=5,
        height=5,
    )
    shirt_decal.nametag = True
    level.add_object(shirt_decal)

    # This second one is a pants decal, which normally would require tinkering the transforms to get it looking right.
    # Bopymo simplifies this for you and makes it more intuitive.
    pants_decal = Bopimo_Decal(
        name=f"Pants Decal (ID: {PANTS_RIGHT_ID})",
        decal_type=Decal_Type.PANTS_FRONT_RIGHT,
        image_id=PANTS_RIGHT_ID,
        position=Vector3(0, 5, 0),
        width=5,
        height=5,
    )
    pants_decal.nametag = True
    level.add_object(pants_decal)

    # Normally, getting rotation kinematics working on a pants decal requires a lot of fine tuning the pivot to get working properly.
    # Bopymo takes care of this for you and makes this easy.
    pants_kinematics = pants_decal.copy(
        name="Pants with Rotation Kinematics",
        position=pants_decal.position - Vector3(10, 0, 0),
    )
    pants_kinematics.rotation_enabled = True
    pants_kinematics.rotation_direction = Vector3.up(0, 0, 0)
    pants_kinematics.rotation_speed = 20
    level.add_object(pants_kinematics)

    # Uncomment the following line to see a live demonstration of how well Bopymo decals adapt to rotation
    # WARNING: This will take some performance to generate
    level.add_objects(rotation_stress_test())

    level.export("bopymo_decals")


def rotation_stress_test() -> List[Bopimo_Object]:
    start_offset = Vector3(40, 0, 0)
    blocks: List[Bopimo_Object] = []
    directions: List[tuple[int, int, int]] = [
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 1),
    ]
    r = 0
    start_time = perf_counter()
    for x, y, z in directions:
        for i in range(0, 30):
            inc = i * 12
            block = Bopimo_Block(
                position=start_offset + Vector3(10 * i, 5, r * 10),
                rotation=Vector3(x * inc, y * inc, z * inc),
                scale=Vector3(5, 5, 2),
            )
            block.collision_enabled = False
            block.transparency_enabled = True
            block.transparency = 2
            decal = Bopimo_Decal(
                decal_type=Decal_Type.PANTS_FRONT_RIGHT,
                image_id=PANTS_RIGHT_ID,
                position=block.position,
                rotation=block.rotation,
                width=block.scale.x,
                height=block.scale.y,
            )
            blocks.append(block)
            blocks.append(decal)
            look_vector = Vector3.forward(*block.rotation.to_radians())
            blocks.append(
                Bopimo_Block(
                    position=block.position + look_vector * block.scale.z / 2,
                    rotation=block.rotation,
                    scale=Vector3(0.1, 0.1, block.scale.z),
                    color=Color(255, 0, 0),
                )
            )
        r += 1
    end_time = perf_counter()
    final_time = int((end_time - start_time) * 1000)
    text: List[str] = [
        "This is a stress test to show how well Bopymo decals hold up to",
        "rotations. Along with a decal, a transparent block is generated",
        "as a reference for the decal's transform to match. In addition,",
        "a visible ray (in red) shows the reference block's forward",
        "direction. If the decal is off position, size, or rotation, then",
        "that means there's a bug with Bopymo decals.",
        f"Time to generate: {final_time} ms",
        "(This will vary based on the machine that generated this)",
    ]
    for i, line in enumerate(text):
        text_block = Bopimo_Block(
            name=line, position=start_offset + Vector3(0, -0.5 * i, 70)
        )
        text_block.nametag = True
        text_block.transparency_enabled = True
        text_block.transparency = 0
        text_block.collision_enabled = False
        blocks.append(text_block)

    return blocks


if __name__ == "__main__":
    main()
