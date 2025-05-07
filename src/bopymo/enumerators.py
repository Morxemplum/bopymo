from enum import IntEnum


class Block_ID(IntEnum):
    """
    Bopimo differentiates their objects through a numeric ID. This enum makes
    it easy to see what the different IDs for objects are. Cube should be the
    default, but invalid IDs will be resolved to NULL (-1)
    """

    NULL = -1

    PRIMITIVE = 0

    # DECORATION
    PINE_TREE = 1000
    LOGO = 1002
    LOGO_ICON = 1003
    PALM_TREE = 1004
    STREET_LAMP = 1005
    FLOWER = 1006
    FENCE = 1007
    TORCH = 1008
    STRING_LIGHTS = 1009
    ROSE = 1014
    TREE = 1015
    CORNSTALK = 1016

    MESH = 1100
    CLOUD = 1101
    STATUE = 1102

    # ACTION
    SPRING = 2000
    WATER = 2001
    SPAWN = 2002
    CHECKPOINT = 2003
    TOKEN = 2004
    LADDER = 2005
    ICE = 2006
    COMPLETION_STAR = 2007
    MAGMA = 2008
    BOOST_PANEL = 2009
    SPEED_PANEL = 2010
    GRATES = 2011
    DISAPPEARING_BLOCK = 2012
    MISSILE_LAUNCHER = 2013
    BREAKABLE_BLOCK = 2014
    CANNON = 2015
    PORTAL = 2016
    DIALOGUE_SIGN = 2019
    WEB = 2025
    NOTE_BLOCK = 2026
    LEVEL_PAINTING = 2027

    # NPC
    BOPI_SPAWNER = 3000

    # HIDDEN
    HYACINTH = 1010
    ANALOG_CLOCK = 1012
    GLOOMLIGHT_SPAWNER = 3100
    ITEM_GRANTER = 60000
    BLEEDING_EYE = 61366

    # DEPRECATED
    LAVA = 2008  # Old alias for Magma


class Shape(IntEnum):
    """
    Since Bopimo 1.1.0, primitives all share the same Block ID and are uniquely
    identified through a "shape" attribute. This enum outlines the different
    shape values that are associated with primitives
    """

    CUBE = 0
    RAMP = 1
    CYLINDER = 2
    HALF_CYLINDER = 3
    QUARTER_CYLINDER = 4
    SPHERE = 5
    HALF_SPHERE = 6
    CORNER_RAMP = 7
    CONE = 8
    TORUS = 9
    THIN_TORUS = 10
    TETRAHEDRON = 11
    PYRAMID = 12
    PYRAMID_CORNER = 13
    OCTAHEDRON = 14
    ROUNDED_RAMP = 15
    INVERTED_ROUNDED_RAMP = 16
    HOLLOW_CYLINDER = 17
    HALF_HOLLOW_CYLINDER = 18
    QUARTER_HOLLOW_CYLINDER = 19
    HOLE = 20
    ARCH = 21
    HALF_ARCH = 22
    PENTAGON = 23
    HEXAGON = 24
    HEPTAGON = 25
    OCTAGON = 26
    STAR = 27
    HEART = 28
    OPEN_CRESCENT = 29
    CLOSING_CRESCENT = 30
    EGG = 31
    LOOP = 32


class Block_Pattern(IntEnum):
    """
    Bopimo objects with patterns will represent their patterns use a numeric
    ID. By default, objects will use the checkerboard pattern (0).

    If you are aiming for no pattern, the easiest way to do so is by matching
    the pattern color with the block color or by setting pattern opacity to 0.
    """

    CHECKERBOARD = 0
    HEX = 1
    STRIPES = 2
    PLANKS = 3
    ZIG_ZAG = 4
    BRICKS = 5
    LARGE_BRICKS = 6
    WAVES = 7
    CHEVRON = 8
    GEOMETRIC = 9
    HORIZONTAL_STRIPES = 10
    VERTICAL_STRIPES = 11
    X = 12
    PLATE = 13
    RADIAL = 14
    ARROW = 15
    CIRCLES = 16
    EVEN_CIRCLES = 17
    MESSY_CIRCLES = 18
    SQUARES = 19
    EVEN_SQUARES = 20
    MESSY_SQUARES = 21
    TRIANGLES = 22
    EVEN_TRIANGLES = 23
    MESSY_TRIANGLES = 24
    DIAMONDS = 25
    ODD_DIAMONDS = 26
    MESSY_DIAMONDS = 27
    LARGE_DIAMONDS = 28
    STARS = 29
    EVEN_STARS = 30
    MESSY_STARS = 31
    HEARTS = 32
    EVEN_HEARTS = 33
    MESSY_HEARTS = 34
    NOTE = 35
    BEAMED_NOTE = 36


