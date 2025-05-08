# Import new classes when necessary.
# Usually language servers will fill this in for you when autocompleting.
from bopymo.classes import Bopimo_Block, Bopimo_Level
from bopymo.enumerators import Shape
from bopymo.bopimo_types import Vector3


def main():
    ### WRITE YOUR LEVEL CODE HERE
    level = Bopimo_Level(
        "My Bopimo Level",
        "This is my level, written using Bopymo!",
    )

    baseplate = Bopimo_Block(
        shape=Shape.CYLINDER,
        name="Baseplate",
        position=Vector3(0, -6, 0),
        scale=Vector3(250, 6, 250),
    )
    # Always add your objects to the level. This can be a common mistake you can run into
    level.add_object(baseplate)

    ### END OF LEVEL CODE
    # This will write the bopjson in the same directory. You are welcome to change the file path to save it somewhere else
    level.export("YOUR_FILE_NAME")


if __name__ == "__main__":
    main()
