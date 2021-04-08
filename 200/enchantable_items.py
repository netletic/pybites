from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Dict
from typing import List
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup

out_dir = "/tmp"
html_file = f"{out_dir}/enchantment_list_pc.html"

HTML_FILE = Path(html_file)
# source:
# https://www.digminecraft.com/lists/enchantment_list_pc.php
URL = "https://bites-data.s3.us-east-2.amazonaws.com/minecraft-enchantment.html"

LAZY_ROMAN = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
}


@dataclass(order=True)
class Enchantment:
    """Minecraft enchantment class

    Implements the following:
        id_name, name, max_level, description, items
    """

    id_name: str
    name: str
    max_level: int
    description: str
    items: List[str] = field(default_factory=list)

    def __str__(self):
        return f"{self.name.title()} ({self.max_level}): {self.description}"


@dataclass
class Item:
    """Minecraft enchantable item class

    Implements the following:
        name, enchantments
    """

    name: str
    enchantments: List[Enchantment] = field(default_factory=list)

    @property
    def title_name(self):
        return self.name.replace("_", " ").title()

    def __str__(self):
        res = ""
        res += f"{self.title_name}: \n"
        for ench in sorted(self.enchantments):
            res += f"  [{ench.max_level}] {ench.id_name}\n"
        return res


def clean_item_link(item_link: str) -> List[str]:
    unwanted = [".", "enchanted", "iron", "png", "sm"]
    for chars in unwanted:
        item_link = item_link.replace(chars, "")

    *_, item_names = item_link.split("/")

    item_names = item_names.replace("fishing_rod", "fishing*rod")
    item_names = item_names.strip("_")
    items = [item.replace("*", "_") for item in item_names.split("_")]

    return items


def generate_enchantments(soup):
    """Generates a dictionary of Enchantment objects

    With the key being the id_name of the enchantment.
    """
    rows = soup.find("table", {"id": "minecraft_items"})("tr")[1:]
    enchants = {}
    for row in rows:
        data = row("td")

        name, id_name = data[0].text.rstrip(")").split("(")
        max_level = LAZY_ROMAN[data[1].text]
        desc = data[2].text
        items = clean_item_link(data[4].img["data-src"])

        enchant = Enchantment(id_name, name, max_level, desc, items)
        enchants[id_name] = enchant

    return enchants


def generate_items(data: Dict[str, Enchantment]):
    """Generates a dictionary of Item objects

    With the key being the item name.
    """
    items = defaultdict(list)
    for enchant in data.values():
        for item in enchant.items:
            items[item].append(enchant)

    return {item: Item(item, enchantments) for item, enchantments in items.items()}


def get_soup(file=HTML_FILE):
    """Retrieves/takes source HTML and returns a BeautifulSoup object"""
    if isinstance(file, Path):
        if not HTML_FILE.is_file():
            urlretrieve(URL, HTML_FILE)

        with file.open() as html_source:
            soup = Soup(html_source, "html.parser")
    else:
        soup = Soup(file, "html.parser")

    return soup


def main():
    """This function is here to help you test your final code.

    Once complete, the print out should match what's at the bottom of this file"""
    soup = get_soup()
    enchantment_data = generate_enchantments(soup)
    minecraft_items = generate_items(enchantment_data)
    for item in minecraft_items:
        print(minecraft_items[item], "\n")


if __name__ == "__main__":
    main()

"""
Armor:
  [1] binding_curse
  [4] blast_protection
  [4] fire_protection
  [4] projectile_protection
  [4] protection
  [3] thorns

Axe:
  [5] bane_of_arthropods
  [5] efficiency
  [3] fortune
  [5] sharpness
  [1] silk_touch
  [5] smite

Boots:
  [3] depth_strider
  [4] feather_falling
  [2] frost_walker

Bow:
  [1] flame
  [1] infinity
  [5] power
  [2] punch

Chestplate:
  [1] mending
  [3] unbreaking
  [1] vanishing_curse

Crossbow:
  [1] multishot
  [4] piercing
  [3] quick_charge

Fishing Rod:
  [3] luck_of_the_sea
  [3] lure
  [1] mending
  [3] unbreaking
  [1] vanishing_curse

Helmet:
  [1] aqua_affinity
  [3] respiration

Pickaxe:
  [5] efficiency
  [3] fortune
  [1] mending
  [1] silk_touch
  [3] unbreaking
  [1] vanishing_curse

Shovel:
  [5] efficiency
  [3] fortune
  [1] silk_touch

Sword:
  [5] bane_of_arthropods
  [2] fire_aspect
  [2] knockback
  [3] looting
  [1] mending
  [5] sharpness
  [5] smite
  [3] sweeping
  [3] unbreaking
  [1] vanishing_curse

Trident:
  [1] channeling
  [5] impaling
  [3] loyalty
  [3] riptide
"""