class Sky(IntEnum):
    """
    Bopimo offers various different skyboxes that help set the basic atmosphere
    for the level. This is represented by a numeric ID and this contains all
    of the skyboxes you can choose from.
    """

    DAY = 0
    SUNSET = 1
    NIGHT = 2
    RAINDROP = 3
    ALIEN = 4
    DULL = 5
    WINTER = 6
    INFERNAL = 7
    FLAME = 8
    GOLDEN = 9
    VIOLET = 10
    THE_SUN = 11
    HALLOWEEN = 12
    OVERCAST = 13
    STARLIT_CITY = 14
    VOID = 15
    DESERT = 16
    FAR_GONE = 17
    SUNKEN = 18
    EGGSTAR = 19
    BLOOM = 20
    DEPENDENCE = 21
    RAPTURE = 22
    WASTES = 23


class Weather(IntEnum):
    """
    You can introduce weather into your Bopimo level to enhance the atmosphere
    of the level. This enum contains all of the different types of weather you
    can choose from. By default, there will be no weather (CLEAR)
    """

    CLEAR = 0
    SNOW = 1
    RAIN = 2
    VOID = 3
    AUTUMN = 4


class Sound(IntEnum):
    """
    Typically reserved for Note Blocks, this enum focuses on all of the sound
    IDs that are contained within Bopimo. This includes all the instruments,
    and sounds that are not readily accessible with the Bopimo level editor.

    Keep in mind that when using a Sound value outside of the intended
    instruments, the pitch may not be aligned and needs to be adjusted.
    In addition, sounds that loop will continue looping after the sound
    is emitted.
    """

    SPRING = 0
    TOKEN = 2
    SPLASH = 3
    DISAPPEAR = 4
    CANNON_ENTER = 5
    FIREWORKS = 7  # Used in the New Year's celebration
    PORTAL_ENTER = 9
    PORTAL_EXIT = 10
    STAR_COLLECT = 15

    # LOOPING SOUNDS

    COMPLETION_STAR = 1
    NOTE_LOOP = 6
    PORTAL_AMBIENCE = 8

    # INSTRUMENTS

    PIANO = 11
    CHORD = 12
    SYNTH = 13
    VIOLA = 14


class Music(IntEnum):
    """
    Bopimo has its own unique soundtrack that is produced by the developers.
    This enum gives you all of the different song names and their associated
    numeric IDs.
    """

    SERENE = 0
    SWAYING_DREAMS = 1
    PLAYFUL_WALTZ = 2
    SICILIAN_STREET = 3
    CONTEMPLATION = 4
    CAVE_AMBIENCE = 5
    FUNKY = 6
    DARKNESS_APPROACHES = 7
    CARNIVAL = 8
    LATE_NIGHT_FIREWORKS = 9
    I_DONT_KNOW = 10
    WINTER_FOREST = 11
    ASSAULT_ON_THE_EAR_DRUMS = 12
    BLOOD_MOON = 13
    ORGAN = 14
    BAMBA = 15
    TORTUGA = 16
    FRIVOLOUS_FLUTES = 17
    PEACEFUL = 18
    SIXTY_FOUR = 64

    # OLD NAMES
    ISAIAH_NEW_SONG = 14


class Decal_Type(IntEnum):
    """
    Decal uploaders will often upload their textures in three popular formats.
    The two major articles of clothing, shirts and pants, both have their own
    pros and cons.

    Shirts will have a better pixel resolution and should be the case if
    resolution is important. However, be careful with the corners, as the
    corners will warp in the final decal.

    Pants have significantly less warping artifacts, but they will have a lower
    resolution. In addition, there are two variants of pants decals, depending
    on which leg the decal maker chooses to put their texture. Make sure to
    select the appropriate leg so the transformations will apply correctly.
    """

    SHIRT = 0
    PANTS_FRONT_LEFT = 1  # Left Leg
    PANTS_FRONT_RIGHT = 2  # Right Leg


class Grates_Style(IntEnum):
    """
    Since Bopimo 1.1.0, Grates now have a variety of textures that can be
    applied to give them a different look. These are exclusive to the Grates
    block and can't be applied to other blocks.
    """

    GRID = 0
    X = 1
    BOX = 2
    ROUNDED_BOX = 3
    TILES = 4
    OVERLAPPING_TILES = 5
