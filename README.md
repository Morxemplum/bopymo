# Bopymo

Bo-py-mo is a Python wrapper for the bopjson level format for the 3D Platformer Bopimo! Written in Python!

Not only does this wrapper allow you to write levels completely with Python code, it also allows you to tap into features you can not access with the in-game level editor.

It's quite simple to use. For example, this code recreates the default baseplate that you start with in the level editor:

```python
level = Bopimo_Level()

level.add_object(
    Bopimo_Block(id = Block_ID.CYLINDER, name = "Baseplate", position = Bopimo_Vector3(0, -6, 0), scale = Bopimo_Vector3(250, 6, 250))
)
```

### Why Python?

There's a couple of reasons why I chose Python as the language for my wrapper:

1. Python is a fairly simple and easy to understand language. It is many people's first programming language they learn, so by choosing Python, this will be more accessible to new comers
2. It helps keep my Python skills in check. Never underestimate how quickly you can forget a programming language.

## Why should you use Bopymo?

* It's fun to learn a programming language
* Pull off impressive features that would be incredibly tedious to do with the level editor
* With Bopymo, you have complete control over your level
* Tap into features that are otherwise unavailable in the level editor, unleashing your full potential

## How to use Bopymo

[!WARNING]
Bopymo requires a Bopimo version of 1.0.11 or newer to use. To write levels for 1.0.8 or earlier, there are legacy modules in the `legacy` folder you can use.

[!TIP]
It is recommended that you use a type checker, such as Pylance, Pyright, or MyPy. Bopymo has careful type annotations that can help you catch type errors.

Bopymo is plug and play. Clone the repository to get its modules, and make sure you import the bopymo classes by starting your script with the following.

```python
from bopymo import * # Once you finalize your level, you'll want to replace this with proper imports
```

Once you're done, call the `export` method of a level object and give a file name. You'll now have a level file that can be opened in Bopimo.

The main.py script should have this all set up for you, so you can immediately start writing Bopimo levels in Python.