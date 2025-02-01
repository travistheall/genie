from enum import StrEnum, IntEnum
import pandas as pd


class CleanNanEnum(IntEnum):

    @classmethod
    def clean(cls, value):
        if pd.isna(value):
            value = 0
        return cls(value)


class ShadowPurified(CleanNanEnum):
    normal = 0
    shadow = 1
    purified = 2


class Gender(StrEnum):
    male = "♂"
    female = "♀"
    unkown = "Unknown"

    @classmethod
    def clean(cls, value: str | None):
        if pd.isna(value) or value is None:
            value = "Unknown"

        _map = {
            "‚ôÇ": "♂",
            "‚ôÄ": "♀",
        }
        return cls(_map.get(value, value))


class PvpMark(StrEnum):
    gl = "G"
    gl_l = "g"
    ul = "U"
    ul_l = "u"
    lc = "L"
    lc_l = "l"


class Favorite(CleanNanEnum):
    none = 0
    high_iv = 1  # yellow
    gl_pvp = 2  # blue
    lc_pvp = 3  # green
    ul_pvp = 4  # orange
    ml_pvp = 5  # purple
    xxl = 6  # dark blue
    xxs = 7  # black


class FormEnum(StrEnum):
    alola = "Alola"
    altered = "Altered"
    aria = "Aria"
    armored = "Armored"
    attack = "Attack"
    average = "Average"
    baile = "Baile"
    chill = "Chill"
    complete = "Complete"
    dawn_wings = "Dawn Wings"
    defense = "Defense"
    dusk = "Dusk"
    dusk_mane = "Dusk Mane"
    female = "Female"
    four = "Four"
    galar = "Galar"
    hero = "Hero"
    hisui = "Hisui"
    land = "Land"
    large = "Large"
    male = "Male"
    mega = "Mega"
    midday = "Midday"
    midnight = "Midnight"
    none = "None"
    normal = "Normal"
    origin = "Origin"
    pau = "Pa'u"
    paldea = "Paldea"
    plant = "Plant"
    pom_pom = "Pom-Pom"
    rainy = "Rainy"
    roaming = "Roaming"
    sandy = "Sandy"
    sensu = "Sensu"
    shock = "Shock"
    sky = "Sky"
    small = "Small"
    snowy = "Snowy"
    speed = "Speed"
    sunny = "Sunny"
    super = "Super"
    therian = "Therian"
    three = "Three"
    trash = "Trash"

    @classmethod
    def clean(cls, value):
        if pd.isna(value):
            value = "None"
        return cls(value)
