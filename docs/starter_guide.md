> [!WARNING]
> This guide is mostly finished and has a complete walk through of using the module, but it still needs polishing. What you are seeing in this page is not final and subject to change.

This is a starter guide written by the founder and maintainer of the Bopymo module to help interested level makers learn the basics of the module and how they can use the modules to make their own Bopimo levels.

# Why Use Bopymo?

Before I start teaching you the basics of Bopymo, we need to answer a couple of questions you probably have, along with ruling out any misunderstandings regarding what this wrapper is and what it is about.

## Bopymo does NOT incorporate scripting into Bopimo

One of the things I see plenty of new users of Bopimo suggest when wanting to develop levels is a way for them to "program" in Bopimo. If we were to take this statement at face value, Bopymo incorporates this suggestion head-on. With Bopymo, you program in Python and allows you to channel your programming skills into designing and developing your own Bopimo levels.

However, this is not what people usually mean when they say they want programming in Bopimo. Most of these people come from platforms such as Roblox or Garry's Mod, which has built-in features for programming through what is known as *scripting*. Scripting allows for users to write code -- in the example of Roblox, using the Lua programming language -- in-engine and translates the code inside of a script to affect game logic or in-engine behavior before or during a live session. Bopymo is _NOT that_. Bopimo's engine currently does not offer a way for level makers to make and execute custom scripts inside their engine, and is considered to be an upcoming feature that will be implemented in a future version of Bopimo.

### Instead, Bopymo does this

Although I like to call Bopymo a wrapper, if you want to be technical, _Bopymo is a translation tool_. Bopymo reverse engineers the bopjson format, Bopimo's plaintext version of their level format in the [JSON format](https://en.wikipedia.org/wiki/JSON), and encapsulates the types, objects, and attributes in Python classes. When you write a Python script using Bopymo, you are technically making a bopjson file being represented by Python instances. It is when you decide to export the level to a file, translation methods are called to convert the Bopymo instances into Python dictionaries, and finally converted into the JSON objects that make up the bopjson format. 

So Bopymo scripts _do not directly modify in-engine behavior_ during a live session unlike the scripting you see in other sandbox titles. Rather, Bopymo is taking your script and generating a playable Bopimo level with the code you've written. While it may not sound as exciting as you think, if you really have a yearn for programming and want to do programming in Bopimo, this module is the closest you're ever going to get until the developers add their own methods.

## Bopymo is NOT a full replacement for the Bopimo level editor

Bopymo technically incorporates (nearly) all of the bopjson format, so you can theoretically create your own engine that follows the bopjson format. If your engine is fully conformant with bopjson, then this module will be effective in writing files for your engine as well. At the end of the day, bopjson is a bunch of text in a file, whose standards are dictated by Bopimo. For that file to mean anything, you need to have an engine that can read bopjson and load your level. 

Even I, the founder and maintainer of Bopymo, still use the Bopimo client and in-built level editor; the level editor is useful for me to help design new level ideas, play test my generated levels, and quickly stage fixes that I will mirror to my script.

### Instead, it is an alternative backend that opens up new workflows

Consider Bopymo a companion to your level making experience in Bopimo. With Bopymo, you are able to use the full Python programming language to make your levels. This includes the ability to use custom Python packages and translate higher-level concepts into Bopymo scripts that can help you pull off features that would otherwise be incredibly difficult or impossible to pull off with the Bopimo level editor. In addition, if you find some of the editor's features dubious (e.g. Bopimo's "Pending Changes" instead of an undo system, Bopimo's backup feature not reliable enough), you can have full confidence by working in the comfort of the text editor/IDE of your choice. 

## Remaining Questions

Now, the question "Why use Bopymo?" is quite a generic and vague question, so let's break this up into a couple more specific questions that I can answer:

### Why should I have to use a programming language? This sucks

You have every right to use the current Bopimo level editor if you are not interested in programming. I did not make this module expecting it to overtake the level editor or expecting it to be ubiquitous. I made this out of my own love of programming and I found this to help me relearn my Python skills. This is meant for people who love programming and desperately want to incorporate coding into their development process.

However, if you are a developer and feel super ambitious, I'm sure you will find a way to embed this module into a custom editor. If you ever need help with embedding, I'm here to help and I will be thrilled for my module to be more accessible.

### Why would you use Python? Why not use C, C++, Rust, or [Insert Trendy Language] instead?

When I pitched my wrapper out to the Bopimo community, several people -- including the main developer FireCatMagic -- made offhand comments about how Python is not their preferred programming language and would've preferred if I wrote it in *their* language instead. Upon a bit of deliberation, I chose the Python programming language for a couple of reasons:

* Python is one of (if not *THE*) most popular programming languages there are out there. Not just programmers use Python. Python is used by data scientists, researchers, web developers (besides JavaScript), engineers, and more. On top of that, new programmers tend to learn Python as their first (and often only) programming language. So by choosing Python, I am casting the largest net so that any Python programmer will be able to use their skills to make scripts.

* When it comes to syntax, Python is very legible and easy to write. It is easy for programmers to write quick Python scripts to do things. I don't want writing Bopimo levels to be a chore, so by adopting Python, writing levels can be **fun**. That is the most important thing I want people using this module to have.

* As of right now, performance is not the biggest concern. I know that there are plenty of programmers and users out there who want to get the most efficient machine code for performing tasks; I am one of those people. At the same time, it is important to recognize the priority of performance in an application; applications that are continuously running in real time or demand low latency are going to need any performance gains they can get. Since Bopymo generates levels ahead of time and doesn't modify behavior in a live session, performance is not critical. That being said, I will make optimizations overtime to ensure that generation times can be fast, even on weaker hardware. To quote an infamous computer scientist Donald Knuth: "premature optimization is the root of all evil."

### What benefits will I get by using Bopymo over the default level editor or manually modifying the bopjson?

By adopting Bopymo and writing levels through Python scripts, you do have several key benefits you will not get by using the level editor or editing a bopjson file.

* You can have a look over an entire Bopimo level that is more human-readable than bopjson. Bopjson is technically readable, but you're reading *pure data*. This does not scale very well and can make large levels difficult to read and understand, especially if you don't know how the format works. With Bopymo scripts, you are reading *instructions* on making a level. This can be further human-readable and understandable by the use of comments, a feature that is not standard in JSON (and bopjson). Legibility will depend on the person who wrote the script, but well documented code is a night and day difference over reading a bopjson file.

* Depending on how efficient your code is, Bopymo scripts will often have much smaller file sizes than an equivalent bopjson file. If you're really efficient, you can compare the file sizes to bop files: binary files of the Bopimo level format. This helps fix one of the biggest downsides of bopjson: it's large file size. By writing a level in pure Bopymo, you can save file space.

* The Bopimo level editor, while it supports all of the basic features needed to make a Bopimo level, it does not give level makers full access to everything in the Bopimo engine. There are many hidden, upcoming, or unfinished features that are present in the Bopimo engine that often requires modifying a bopjson file or settings files to obtain. Bopymo is meant to reverse engineer bopjson, which includes hidden features. With Bopymo, you are able to tap into hidden features of the Bopimo editor with a first-class experience.

* Following the previous point, Bopymo does more than just reverse engineering the bopjson format. It offers many additional tools and incorporates community-based features with a first-class experience.
    * The biggest example is Decals; decals are not an official object in Bopimo, but rather created using Item Meshes with clothing that display a texture. Especially with decals that use the pants mesh, using and modifying decals in the level editor is difficult in the level editor. Bopymo incorporates a Decal class that abstracts the pain points away and you can use Decals as if they were any other object.
    * In addition, I have incorporated several useful methods for Vectors, a type used in Bopimo to represent information in 3D space. Using these methods allows for programmers with an understanding in vector math to pull off impressive features in Bopimo.

* With Bopymo, the power you have over making levels is only limited by your programming skills. You are able to quickly script levels that would otherwise be very tedious to make in the Bopimo level editor. With Bopymo, you have full control and unrestricted freedom.

# Getting Started

Now that we've addressed potential misconceptions and the benefits you'd get from using Bopymo, let's introduce ourselves to the general workflow of Bopymo as we introduce the basic features behind them.

## Setting Up a Bopymo Script

