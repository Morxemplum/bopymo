# Bopymo

Bopymo is a translation layer for the bopjson level format, used in the 3D Platformer Bopimo, that allows you to write Bopimo levels using Python!

It's quite simple to use. For example, this code recreates the default baseplate that you start with in the level editor:

```python
level = Bopimo_Level()

level.add_object(
    Bopimo_Block(
        shape = Shape.CYLINDER, 
        name = "Baseplate", 
        position = Vector3(0, -6, 0), 
        scale = Vector3(250, 6, 250)
    )
)
```

## Why should you use Bopymo?

* It's fun to learn a programming language
* Pull off impressive features that would be incredibly tedious to do with the level editor
* With Bopymo, you have complete control over your level
* Tap into features that are otherwise unavailable in the level editor, unleashing your full potential

## How to use Bopymo

> [!WARNING]
> Bopymo 0.3 requires a Bopimo version of 1.1.0 or newer to use. To write levels for earlier versions, there are earlier releases of Bopymo available on the releases page.

> [!TIP]
> It is recommended that you use a type checker, such as Pylance, Pyright, or MyPy. Bopymo has careful type annotations that can help you catch type errors.

Bopymo is plug and play. Use pip to install a tarball from the releases page, or build the package yourself by cloning the repository and using `python -m build`. Then you can import modules from the `bopymo` package.

```python
from bopymo.classes import Bopimo_Level
```

Once you're done, call the `export` method of a level object and give a file name. You'll now have a level file that can be opened in Bopimo.

The template.py script should have this all set up for you, so you can immediately start writing Bopimo levels in Python.

If you want a more comprehensive guide, check out the Starter's Guide on the wiki!
