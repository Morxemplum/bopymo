from bopymo import *  # Once you finalize your level, you'll want to replace this with proper imports


def main():
    ### WRITE YOUR LEVEL CODE HERE
    level = Bopimo_Level(
        "My Bopimo Level",
        "This is my level, written using Bopymo!",
    )

    baseplate = Bopimo_Block(
        id=Block_ID.CYLINDER,
        name="Baseplate",
        position=Bopimo_Vector3(0, -6, 0),
        scale=Bopimo_Vector3(250, 6, 250),
    )
    # Always add your objects to the level. This can be a common mistake you can run into
    level.add_object(baseplate)

    ### END OF LEVEL CODE
    # This will write the bopjson in the same directory. You are welcome to change the file path to save it somewhere else
    level.export("YOUR_FILE_NAME")


if __name__ == "__main__":
    main()
