from enum import IntEnum

class Block_ID(IntEnum):
    """
    Bopimo differentiates their objects through a numeric ID. This enum makes
    it easy to see what the different IDs for objects are. Cube should be the
    default, but invalid IDs will be resolved to NULL (-1)
    """

    NULL = -1

    # PRIMITIVES
    CUBE = 0
    RAMP = 1
    CYLINDER = 2
    SPHERE = 5
    CORNER_RAMP = 7
    CONE = 8
    PYRAMID = 12
    PYRAMID_CORNER = 13
    ROUNDED_RAMP = 15
    HOLE = 20
    ARCH = 21
    HALF_ARCH = 22
    LOOP = 32

    # DECORATION
    PINE_TREE = 1000
    PINE_TREE_SNOW = 1001
    LOGO = 1002
    LOGO_ICON = 1003
    PALM_TREE = 1004
    STREET_LAMP = 1005
    FLOWER = 1006
    FENCE = 1007
    TORCH = 1008
    STRING_LIGHTS = 1009
    ROSE = 1014
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
    LAVA = 2008
    BOOST_PANEL = 2009
    SPEED_PANEL = 2010
    GRATES = 2011
    DISAPPEARING_BLOCK = 2012
    MISSILE_LAUNCHER = 2013
    BREAKABLE_BLOCK = 2014
    CANNON = 2015
    PORTAL = 2016
    WEB = 2025

    # NPC
    BOPI_SPAWNER = 3000

    # HIDDEN
    HYACINTH = 1010
    ANALOG_CLOCK = 1012
    GLOOMLIGHT_SPAWNER = 3100
    ITEM_GRANTER = 60000
    BLEEDING_EYE = 61366


class Block_Pattern(IntEnum):
    """
    Bopimo objects with patterns will represent their patterns use a numeric
    ID. By default, objects will use the checkerboard pattern (0).

    If you are aiming for no pattern, the easiest way to do so is by matching
    the pattern color with the block color.
    """

    CHECKERBOARD = 0
    HEX = 1
    STRIPES = 2
    PLANKS = 3
    ZIG_ZAG = 4
    CIRCLES = 5
    DIAMONDS = 6
    LARGE_DIAMONDS = 7
    BRICKS = 8
    LARGE_BRICKS = 9
    WAVES = 10
    CHEVRON = 11
    GEOMETRIC = 12
    HORIZONTAL_STRIPES = 13
    VERTICAL_STRIPES = 14
    X = 15
    HEARTS = 17


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
    ISAIAH_NEW_SONG = 14
    BAMBA = 15
    TORTUGA = 16
    FRIVOLOUS_FLUTES = 17
    SIXTY_FOUR = 64

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