Make you that you have read the [requirements](/Morxemplum/bopymo/wiki#requirements) for Bopymo so you have the appropriate environment.

First thing's first, we need to create a new Python script and set it up so that we can start using Bopymo. Bopymo is designed in a "plug and play" fashion, but the package is split up into various modules, each providing crucial functionality to the package. Throughout this starter guide, there are going to be three modules that we will be using: `bopimo_types`, `enumerators`, and `classes`. We will go over the `enumerators` module in a bit, but we want to focus on `bopimo_types` and `classes`. 

The `bopimo_types` modules is going to contain additional types that are important in the context of a Bopimo level. These contain types that can not be sufficiently represented by a native Python type. In addition, plenty of these types have additional methods that will help accommodate various workflows and speed up your scripting.

```python
from bopymo.bopimo_types import *
```

The `classes` module is going to contain all of the classes encapsulating our Bopimo blocks and higher-order objects.

```python
from bopymo.classes import *
```

Now, *it is bad convention to use a \* for importing modules*. If you have an IDE / text editor with a language server that can fill in imports for you, it's best to not add these lines and let your IDE do the work. If you don't have such an IDE, it's best to use these lines for right now so we don't have to constantly import classes. When we get to finalizing our level, we will be replacing these by only importing the classes and types we need.

To follow regular Python convention, we are also going to be implementing a `main()` method to put all of our code in. So now, your initial script should look like this:
```python
from bopymo.bopimo_types import *
from bopymo.classes import *

def main() -> None:
    pass

if __name__ == "__main__":
    main()
```

>[!NOTE]
> The `None` return type is optional. However, if you're using a type checker on its strictest settings (like MyPy strict), you are expected to give the `None` return type for methods that don't return anything, otherwise you will get an error.

## Setting Up Our Bopimo Level

Now that we have our script set up, let's start our Bopymo script by creating a `Bopimo_Level` object. The `Bopimo_Level` class contains metadata, level settings, and all of the objects inside the level. Bopimo calls their objects "Blocks", but for the sake of this guide, I am going to be referring to all blocks as "objects". 

The following line of code below will create a brand new Level object that we can use.
```python
level = Bopimo_Level()
```

This is legal Bopymo code that will create a level object. However, I'm sure that most of us want to give our level a name and a description. Fortunately, the level object can be instantiated with a given name and description.

### Declaring Metadata

```python
level = Bopimo_Level(name = "Starting Guide Level", description = "This level is gonna teach me how to write Bopimo levels using Python!")
```
>[!NOTE]
> The `level` and `description` keywords are the names of the parameters, and are not required to instantiate a level. However, in Bopymo, it is strongly recommended that you supply keyword arguments rather than sequential arguments with objects coming from the `classes` module. This will ensure your code is less likely to break in future updates.

Perfect! Now we have a Bopimo level that has a custom name and description. And by default, the Bopimo version that our level will be using will be the latest feature version that is correlated to the Bopymo version. So we can assume that our module will have access to the latest features.

### Changing Level Settings

Now, let's start changing the level settings. The way we change level settings is by modifying the attributes of our Level object. For example, Bopimo's default value on a death plane has a relatively low altitude to where we are going to be building our level. So when players fall into the void, there will be a noticeable delay before they reach the death plane and die. The death plane is represented by the `death_plane` attribute, so we're going to set our level's death plane to have a lower value. We're going to set it to a value of `-100` instead of the default `-1000`. To modify an attribute of an object, you will write a line of code in the following format:
```
<OBJECT>.<ATTRIBUTE> = <VALUE>
```
Employing this format to change the death plane, our code stub should now look like this:

```python
level = Bopimo_Level(name = "Starting Guide Level", description = "This level is gonna teach me how to write Bopimo levels using Python!")
level.death_plane = -100
```

Great! Now when players fall off the map, they will reach the death plane quicker and respawn faster.

Let's start changing our level's environment. We're going to be changing the level's skybox to something a little more relaxing. Bopimo represents the skybox attribute by an integer value. By default, we're going to have a value of `0`, which is the "Day" skybox. Let's lower the sun and get a nice sunset. The "Sunset" skybox is represented by a value of `1`. The skybox attribute is called `sky`. This following line of code will change the level skybox to our Sunset skybox.

```python
level.sky = 1
```

### Introduction to Enumerators

The line of code that we wrote to change the sky is legal Bopymo code, and is how the data is represented verbatim in a bopjson file. However, there are a couple of problems with assigning a direct integer to a property like the skybox.

* Memorizing what integers represent what values is not easy. Oftentimes, properties that rely on integer values will have dozens of values that represent different settings. Keeping up with the latest values is difficult and exhausting
* This makes you prone to typing in an incorrect, or worst case *nonexistent*, value. When typing in nonexistent values, you will get undefined behavior, or worst case have the client error and crash.
* These values can be changed at **any time** by the Bopimo developers. This was the case with certain block patterns in the Bopimo 1.1.0 update. An integer that represents one value may represent another in a future version. This will break your code and require you to correct the value(s) to work in later versions.

This poses a significant problem. Fortunately, Bopymo solves this issue by using something called *enums*. Short for enumerators, enums abstract constant integers into human-readable values. This not only makes it easier to access different values, but also helps future-proof your code and abandons the need to memorize values. 

Bopymo has various defined enums to accommodate many different settings, all contained in the `enumerators` module. If you don't have automatic imports with your IDE, add this line to your imports.

```python
from bopymo.enumerators import *
```

Let's go back to our skybox. Instead of using an integer to change the sky, we are going to be using the `Sky` enum to set the skybox for our level. For the "Sunset" skybox, the value would be `Sky.SUNSET`. Using the new enum, the line of code should now be

```python
level.sky = Sky.SUNSET
```

Now our skybox will be guaranteed the sunset skybox. Python will handle the Enum behind the scenes and fill it in with the equivalent integer. This means that the appropriate enum is interoperable with integers on a given property.

### Working with Data Structures (Arrays)

Let's change the level's music. These are a collection of songs from the official Bopimo soundtrack that will play in the background and enhances your level's atmosphere by adding a diegetic element players will be listening to while playing your level. Since we have a relaxing level, let's choose some songs that give a relaxing feeling. I find that the songs "Serene", "Sicilian Street", and "Late Night Fireworks" tend to fit the tone pretty well, so that's what I want to use. The `Music` enum will have all of the song titles we can choose from.

But here's the thing, I want to add *multiple* songs to my level music, but how would I do that? Bopjson has special types within their format that help represent the data structures that we'll need to add all of our music. Since enums will be translated to their respective integer values by Python, we will simply use an array of integers. Bopjson uses 32-bit integers to represent their music values, so the type that we'll need to use is `Int32Array`. The following lines of code will add all of our music to our level.

```python
level.music = Int32Array()
level.music.add_int(Music.SERENE)
level.music.add_int(Music.SICILIAN_STREET)
level.music.add_int(Music.LATE_NIGHT_FIREWORKS)
```

Great. But we can improve this code and do this all in one assignment. Fortunately, `Int32Array` does allow you to give a Python list as an argument and create the array. So now it should look like this:

```python
level.music = Int32Array(
    [
       Music.SERENE,
       Music.SICILIAN_STREET,
       Music.LATE_NIGHT_FIREWORKS
    ]
)
```
>[!WARNING]
>Python does not have a bit limit on their integers, unlike most programming languages. However, as implied by the number "32", the integers in this array (and for most integer properties in Bopjson) are represented by only 32 bits. If you give a number that cannot be represented by 32 bits, you will have a value that will [overflow](https://en.wikipedia.org/wiki/Integer_overflow) into a value that *can* be. When an array is given an integer that can't be represented in the appropriate bits, Bopymo will throw an error. It is the level maker's responsibility to handle overflowing and under-flowing values.
 
Great! Now we have set our level's music by using an integer array and will play the songs we want to our players. There are far many more things we can customize about our level, but we are going to move on to actually making our level.

Our script so far should look like this
```python
from bopymo.bopimo_types import *
from bopymo.classes import *
from bopymo.enumerators import *

def main():
    level = Bopimo_Level(name = "Starting Guide Level", description = "This level is gonna teach me how to write Bopimo levels using Python!")
    level.death_plane = -100
    level.sky = Sky.SUNSET
    level.music = Int32Array(
        [
           Music.SERENE,
           Music.SICILIAN_STREET,
           Music.LATE_NIGHT_FIREWORKS
        ]
    )

if __name__ == "__main__":
    main()
```

## Creating Objects In Our Level

Alright, now that we have finished configuring our level metadata and settings, it's now time to start creating our level. The various objects that are available in Bopimo are encapsulated in Python classes, each with their specific attributes and methods that we can use to create and configure our objects to how we would want them.

First, what is our level going to be about? Well, considering Bopimo is a 3D platforming game, it's only fair that for this guide we should create a simple platforming course that demonstrates all of the basics of Bopymo. We're not going to worry too much about a theme here.

### Creating Primitives

To start off, we're going to focus on creating primitives. What are primitives? Your cubes, ramps, cylinders, and all of the basic blocks in Bopimo are what I call "Primitives". They are the basic building blocks for what helps give your level shape and structure. In Bopymo, primitives are all represented by one class: `Bopimo_Block`.

Let's start by creating the primitive that the Bopimo level editor starts you out with: The Baseplate. Despite it being a baseplate, there are a couple of configurations that we'll need to perform on a block object to get it to match the characteristics, and we can do this by setting properties.

Let's create a variable called `baseplate` and assign it a brand new instance of `Bopimo_Block`.
```python
baseplate = Bopimo_Block()
```

By default, when you create a block object, it will be in the shape of a Cube (or rectangular prism if you want to be a geometry nerd). However, the shape for the default baseplate is not a cube; it is a cylinder. To change the shape of a block to a different primitive, we are going to be setting the `shape` attribute using the `Shape` enum. The `Shape` enum comprehensively lists all possible shapes in Bopimo. The value for a cylinder is `Shape.CYLINDER`. 

```python
baseplate = Bopimo_Block()
baseplate.shape = Shape.CYLINDER
```

#### Introducing The Vector3 Type

So now our block is the correct shape, but there are a couple other properties we need to change to get it to match the original: position and size. This is where `Vector3` is going to come into use. The Vector3 class encapsulates mathematical vectors used to define values in 3D space, using X, Y, and Z numeric values (in that order). This is used by 3D engines to represent various transformation data, such as position, rotation, scale, or directions. Bopimo is no exception. 

While we can change the attributes individually, `Vector3` requires you to specify the XYZ values to construct an instance (there are alternative and special constructors, but we'll worry about those later). Bopimo puts the default baseplate at a position of `(0, -6, 0)`. It is odd that the baseplate is not in the origin position, but I'm assuming the developers have done this to not only adjust for the thickness of the plate, but also so that a Bopi's head position will be at a Y level of 0. In addition, Bopimo scales the default baseplate to a size of `(250, 6, 250)`. Not only for plenty of thickness, but also plenty of building space for level makers to start building from. To set our baseplate to these values, we will instantiate `Vector3` instances with those XYZ values.

```python
baseplate = Bopimo_Block()
baseplate.shape = Shape.CYLINDER
baseplate.position = Vector3(0, -6, 0)
baseplate.scale = Vector3(250, 6, 250)
```

Congratulations, we now have a 1:1 recreation of the default baseplate using Bopymo.

#### Introducing the Color Type

Bopymo's classes will have default values for attributes that are meant to mimic the default values for Bopimo's level editor. So technically, our baseplate is already in the correct color. But that's boring. I want our level to at least have a little bit of pizazz. One of the easiest ways that we can make our newly created baseplate unique is by changing the color. To do this, we need to use a special type called `Color`. The class encapsulates your typical [RGB color model](https://en.wikipedia.org/wiki/RGB_color_model) with 8-bit unsigned integer values, meaning that each channel's value will range from 0 to 255. There is no alpha channel present in this color object; while it is valid bopjson, the alpha channel is never used; if you want alpha, use the `opacity` attribute and give an integer instead.

Let's make our baseplate represent sand. Using an online color picker, I found an optimal sand color that has an RGB value of `(232, 182, 118)`. So let's apply this value to our baseplate using `Color`

```python
baseplate.color = Color(232, 182, 118)
```

Great, but the underlying checkerboard pattern doesn't give a convincing representation that this is supposed to be sand. I think the "Waves" block pattern will help sell that this is meant to be a sandy material. Fortunately, we can use the `Block_Pattern` enum to set the `pattern` attribute of our baseplate.

```python
baseplate.pattern = Block_Pattern.WAVES
```

Perfect! Now we have taken the default baseplate and further customized it's attributes to change its appearance. So now the entire baseplate configuration should look like this

```python
baseplate = Bopimo_Block()
baseplate.shape = Shape.CYLINDER
baseplate.position = Vector3(0, -6, 0)
baseplate.scale = Vector3(250, 6, 250)
baseplate.color = Color(232, 182, 118)
baseplate.block_pattern = Block_Pattern.WAVES
```

#### Introduction to "Quickhanding"

So far, the setup for making blocks in Bopimo seems pretty straightforward. However, it took us 6 statements to create and define our baseplate to the way we wanted it. What if there was a way that we can take all of that configuration and declare it upon instantiation? Fortunately, the `Bopimo_Block` class offers parameters that you can put in to quickly define the most commonly used attributes. Nearly all of the attributes that we have defined can be offered as arguments in the constructor, with the exception of `pattern`. Taking advantage of these constructor parameters with keyword arguments, we can get this baseplate created using only 2 statements.

```python
baseplate = Bopimo_Block(
    shape=Shape.CYLINDER, 
    position=Vector3(0, -6, 0), 
    scale=Vector3(250, 6, 250), 
    color=Color(232, 182, 118)
)
baseplate.block_pattern = Block_Pattern.WAVES
```

What this code block demonstrates is a concept that I informally like to call "quickhanding". Bopymo classes have varying attributes that can be quickhanded, but the main purpose of quickhanding is to use keyword arguments to quickly define objects without the need to assign them to a variable. And you will see where this concept will come into good use.

## Adding Objects to Our Level

We managed to create a sandy baseplate using some Python code, but if we were to take the code we have so far and translate it into a bopjson file, you'll still have an empty level with no blocks. Where did my baseplate go? Well, you did create the baseplate, but we need to take our block object and add it to our level's `blocks` structure, represented by a Python dictionary. **A level will only contain the blocks you have added to its dictionary**. A common mistake you'll probably run into when using Bopymo is _forgetting to add the block into the level_. So let's add our baseplate into our level so it will show up.

The `Bopimo_Level` class has various methods on how to handle a level's blocks. The one we're going to focus on is a method called `add_object`. This method is what we're going to use to add our block object into the level.
```python
level.add_object(baseplate)
```

Now when we go to generate our level, the final bopjson file will have our created baseplate. 

If you are an especially keen observer, you'll realize that this method actually returns an integer. The integer that is being returned is the object's `UID` in the level. This UID serves as a integer reference to our block object in the level's object dictionary. This is a default attribute in the bopjson format to help uniquely identify objects, so they are randomly generated. Bopymo will ensure that no collisions will occur when objects are added to a level in the very rare chance they happen. This UID value is required to reference other objects (example: the Portal object and its destinations) when configuring objects. 

# Creating A Level Using Bopymo

Alright, so now we are going to actually design an obstacle course that we'll have the player complete. The course will have a star at the end the player can collect and complete the level.

We're going to split our course into three sections: Basic platforming, platforming with Kinematics, and a finale that will use action objects to complete our level. At the end, we'll create an ending platform with some decoration. Along the way, I will be introducing and explaining more Bopimo features and how to recreate them through Bopymo.

>[!NOTE]
>For this guide, you're going to follow the steps as I go along, but when you start designing and creating actual levels with Bopymo, you will often generate incomplete levels, just to see how well your code is applying and to [play test](#exporting-our-level-and-playtesting) your creation. This is normal, as you'll want to save, generate, and test your changes frequently.

Alright, so first thing's first, let's take our sandy baseplate and shrink it to an appropriate size. The size is meant for people using the Bopimo Editor to have a canvas to build on, but we don't need the player to be walking *that* much to get to our course. The updated code now looks like this:

```python
baseplate = Bopimo_Block(
    shape=Shape.CYLINDER, 
    position=Vector3(0, -6, 0), 
    scale=Vector3(32, 6, 32), 
    color=Color(232, 182, 118)
)
baseplate.block_pattern = Block_Pattern.WAVES
level.add_object(baseplate)
```

Although the Bopimo engine will spawn players at the origin position by default, I think it is important to create a spawn to ensure that we can be confident that our players will be spawning at the start like they are supposed to. Spawns are represented by the `Bopimo_Spawn` class. The only attribute we care about is position, as everything else is serviceable (feel free to change other attributes like color, pattern, and rotation to experiment).

Let's introduce ourselves to a practice that you'll find useful when making scripts: Grouping. I use this term loosely, because Bopimo does not have a native method of grouping multiple objects together. What I'm going to be doing is referencing the baseplate's position and giving an offset position so that the spawn will be positioned relative to our baseplate. 

Thanks to the advantages of programming, grouping is quite easy. Since we have our baseplate assigned to the variable `baseplate`, we can reference the object's position and add our "offset" position to calculate the spawn's position. To ensure we calculate a precise offset, we're going to take the Y scale of our baseplate (6) and divide the value in half (3). Then, we are going to take the Y scale of our spawn (by default, this will be 1) and also divide the value in half (0.5). By adding these two values together, we get a value of 3.5, which is the offset position of our spawn in the Y axis that will have the spawn placed on top of our baseplate.

```python
SPAWN_OFFSET = Vector3(0, baseplate.scale.y / 2 + 0.5, 0)
level.add_object(Bopimo_Spawn(position=baseplate.position + SPAWN_OFFSET))
```

And thanks to quickhanding, we don't have to declare a separate variable for the spawn. So we have added a spawn into our level with only 2 lines of code.

## Basic Platforming Section

Alright, now let's start on the first section of our level by adding platforms. We don't have to be fancy about it, just some simple platforms that players must jump across. I'm going to add 5 platforms that the user must hop across.

To follow our useful practice of grouping, we're going to calculate a starting position for our first section of the level using the baseplate's Z scale and our platform's size. I'm going to have our course go in the Z axis, as Z is typically associated with depth.

```python
start_pos = baseplate.position + Vector3(0, 0, baseplate.scale.z / 2 + 7.5)
```

As a useful programming practice, it's best that you make sure you minimize the amount of "magic" numbers you have. Magic numbers are arbitrary numbers that don't have a clear meaning on what they're used for. In this case, `7.5` is considered a magic number. It's meant to be half the size of my platforms, but I don't make that clear in my code. 

I'm going to declare a constant that will represent the size of my platforms, so that if I choose to read this code weeks from now, I know what the number means. I'm also going to declare a constant `GAP_SIZE` that is meant to resemble the number of units between platforms, so that they are consistent and players will have to actually jump between platforms. I'll also declare a constant `SECTION_ONE_COLOR` so they stand out. I'm going to choose a brownish-orange color, but feel free to change this to whatever color you like.

```python
PLATFORM_SIZE = 15
GAP_SIZE = 25
SECTION_ONE_COLOR = Color(132, 65, 35)
start_pos = baseplate.position + Vector3(0, 0, baseplate.scale.z / 2 + PLATFORM_SIZE / 2 + GAP_SIZE)
```

Now, we can easily create our platforms. We can do this by having 5 different `add_object` calls, but we're employing another general programming practice: don't duplicate code that does the same thing. I'm going to use a for loop to pull this off.

```python
for i in range(0, 5):
    platform = Bopimo_Block(
        color=SECTION_ONE_COLOR, 
        position=start_pos + Vector3(0, 0, (PLATFORM_SIZE + GAP_SIZE) * i),
        scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE)
    )
    level.add_object(platform)
```

With that one loop, that completes our first section of our level. This code is already going to be much easier for someone to read than if you were to just give them bopjson to read.

## Learn to Organize Your Level Code

Before we get started on the next section of our level, let's take a brief pause for a moment. This is the starter guide and the level we're making is simple, but if you are going to be making more complex levels with several sections or even non-linear design, it is important to know how to break up your course/map into reasonable groups, and then split those groups into separate functions. This is going to help you organize your code and keep it modular. We've already been sort of taking advantage of a sense of grouping by calculating relative positions, but functions will further enhance this grouping and make it easier.

What we're going to do is take all of the code that we have written for our first section and break it up into its own function, so that we can generate that entire section in just one function call within the `main` function. Let's create a function called `section_one` and drag all of our code there

```python
def section_one():
    PLATFORM_SIZE = 15
    GAP_SIZE = 25
    SECTION_ONE_COLOR = Color(132, 65, 35)
    start_pos = baseplate.position + Vector3(0, 0, baseplate.scale.z / 2 + PLATFORM_SIZE / 2 + GAP_SIZE)

    for i in range(0, 5):
        platform = Bopimo_Block(
            color=SECTION_ONE_COLOR, 
            position=start_pos + Vector3(0, 0, (PLATFORM_SIZE + GAP_SIZE) * i),
            scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE)
        )
        level.add_object(platform)
```

Great, but do you see the problem with this stub? Since we have decided to move all of the code to its own function, the code no longer has a reference to our level object, nor our baseplate object that we used for calculating our start position. This is invalid Python code and will error. So how do we fix this problem?

First, let's take care of the level reference problem. Since we no longer have a level to add our objects to, what we can do is use a data structure to store all of our newly created objects. A Python list is simple and should do the job. Next, we're going to replace all ``add_object`` calls and replace them with ``append`` calls. Then, what we will do is we're going to take our list and return it. 

```python
def section_one():
    blocks = []

    PLATFORM_SIZE = 15
    GAP_SIZE = 25
    SECTION_ONE_COLOR = Color(132, 65, 35)
    start_pos = baseplate.position + Vector3(0, 0, baseplate.scale.z / 2 + PLATFORM_SIZE / 2 + GAP_SIZE)

    for i in range(0, 5):
        platform = Bopimo_Block(
            color=SECTION_ONE_COLOR, 
            position=start_pos + Vector3(0, 0, (PLATFORM_SIZE + GAP_SIZE) * i),
            scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE)
        )
        blocks.append(platform)
    
    return blocks
```

By returning a list of our created objects, we are passing the responsibility of adding the objects in our level to the caller of our function; in this case, the caller will be our `main` function with the level object. 

Now, for this section, all objects will be of type `Bopimo_Block`. Soon enough, however, you will often have objects of varying types; your type checker is going to pester you about this sooner or later. So how can we ensure that our list will have a consistent type? All Bopymo classes that encapsulate "blocks" all inherit from one class: `Bopimo_Object`. This class is meant to represent as the superclass that all level objects inherit from, and will be at the top of the inheritance tree. One of the benefits for me, the maintainer, is it heavily de-duplicates code. However, the biggest benefit for you is that you can utilize [polymorphism via subtyping](https://en.wikipedia.org/wiki/Polymorphism_(computer_science)#Subtyping) and declare a Python list where the elements are all of type `Bopimo_Object`.

```python
def section_one() -> List[Bopimo_Object]:
    blocks : List[Bopimo_Object] = []

    PLATFORM_SIZE = 15
    GAP_SIZE = 25
    SECTION_ONE_COLOR = Color(132, 65, 35)
    start_pos = baseplate.position + Vector3(0, 0, baseplate.scale.z / 2 + PLATFORM_SIZE / 2 + GAP_SIZE)

    for i in range(0, 5):
        platform = Bopimo_Block(
            color=SECTION_ONE_COLOR, 
            position=start_pos + Vector3(0, 0, (PLATFORM_SIZE + GAP_SIZE) * i),
            scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE)
        )
        blocks.append(platform)
    
    return blocks
```

We took care of the typing issue and the level referencing issue. But we need to handle the baseplate referencing issue. How are we going to calculate the starting position without the baseplate? Similar to the level referencing, we're going to push responsibility onto the caller. In this instance, we are able to calculate part of the starting position with our platform size, so we can leave the platform size calculation. However, the remaining calculations are going to be abstracted by adding a parameter to our function that we'll call `start`. `start` will replace `start_pos` to represent our starting position.

```python
def section_one(start: Vector3) -> List[Bopimo_Object]:
    blocks : List[Bopimo_Object] = []

    PLATFORM_SIZE = 15
    GAP_SIZE = 25
    SECTION_ONE_COLOR = Color(132, 65, 35)
    start += Vector3(0, 0, PLATFORM_SIZE / 2 + GAP_SIZE)

    for i in range(0, 5):
        platform = Bopimo_Block(
            color=SECTION_ONE_COLOR, 
            position=start + Vector3(0, 0, (PLATFORM_SIZE + GAP_SIZE) * i),
            scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE)
        )
        blocks.append(platform)
    
    return blocks
```

Perfect, now we have a valid Python function that will run without throwing an error. Now let's return to our `main` function and add our separated section into our level. `Bopimo_Level` has a separate method called `add_objects`, which will accept a Python list of objects and add them all to our level. We'll just simply supply our function call as the argument. Now, let's take our previous baseplate calculations and apply them to the `start` argument. 

```python
level.add_objects(
    section_one(
        start = baseplate.position + Vector3(0, 0, baseplate.scale.z / 2)
    )
)
```

Now we have broken up section one into a separate function. We are going to be employing this same tactic for the remaining sections, but I am going to be leaving you to figure out how to split off the code. Again, this is an extremely good practice and _I highly recommend you do this_ so your `main` function is not over-congested with level code.

## Platforming with Kinematics

> [!TIP]
> When you are done with a section and you are working on a different section, one of the big benefits of breaking up your level code is that you can comment out the function call in your `main` function and remove it from generation.
> 
> This is especially useful if you are repeatedly generating bopjson files to test out your changes. Having less objects to generate will make generation go by significantly faster and less taxing on performance.

Now, let's create the next section of our level. We're going to make things a little more interesting, and we're going to be using Bopimo's kinematic system to create moving and rotating platforms.

We're going to be utilizing seven platforms here. The first three are going to be rotating around a pivot; the remaining platforms are going to be moving using position kinematics; three of them are going to be moving at constant speed, and the last one will be using time-based kinematics for multiple speeds.

Unfortunately, kinematics can NOT be quickhanded in Bopymo, and for good reason. Being able to quickhand kinematics would lead to code that can be difficult to read. We're going to be declaring them in separate statements.

### Rotation Kinematics

Rotation kinematics is going to be the easier one to understand out of the two, so let's do this one first. Similar to our previous section, I'm going to do some setup by declaring important constants and setting a starting position that all of our blocks will be relative towards to ensure grouping.

Since I don't have direct access to the last block of the previous position, I am going to give an arbitrary starting position for right now and I will be changing it once I am finished with the section.

```python
NUM_PLATFORMS = 3
PLATFORM_SIZE = 20
PIVOT_RADIUS = 30
GAP_SIZE = 10
ROTATION_SPEED = 45
COURSE_TWO_COLOR = Color(255, 155, 155) # Pink
# TODO: Get a more accurate starting position
turtle_pos = Vector3(0, 0, 30 + PLATFORM_SIZE / 2 + PIVOT_RADIUS + GAP_SIZE)
```

Now, let's create a basic cylindrical platform that we'll be employing kinematics on.

```python
rot_platform = Bopimo_Block(shape=Shape.CYLINDER, color=COURSE_TWO_COLOR, position=turtle_pos, scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE))
```

In order for our rotation kinematics to have any effect, we need to first enable rotation kinematics by setting `rotation_enabled` to `True`.

```python
rot_platform.rotation_enabled = True
```

Perfect, now we can start employing rotation kinematics. There are two attributes that must be changed to see any rotation: `rotation_direction` and `rotation_speed`. The `rotation_direction` takes a Vector3 value, but the Vector3 value in this setting is special. Since we are dealing with a direction, the Vector is meant to resemble a [unit vector](https://en.wikipedia.org/wiki/Unit_vector). Unit vectors have a constraint: **All three values in the vector must add up to 1**. For this example, I only want to rotate the platform on the Y axis, so the unit vector for this one is simple: `(0, 1, 0)`.

However, Bopymo offers constructors that allow you to easily calculate unit vectors, should you be working with a rotated object and you want the direction to be relative. We're going to use this method instead to show you what Bopymo has to offer. 

Bopimo and Bopjson measure their rotation values in **degrees**. However, to calculate a unit vector in Bopymo, the rotation must be given in **radians**. Bopymo offers methods to easily convert between the two units. And since we want to rotate on the axis upwards of the object, the constructor we should use is `Vector3.up`. 

```python
rot_rad = rot_platform.rotation.to_radians()
rot_platform.rotation_direction = Vector3.up(rot_rad.x, rot_rad.y, rot_rad.z)
```

This snippet gives a rudimentary breakdown of how calculating the unit vector works. However, Bopymo incorporates an operator into Vector3 that can help us simplify this snippet even further. By prefacing our converted rotation with a `*`, we can utilize Python [syntactic sugar](https://en.wikipedia.org/wiki/Syntactic_sugar) to quickly unpack the XYZ values and shorten our snippet to one line.

```python
rot_platform.rotation_direction = Vector3.up(*rot_platform.rotation.to_radians())
```

> [!WARNING]
> This is not exclusive to calculating unit vectors. Any vector math that is done in Bopymo involving rotation will use radians, NOT degrees. This can be a common mistake to run into when making more advanced levels, so please make sure you are using the correct units by converting using `to_radians` and `to_degrees` when necessary.

As for rotation speed, this one is fairly straightforward

```python
rot_platform.rotation_speed = ROTATION_SPEED
```

And with these two attributes changes, you will have a rotating platform in the Y axis. It is cool, but in terms of gameplay, isn't much different from our previous section. So to put a spin on this, we're going to be utilizing `rotation_pivot_offset` to offset the platform's position, so it will revolve around the pivot.

> [!WARNING]
> The `rotation_pivot_offset` vector is local to the object's position. Make sure you aren't using global coordinates when setting the pivot.
```python
rot_platform.rotation_pivot_offset = Vector3(0, 0, PIVOT_RADIUS)
```

Now we have created a revolving platform using rotation kinematics. So our code should look like this:

```python
rot_platform = Bopimo_Block(shape=Shape.CYLINDER, color=COURSE_TWO_COLOR, position=start_pos, scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE))
rot_platform.rotation_enabled = True
rot_platform.rotation_direction = Vector3.up(*rot_platform.rotation.to_radians())
rot_platform.rotation_pivot_offset = Vector3(0, 0, PIVOT_RADIUS)
rot_platform.rotation_speed = ROTATION_SPEED
```

Now for the sake of simplicity, we were only focusing on *one* revolving platform. We want to make three revolving platforms for our level. 
We could just increment the position in a for loop and call it a day. However, if you were to generate the level and test it out, you'll find all the revolving platforms will have constant distance between them, which can be difficult to navigate. To make this easier, we should make the middle platform start revolving on the opposite side. There are multiple approaches on how this can be done, including inverting the `rotation_pivot_offset`. However, one neat thing about rotation kinematics is the object's rotation is also taken into consideration when offsetting the platform. So instead, we can just rotate the platform by 180 degrees and it'll do the same thing; this will not affect our unit vector calculation, as the rotation does not affect the upward direction.

Here is the resulting for loop that employs this tactic:

```python
for i in range(0, NUM_PLATFORMS):
    plat_rot = Vector3(0, 180 * (i % 2), 0)
    rot_platform = Bopimo_Block(shape=Shape.CYLINDER, color=COURSE_TWO_COLOR, position=turtle_pos, rotation=plat_rot, scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE))
    rot_platform.rotation_enabled = True
    rot_platform.rotation_direction = Vector3.up(*rot_platform.rotation.to_radians())
    rot_platform.rotation_pivot_offset = Vector3(0, 0, PIVOT_RADIUS)
    rot_platform.rotation_speed = ROTATION_SPEED
    level.add_object(rot_platform)

    turtle_pos += Vector3(0, 0, PIVOT_RADIUS * 2 + PLATFORM_SIZE + GAP_SIZE)
```

You may have noticed something when we were beginning this section: I decided to name the starting position `turtle_pos`. The above code snippet explains why I named it that. I am using a "turtle" method, which is based on the infamous [turtle graphics](https://en.wikipedia.org/wiki/Turtle_graphics) method of drawing graphics. I'm constantly updating the starting position to position the platforms. I am doing this method to avoid doing a separate calculation on the starting position of the next section. You will find this method useful if you are constructing a course, as it helps keep your course grouped.

Now I could shift the entire starting position all with one calculation, and it would look like this:
```python
turtle_pos += Vector3(0, 0, (PIVOT_RADIUS * 2 + PLATFORM_SIZE) * NUM_PLATFORMS + GAP_SIZE)
```

However, with the turtle method, I don't have to do any of this. I'm going to also add a regular platform before starting the next series of platforms in the event the cycles don't line up, so we'll have to slightly update the final turtling.

```python
platform = Bopimo_Block(color=COURSE_TWO_COLOR, position=turtle_pos, scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE))
level.add_object(platform)
turtle_pos += Vector3(0, 0, GAP_SIZE + PLATFORM_SIZE * 3 / 2)
```

### Position Kinematics (with constant speed)

In Bopimo versions 1.0.13 and prior, position kinematics were a lot simpler, but at the same time were more limiting on what you could accomplish. Position kinematics worked by the object travelling through a looping sequence of positions, moving at a constant speed given by the level maker. Starting in Bopimo 1.0.14, the speed-based kinematic system was completely replaced with a time-based kinematic system for position kinematics. You can perfectly recreate the speed-based kinematic system using the new system, but calculating the time values to keep a constant speed can be quite difficult and requires a lot of math.

Bopymo has reverse compatibility with the old speed-based kinematic system, abstracting away the math you'd need to calculate to recreate the old system. While the `position_travel_speed` attribute is no longer functional in bopjson starting at 1.0.14, it is still a modifiable attribute in Bopymo, and can be changed on any object. These next three platforms will be using the old kinematic system to ensure a constant speed.

Before starting, I'm going to add a new constant and variable that will be relevant to this section
```python
MOVE_SPEED = 10
travel_distance = 50
```

#### A Brief Introduction To Copying

Let's create a similar cubed platform for our position kinematics. But here's the thing, I've already declared an object with similar attributes. I could copy and paste the same instantiation, but that is violating one of the rules I've mentioned earlier: don't duplicate code that does the same thing. Fortunately, Bopymo classes offer the `copy` method that allows you to take a current object and copy it into a new object with identical attributes. This method is available on both classes and types, and copies will be recursive.

> [!NOTE]
> By default, copying objects and arrays in Bopymo will deep copy attributes. While this goes against convention, I chose this as the default behavior for a couple reasons:
> 1. The issues related to shallow copying can be difficult to debug, especially for newer programmers. It's more intuitive to just perform a deep copy
> 2. In the event Bopimo adds parent-child relationships to objects, ``__deepcopy__`` will be reserved for that use case, where it will also copy the object's children.
>
> To get a true shallow copy of an object, pass in `deep_copy = False` as an argument to the `copy` method. For arrays, you can also import the `copy` module and use `copy.copy`.

Let's start off the moving platform by copying the intermission platform and updating the position to the new starting position.

```python
moving_platform = platform.copy()
moving_platform.position = turtle_pos
```

However, one of the unique properties of the `copy` method on objects is that you are able to quickhand *ANY* attribute that is associated with the object, which makes it really easy to apply small changes in just one call.

```python
moving_platform = platform.copy(position=turtle_pos)
```
> [!WARNING]
> Unlike quickhanding when instantiating new objects, quickhanding when copying objects does NOT perform type checking at "compilation", and will only do type checking at run time, which can make proofreading your code more difficult. Be careful of the values you pass in when quickhanding a copied object.
>
> In addition, don't abuse the quickhanding feature to set every attribute. It can hurt the legibility of your code. You'll notice that I don't quickhand kinematics even though it is technically possible.

#### Position Kinematics cont.

Now that we have made a copy of the moving platform, similar to the rotation kinematics, we have to enable position kinematics to see any of our kinematics take effect through the `position_enabled` attribute.

```python
moving_platform.position_enabled = True
```

Position kinematics will use the new time-based kinematic system by default. This will affect the syntax that we'll be using when we get to defining our position points. So to switch to the speed-based kinematic system, we are going to set the `position_travel_speed` attribute.

```python
moving_platform.position_travel_speed = MOVE_SPEED
```

Now we need to define an ordered sequence of points that our platform will be looping through. To keep this simple for the guide, we're going to only have two position points that our platform will be moving through.

> [!WARNING]
> Like `rotation_pivot_offset`, the position vectors in position points are local to the object's position. Make sure you aren't using global coordinates.

We can not access an object's position points directly, so the only way that we'll be able to modify an object's position points is by using methods. We're going to be using `add_position_point` to add in a vector that will act as a position point for the object to move towards. The first (or start) position is going to be identical to the object's position, so it will be a position of `(0, 0, 0)`. You are free to put 0's in the default constructor, but Bopymo has a special constructor for this value: `Vector3.zero`. The second position will be using my `travel_distance` variable.

```python
moving_platform.add_position_point(Vector3.zero())
moving_platform.add_position_point(Vector3(0, 0, travel_distance))
```

This snippet works, but similar to adding objects to a level, there is a separate `add_position_points` method that will accept a Python list of Vector3 values that will bulk add them to our object.

```python
moving_platform.add_position_points(
    [
        Vector3.zero(), 
        Vector3(0, 0, travel_distance)
    ]
)
```

> [!TIP]
> In the case of speed-based kinematics, if you have many position points that you want to add, use the `add_position_points` method. When a new position point is added with `add_position_point`, the final time value is recalculated each time to ensure that speed is kept constant. However, `add_position_points` will delay this calculation until the final element. Not only will this make your code look neater, but it will cut out redundant calculations.

By putting all this together, we now have a platform moving at a constant speed. Similar to the rotation kinematic section, we will have the second platform start on the opposite side to make the level easier. To pull this off, we can just simply reverse the staging list before adding it to our object.

```python
for i in range(0, NUM_PLATFORMS):
    moving_platform = platform.copy(position=turtle_pos)
    moving_platform.position_enabled = True
    moving_platform.position_travel_speed = MOVE_SPEED
    points = [
            Vector3.zero(), 
            Vector3(0, 0, travel_distance)
        ]
    if i % 2 == 1:
        points.reverse()
    moving_platform.add_position_points(points)
    level.add_object(moving_platform)

    turtle_pos = turtle_pos + Vector3(0, 0, travel_distance + PLATFORM_SIZE + GAP_SIZE)
```

And to quickly end off this section, we'll add in one final intermission platform.

```python
turtle_pos += Vector3(0, 0, PLATFORM_SIZE / 2)
level.add_object(platform.copy(position=turtle_pos))
turtle_pos += Vector3(0, 0, PLATFORM_SIZE + GAP_SIZE)
```

### Position Kinematics (with time values)

This last platform will use the time-based kinematic system to accomplish multiple speeds. Alongside position points, are time ranges that indicate how much time (in seconds) it takes to get from the current position point to the next. Time-based kinematics have multiple advantages over speed-based kinematics:

* Different speeds
* You can bring platforms for a temporary full-stop before moving them again
* You can create the illusion of teleporting blocks by having a time value of 0

In fact, the platform we'll be making will be utilizing the latter two bullet points. It will start at our beginning position for a few seconds, move to our ending position, stop moving for a few more seconds, and then teleport back to the start.

As per usual, let's introduce a couple new constants and create our moving platform. I'm also going to update our previous `travel_distance` variable to a higher value of 250. And similar to speed-based kinematics, we need to enable position kinematics.

```python
DELAY = 4.0
MOVEMENT_TIME = 6.0
travel_distance = 250
time_platform = platform.copy(position=turtle_pos)
time_platform.position_enabled = True
```

Now this time, we are going to tackle the `add_position_point` method differently by offering a new argument that represents our time value. We didn't have to worry about this with speed-based kinematics, as any time value would've been ignored anyway. However, each position point *must have a corresponding time value*. Similar to the speed-based kinematics, we are starting the position at our object's position.

```python
time_platform.add_position_point(Vector3.zero(), DELAY)
```

For our next position, we want to put the same position point as the previous one, to ensure that the platform stays in place. Now this time, we are going to set the time value to `MOVEMENT_TIME`.

```python
time_platform.add_position_point(Vector3.zero(), MOVEMENT_TIME)
```

Now we can advance the position over to our destination position, which will use `travel_distance`. The time value will be `DELAY`.

```python
time_platform.add_position_point(Vector3(0, 0, travel_distance), DELAY)
```

Now, for our last position, we are going to keep the same position point. However, the time value will now be set to a value of 0. This will mean that the platform will teleport back to the start of our sequence.

```python
time_platform.add_position_point(Vector3(0, 0, travel_distance), 0)
```

And that creates our movement cycle for the last platform. Similar to speed-based kinematics, we can make this implementation more efficient with `add_position_points`. The way that `add_position_points` works in the time-based kinematic system is that each element is a Python tuple of a position point and time value pair.

```python
time_platform.add_position_points(
    [
        (Vector3.zero(), DELAY),
        (Vector3.zero(), MOVEMENT_TIME),
        (Vector3(0, 0, travel_distance), DELAY),
        (Vector3(0, 0, travel_distance), 0.0)
    ]
)
```

After adding the platform to the level, we're going to add our final platform that will indicate the end of the section. We'll simply move the turtle to our final position and make a simple platform.

```python
turtle_pos += Vector3(0, 0, travel_distance + PLATFORM_SIZE + GAP_SIZE)
level.add_object(platform.copy(position=turtle_pos))
```

This section was noticeably more complicated compared to the first section, with triple the number of lines of code. You can start to see why breaking up our sections into functions is incredibly useful. Fortunately, the procedures for splitting this section into its own code is pretty much the same, with only one difference.

The big difference, if you haven't figured out, is that the start position the caller provides will not be directly used by our objects, but will simply be added onto our initial turtle position. 

```python
turtle_pos = start + Vector3(0, 0, PLATFORM_SIZE / 2 + PIVOT_RADIUS)
```

Now, how are we going to connect our first section to the second one? Well, we're going to have to split the function call into its own variable, so that we can access the last block and use the position and scale to calculate our new starting position. So now our `main` function will have this updated code

```python
c_one = section_one(start=baseplate.position + Vector3(0, 0, baseplate.scale.z / 2))
level.add_objects(c_one)

last_pos = c_one[-1].position + Vector3(0, 0, c_one[-1].scale.z / 2)
c_two = section_two(start=last_pos)
level.add_objects(c_two)
```

## Giving Our Players A Break

> [!TIP]
> It is easy to get lost in creating your level, and you'll often forget how difficult a level can get. It is especially important that you play test your level often, so you can fine tune the difficulty to your preference. It will also help you ensure that what you are designing is working correctly.

We are programming our Bopimo level, but regardless of what you're using to make your Bopimo levels, level design is crucial. Since our next section is going to be more challenging than the previous two, we should add a checkpoint. When our players fail, they won't have to start from the very beginning.

Similar to how we added our spawn, we're going to be positioning the checkpoint relative to the last platform we created. So we're going to grab the last block from `c_two` and use that as our reference. A checkpoint has a default height of 4, so we'll add half of this value to our final offset.

```python
last_block = c_two[-1]
CHECKPOINT_OFFSET = Vector3(0, last_block.scale.y / 2 + 2, 0)
level.add_object(
    Bopimo_Checkpoint(position=last_block.position + CHECKPOINT_OFFSET)
)
```

Perfect! And for simplicity, we're going to keep this code in the `main` function.

## Playing with Action Blocks

Now it's time for use to build the third and final section of our level. We're going to be utilizing a variety of action blocks offered by Bopimo so we can get a basic idea of how action blocks work with Bopymo.

We're going to be starting off our section by having our players jump around 3 pillars of magma. The main point is to get the player to jump around. In addition, we're going to put a little twist on this: we're gonna make the floor use ice. This will ensure that the player has to be extra careful when landing.

First, we're going to make a variable `platform_length` for how long we want the ice floor to be. I'm gonna start with 200 units. In addition, I'm gonna give a constant `MAGMA_HEIGHT` and set it to a value that makes it so that players can't just simply jump over the pillar (I'm choosing 50). Similar to the second section, I am going to be using the turtle method to help position my objects. With some other constants out of the way, I now have all my preparation.

```python
platform_length = 200
PLATFORM_SIZE = 20
MAGMA_HEIGHT = 50
turtle_pos = last_block.position + Vector3(
    0, 0, last_block.scale.z / 2 + platform_length / 2
)
```

Now we're going to make the ice floor. The `Bopimo_Ice` class will resemble ice. Ice has a special attribute called `slipperiness`, which can increase or decrease the friction of the block for the player. However, I'm not going to change this value and keep it the same. To make sure that the magma will be properly spaced across the ice floor, I will be decrementing the turtle's position back to the start.

```python
ice = Bopimo_Ice(
    position=turtle_pos, scale=Vector3(PLATFORM_SIZE, 2, platform_length)
)
level.add_object(ice)
turtle_pos -= Vector3(0, 0, platform_length / 2)
```

Now it's time to add in our magma pillars. The `Bopimo_Magma` class will resemble magma. Magma has only a customizable pattern color (the pattern is hardcoded and can not be changed), and a `damage_amount` to deal to the player upon touching. Both of these attributes can be quickhanded (keep in mind that `damage_amount` is shortened to `damage` in quickhanding; you'll often see quickhand attribute names be shorter for legibility reasons or renamed to mimic the level editor's naming scheme). The default value for damage is 25, but I think that's too forgiving. I'm going to have each pillar deal 50 damage instead.

Normally, when I use for loops, I start my range at a value of 0, but doing so would create a pillar at our checkpoint, so I'm going to start my range at 1. Then after our loop, I will move my turtle past the ice platform.

```python
for i in range(1, 4):
    magma = Bopimo_Magma(
        position=turtle_pos
        + Vector3(0, MAGMA_HEIGHT / 2 + 1, platform_length * i / 4),
        scale=Vector3(PLATFORM_SIZE, MAGMA_HEIGHT, PLATFORM_SIZE),
        damage=50,
    )
    level.add_object(magma)
turtle_pos += Vector3(0, 0, platform_length)
```

That finishes the first part. The second part is gonna involve us propelling the player upwards and doing a jumping section similar to the first section, but with another twist: the platforms below them will fall if they are too slow. I'm going to change our platform length to 50, and I'm going to declare this section's color to be a sort of "carpet" red color. In addition, I'm going to be bringing back `GAP_SIZE` for the platforming.

```python
platform_length = 50
SECTION_THREE_COLOR = Color(144, 31, 31)  # Red Carpet
GAP_SIZE = 15
```

To help propel the player upwards, we're going to create a spring using the `Bopimo_Spring` class. To ensure that the player can safely get to our platforms and start jumping, we're also going to create a grates block using the `Bopimo_Grates` class. We're going to set `bounce_force`, as the default value `50` is kind of weak and we want to make sure that our players can't just double jump onto the platforms. In addition, the default spring size is kind of small, so I'm going to be expanding the length and width of the spring to be 1/4th the size of our platform.

Let's start part two off with by adding a platform and our spring.

```python
part_two_plat = Bopimo_Block(
    color=SECTION_THREE_COLOR,
    position=turtle_pos + Vector3(0, 0, platform_length / 2),
    scale=Vector3(PLATFORM_SIZE, 2, platform_length),
)
level.add_object(part_two_plat)

spring = Bopimo_Spring(
    position=turtle_pos + Vector3(0, 2, platform_length - PLATFORM_SIZE / 2),
    scale=Vector3(PLATFORM_SIZE / 4, 2, PLATFORM_SIZE / 4),
)
spring.bounce_force = 150
level.add_object(spring)
```

Now it's time that we add our grates. We're going to move our turtle by our platform length, but we also need to move upwards to accommodate for the spring. I'm going to take reference from the spring's bounce force to help calculate the up movement. Then after adding the grates, I'm going to move the turtle slightly downwards, and position it perfectly for our platforms.

```python
turtle_pos += Vector3(0, spring.bounce_force * 2/3, platform_length)
level.add_object(Bopimo_Grates(position=turtle_pos, scale=Vector3(PLATFORM_SIZE, 2, platform_length)))
turtle_pos += Vector3(0, -25, platform_length / 2 - PLATFORM_SIZE / 2)
```

We're going to take our code from section one and make a few adjustments. First, we're going to replace the old positioning method with the turtle method we did for section two. Then, we're going to switch from `Bopimo_Block` to `Bopimo_Disappearing_Block`, a special type of block that will disappear after prolonged contact by a player. A disappearing block has 3 exclusive attributes, but we're only going to focus on `disappears_after`, which has a default value of 2 (seconds). This is too forgiving, so I'm going to be changing this value to 0.5. Next, because we chose to lower the disappear time, we need to make our players able to traverse the platforms faster. Our platform size constant will not cut it, so I will divide it by half to get a more tolerable size. Finally, we move our turtle appropriately each iteration, leading to a final code block that should look like this.

```python
for _ in range(0, 5):
    platform = Bopimo_Disappearing_Block(
        color=SECTION_THREE_COLOR,
        position=turtle_pos,
        scale=Vector3(PLATFORM_SIZE / 2, 2, PLATFORM_SIZE / 2),
    )
    platform.disappears_after = 0.5
    level.add_object(platform)
    turtle_pos += Vector3(0, 0, (PLATFORM_SIZE / 2 + GAP_SIZE))
```

Perfect. That completes part two. For this last part, we're going to be granting the player a temporary speed boost to help them overcome a more difficult section. But before we can start, we need to reset our altitude back to normal. Let's get a little creative with this. We're going to make the player perform a long jump to get to this next part.

Now, calculating for this value is unfortunately gonna have to involve using a magic number. I had to playtest in the offline client to get this value, but I will be shifting the turtle 114 units, and I will reverse the upwards movement that was imposed earlier.

```python
turtle_pos += Vector3(0, -spring.bounce_force * 2 / 3 + 25, 114)

platform = Bopimo_Block(
    color=SECTION_THREE_COLOR,
    position=turtle_pos,
    scale=Vector3(PLATFORM_SIZE, 2, PLATFORM_SIZE),
)
```

Now, let's add our speed boost panel. The speed boost panel is what is going to grant our players a temporary speed boost. We'll be using `Bopimo_Speed_Panel` to pull this off. I'm going to not only make it bigger than default, but I'm also going to be tweaking some of the usual attributes. I think the default attributes are a bit too tame for what we're trying to achieve. Instead of a `new_speed` of 30, we will give a speed of 50. And instead of having a `duration` of 10 seconds, let's increase it to 15 seconds. We're going to be positioning this relative to the newly created platform. Every one of these modifications can be quickhanded, so we don't even need to declare a new variable.

```python
level.add_object(
    Bopimo_Speed_Panel(
        position=platform.position + Vector3(0, 1.5, 0),
        scale=Vector3(5, 1, 5),
        speed=50,
        duration=15,
    )
)
```

Great! Now we're going to conclude this last section by having some lengthy rotating platforms. Again, without the speed boost, this section can be quite challenging to pass because of centrifugal force. I'm going to set up the constants and decrease the `platform_length` variable so that the centrifugal force is not too difficult. We're going to be setting 5 of these spinning platforms, which if the player can navigate quickly enough, should last their entire speed boost. 

```python
platform_length = 150
ROTATION_SPEED = 45
turtle_pos += Vector3(
    0, 0, PLATFORM_SIZE / 2 + platform_length / 2 + GAP_SIZE
)
```

Normally, to help distinguish the platforms, I would inverse the rotation speed and have it spin opposing directions. However, I'm going to differentiate the platforms instead by giving a rotation offset, so that the player can more easily jump from one platform to another. We're going to end off the section (and the whole course) by having the player jump into a cannon that will get us our star. Now to make the ending a bit more fair in the event the boost runs out, we're going to make sure that the cannon is separated by just `GAP_SIZE` and have the player use the final platform to jump into the cannon. This is gonna be pulled off by pushing back the turtle after our for loop. So we should now have the following for loop.

```python
for i in range(0, 5):
    platform = Bopimo_Block(
        color=SECTION_THREE_COLOR,
        position=turtle_pos,
        rotation=Vector3(0, 90 * i, 0),
        scale=Vector3(PLATFORM_SIZE, 2, platform_length),
    )
    platform.rotation_enabled = True
    platform.rotation_direction = Vector3.up(*platform.rotation.to_radians())
    platform.rotation_speed = ROTATION_SPEED
    level.add_object(platform)
    turtle_pos += Vector3(0, 0, (platform_length + GAP_SIZE))
turtle_pos -= Vector3(0, 0, platform_length / 2)
```

## Wrapping Up The Level

Now it's time for us to create the ending for our level. For simplicity sake, we're going to make the ending part of the section three code so that we don't have worry about linking the ending separately. First, we're going to create a `Bopimo_Cannon` that is going to propel us to our star. We're going to modify a couple of things to this cannon:

- We're going to fine tune the rotation to (45, 0, 0), so our cannon will be facing 45 degrees upwards and gives us a direction for where we'll be propelling the player
- We're going to increase the size of the cannon, as the default size is pretty small and will be harder to aim from a moving platform. For the sake of avoiding magic numbers, I'm going to have this be a third of the size of a platform.
- We're going to increase the `power` of the cannon, so that the cannon will propel us further than the default value of 50. We're going to choose a value of 150.

Fortunately, all of these things can be quickhanded, but we're still going to be making a variable for this object because we will be referencing its position.

```python
cannon = Bopimo_Cannon(
    position=turtle_pos,
    rotation=Vector3(45, 0, 0),
    scale=Vector3(PLATFORM_SIZE / 3, PLATFORM_SIZE / 3, PLATFORM_SIZE / 3),
    power=150,
)
level.add_object(cannon)
```

> [!NOTE]
> This next section involves having to playtest the level to get a proper value. While I will try and add methods in the future to remove the guesswork, this is the best way to position things according to a projectory.

Now, it's time to finally create our star. Using `Bopimo_Completion_Star`, we can add a star for our player to collect and win the level. We're going to be positioning the star relatively to our cannon, using a calculated offset that should resemble the peak of the cannon trajectory. While we could put the star on our final platform instead, this method formalizes that the player has to use the cannon to retrieve the star. In addition, we're going to increase the size of the star, not only to reduce margins of error, but to help make it more visible for the player.

```python
STAR_OFFSET = Vector3(0, 56, 109)
STAR_SIZE = 7
level.add_object(
    Bopimo_Completion_Star(
        position=cannon.position + STAR_OFFSET,
        scale=Vector3(STAR_SIZE, STAR_SIZE, STAR_SIZE),
    )
)
```

Last, but not least, we need to create a landing platform that will serve as our final spot after the player has completed the level. We'll keep things simple by mimicking a baseplate form, and positioning a `Bopimo_Pine_Tree` in the center for not only aesthetic purposes, but to also catch the player rolling onto the baseplate. In contrast to our starting platform which is meant to resemble sand, we'll stick to the defaults for this one and go for a grassy feel.

Similar to the star, this baseplate will be positioned relatively to the cannon. The tree will be positioned relative to the baseplate.
```python
PLATE_OFFSET = Vector3(0, 0, 250)
PLATE_SIZE = 75
plate = Bopimo_Block(
    shape=Shape.CYLINDER,
    position=cannon.position + PLATE_OFFSET,
    scale=Vector3(PLATE_SIZE, 2, PLATE_SIZE),
)
level.add_object(plate)
level.add_object(
    Bopimo_Pine_Tree(position=plate.position + Vector3(0, 6, 0))
)
```

Our level is now finally complete! Now, the final step that we'll need to do is take *all* of the section three and ending code and put it into its own function. I'm sure you should know how this goes. The main difference is that instead of using a `Vector3` to parameterize the starting position, I actually give a starting `Bopimo_Object` as the turtle requires some size information to properly calculate its starting position.

With that in mind, all I have to do is reference `last_block` in our main function and feed it to the function as an argument
```python
level.add_objects(section_three(last_block))
```

## Exporting Our Level And Playtesting

> [!TIP]
> While I waited until the end to talk about this, it is recommended that you do this often while making your level so that you can ensure your level doesn't have any bugs and that your level is at a proper difficulty. Doing so is following [incremental development](https://en.wikipedia.org/wiki/Incremental_build_model), an essential skill to programming.

> [!WARNING]
> Exporting a level by default will overwrite any previously generated file with the same name. If you want to be able to revert to old versions of your level, you can either utilize undo history or hook up your script with version control software such as [git](https://en.wikipedia.org/wiki/Git) and set up a basic repository to formalize changes through commits.

We have spent all of this time writing code for our level, but we still do not have a playable level that we can launch. To get Bopymo to generate a final `bopjson` file that we can load and play, we need to take our `Bopimo_Level` object and translate it to `bopjson`. This can easily be done through the dedicated `export` method. By abstracting the translation away to a single method, you do not have to worry about programming the IO or knowing how to convert to JSON, as Bopymo will translate your code for you and handle the IO. 

All that you need to do is give a string value that represents a file name, or a file path including the file name (without the extension). **The file name is not the same thing as the level name** and they do not have to be the same, although it is recommended to make your exported file the same name as your script's file name so you can easily associate the generated level with its script. 

Since I decided to name my script `starter_guide.py`, I'm going to export the final level with the name "starter_guide"

```python
level.export("starter_guide")
```

And with just that one line of code, if I run my script using Python, I get a fully generated `bopjson` file that I can open with the Bopimo client and start playtesting! Make sure that you are happy with your progress and the changes made to your level, and if something is wrong, go back and fix it! If there is anything else you would like to add to this level or perform any modifications, feel free to do so and see what you can find!

**Be sure to include your export at the very end of your script, after all your level code.** Exporting your level before or during your level code will cause any Bopymo code after your export statement to not be translated and included in the final level.

# Finalizing Our Level And Publishing

Alright, now that we are completely done with our level, it's time for us to start tidying up the script so that we are not only following best programming practices, but also so our code will be much more legible.

## Additional Documentation

Even if you are not planning on sharing your script with others, one very important thing we should do is add more documentation to our code. We added the occasional comment or so while making the level, but it's best we go back and add more documentation. It's best that we not only keep our code clearly labelled and organized, but also help explain some more non-trivial snippets of code so that when you want to take your script and either update it, or fork it into a new script.

For my script, I added comments that label some sections of the main function (configuring the level and the highest-order level code). But I also went into the individual section functions and also decided to add comments for the various parts that we split up the sections into so it's easier to identify what part of the level the code is responsible for. If you would like to go the extra mile, you are more than welcome to write [Python docstrings](https://peps.python.org/pep-0257/) for the section functions and give a general overview of each section in plain English.

You'll want to find a nice balance between ensuring your code is well documented enough so you can read it, and making sure that you are not spending too much time documenting.

## Formalizing Our Imports

When we started our script, we used a star import to import everything into our level script. If you have managed to use an IDE that allows you to easily import classes and types on the fly, then you can skip this step.

But now, it's time that we replace the star import with proper imports. This will partially assist in the execution of the script by only giving the interpreter the classes and types we are using. Bopymo splits up its functionality into separate scripts that act as modules (e.g. the Bopimo object classes, the underlying types those classes utilize, or any additional utilities).

By removing the star import and replacing it with proper imports, our script should now only import these classes.

```python
# Type Hinting
from typing import List

# Types
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
```

## Adding Some Metadata

This is similar to adding more documentation, but we should also provide some quick metadata. One of the most useful ones includes what version of Bopymo this was written in. I will try and ensure that Bopymo scripts will remain compatible for future versions, but `bopjson` is a format that can often introduce breaking changes. The Bopimo Level Editor has backwards compatibility for older bopjson files, so your generated level will still import correctly in future versions. However, if Bopimo introduces breaking changes to their bopjson format and I don't have a viable way of preserving compatibility, I will have to break certain features to ensure Bopymo is up to date. By writing the Bopymo version, it'll be easier to identify breaking changes that may have occurred since the script was written and update the script to work with later Bopymo versions.

Similarly, write down what version of Python you are using. In the case the minimum Python version is updated, you can find similar changes in your scripts and update them to be conformant with a corresponding Python version.

## Publish Your Level

Once you have everything all finalized, make sure to generate your level one last time and ensure everything is still properly generated. Then, follow the appropriate procedures for publishing a level in Bopimo.

# Conclusion

By creating this basic obstacle course, we've gained a better understanding of the Bopymo wrapper and understanding how to make levels using it. 

Now there are several more object types that exist out there, but if you are struggling to understand what a class name is or what attributes that a class contains, you are more than welcome to look inside the modules to get an understanding of the various classes implemented. I have made sure to give docstrings for classes and their associated methods, so you can get an understanding of the class. I will be working on taking the docstrings and using them to generate a reference that you can use. However, that code is still yet to be made. 

Be sure to keep your Bopymo updated to either the latest commit in the `main` branch, or the latest point release if you want a more stable version of the wrapper. I am just one person maintaining this wrapper, so don't be afraid if it takes time for me to update the wrapper to any new Bopimo changes. You can refer to the releases page of the repository to keep up to date on any new changes regarding the wrapper and Bopimo features.

With that being said, I hope you enjoy using Bopymo and making your own levels!