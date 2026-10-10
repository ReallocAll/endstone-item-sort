from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SortResult:
    ok: bool
    changed_slots: int = 0
    error: str = ""
    fatal: bool = False


# The broad category order intentionally follows the shape used by mature
# inventory sorters such as ChestSort: combat/tools first, then consumables
# and resources, then building families, then uncategorised materials.
CATEGORY_WEAPONS = 0
CATEGORY_TOOLS = 1
CATEGORY_FOOD = 2
CATEGORY_VALUABLES = 3
CATEGORY_ARMOR = 4
CATEGORY_BREWING = 5
CATEGORY_REDSTONE = 6
CATEGORY_WOOD = 7
CATEGORY_STONE = 8
CATEGORY_PLANTS = 9
CATEGORY_BLOCKS = 10
CATEGORY_MATERIALS = 11
CATEGORY_MISC = 12


COLORS = (
    "white",
    "light_gray",
    "gray",
    "black",
    "brown",
    "red",
    "orange",
    "yellow",
    "lime",
    "green",
    "cyan",
    "light_blue",
    "blue",
    "magenta",
    "purple",
    "pink",
)
COLOR_RANK = {name: index for index, name in enumerate(COLORS)}

WOOD_SPECIES = (
    "oak",
    "spruce",
    "birch",
    "jungle",
    "acacia",
    "dark_oak",
    "mangrove",
    "cherry",
    "pale_oak",
    "bamboo",
    "crimson",
    "warped",
)
WOOD_RANK = {name: index for index, name in enumerate(WOOD_SPECIES)}

TIER_PREFIXES = (
    "netherite",
    "diamond",
    "golden",
    "gold",
    "iron",
    "copper",
    "stone",
    "wooden",
    "wood",
    "leather",
    "chainmail",
    "turtle",
)
TIER_RANK = {name: index for index, name in enumerate(TIER_PREFIXES)}

WEAPON_SUFFIXES = ("_sword", "_mace", "_spear")
WEAPON_NAMES = {"bow", "crossbow", "trident"}
TOOL_SUFFIXES = ("_pickaxe", "_axe", "_shovel", "_hoe")
TOOL_NAMES = {
    "shears",
    "fishing_rod",
    "flint_and_steel",
    "brush",
    "compass",
    "recovery_compass",
    "clock",
    "spyglass",
}
ARMOR_SUFFIXES = ("_helmet", "_chestplate", "_leggings", "_boots", "_horse_armor")
ARMOR_NAMES = {"elytra", "shield", "turtle_helmet", "wolf_armor"}

FOOD_NAMES = {
    "apple",
    "golden_apple",
    "enchanted_golden_apple",
    "bread",
    "beef",
    "cooked_beef",
    "porkchop",
    "cooked_porkchop",
    "chicken",
    "cooked_chicken",
    "mutton",
    "cooked_mutton",
    "rabbit",
    "cooked_rabbit",
    "cod",
    "cooked_cod",
    "salmon",
    "cooked_salmon",
    "tropical_fish",
    "pufferfish",
    "carrot",
    "golden_carrot",
    "potato",
    "baked_potato",
    "poisonous_potato",
    "beetroot",
    "beetroot_soup",
    "melon_slice",
    "sweet_berries",
    "glow_berries",
    "cookie",
    "cake",
    "pumpkin_pie",
    "mushroom_stew",
    "rabbit_stew",
    "suspicious_stew",
    "honey_bottle",
    "dried_kelp",
    "chorus_fruit",
}

VALUABLE_NAMES = {
    "coal",
    "charcoal",
    "raw_iron",
    "raw_gold",
    "raw_copper",
    "iron_ingot",
    "gold_ingot",
    "copper_ingot",
    "netherite_ingot",
    "netherite_scrap",
    "iron_nugget",
    "gold_nugget",
    "diamond",
    "emerald",
    "lapis_lazuli",
    "amethyst_shard",
    "quartz",
    "echo_shard",
    "ancient_debris",
}

BREWING_NAMES = {
    "potion",
    "splash_potion",
    "lingering_potion",
    "glass_bottle",
    "blaze_powder",
    "nether_wart",
    "fermented_spider_eye",
    "ghast_tear",
    "magma_cream",
    "sugar",
    "rabbit_foot",
    "glistering_melon_slice",
    "spider_eye",
    "phantom_membrane",
    "dragon_breath",
}

REDSTONE_NAMES = {
    "redstone",
    "repeater",
    "comparator",
    "observer",
    "piston",
    "sticky_piston",
    "lever",
    "tripwire_hook",
    "target",
    "hopper",
    "dispenser",
    "dropper",
    "note_block",
    "daylight_detector",
    "redstone_torch",
    "redstone_lamp",
    "sculk_sensor",
    "calibrated_sculk_sensor",
    "crafter",
}

WOOD_SUFFIXES = (
    "_log",
    "_wood",
    "_stem",
    "_hyphae",
    "_planks",
    "_slab",
    "_stairs",
    "_fence",
    "_fence_gate",
    "_door",
    "_trapdoor",
    "_button",
    "_pressure_plate",
    "_sign",
    "_hanging_sign",
    "_boat",
    "_chest_boat",
)

STONE_TOKENS = (
    "stone",
    "cobblestone",
    "deepslate",
    "andesite",
    "diorite",
    "granite",
    "tuff",
    "calcite",
    "basalt",
    "blackstone",
    "sandstone",
    "prismarine",
    "purpur",
    "quartz_block",
)

PLANT_TOKENS = (
    "sapling",
    "leaves",
    "flower",
    "tulip",
    "orchid",
    "dandelion",
    "poppy",
    "grass",
    "fern",
    "cactus",
    "sugar_cane",
    "bamboo",
    "seeds",
    "wheat",
    "pumpkin",
    "melon",
    "vine",
    "moss",
    "azalea",
    "mushroom",
    "lily",
    "kelp",
    "coral",
)

BLOCK_SUFFIXES = (
    "_block",
    "_bricks",
    "_brick",
    "_slab",
    "_stairs",
    "_wall",
    "_fence",
    "_fence_gate",
    "_door",
    "_trapdoor",
    "_glass",
    "_pane",
    "_wool",
    "_carpet",
    "_terracotta",
    "_concrete",
    "_concrete_powder",
)
BLOCK_NAMES = {
    "dirt",
    "coarse_dirt",
    "rooted_dirt",
    "grass_block",
    "podzol",
    "mycelium",
    "mud",
    "clay",
    "gravel",
    "sand",
    "red_sand",
    "netherrack",
    "soul_sand",
    "soul_soil",
    "end_stone",
    "obsidian",
    "crying_obsidian",
    "bedrock",
}

MATERIAL_NAMES = {
    "string",
    "gunpowder",
    "bone",
    "bone_meal",
    "rotten_flesh",
    "leather",
    "feather",
    "slime_ball",
    "spider_eye",
    "ender_pearl",
    "blaze_rod",
    "magma_cream",
    "ghast_tear",
    "phantom_membrane",
    "prismarine_shard",
    "prismarine_crystals",
    "nautilus_shell",
    "scute",
    "armadillo_scute",
    "ink_sac",
    "glow_ink_sac",
    "rabbit_hide",
    "rabbit_foot",
}


@dataclass(slots=True)
class _MergeGroup:
    items: list[Any]
    total: int
    max_stack: int


def item_id(item: Any) -> str:
    return str(item.type.id)


def item_name(item: Any) -> str:
    identifier = item_id(item)
    return identifier.split(":", 1)[-1].lower()


def is_bundle(item: Any) -> bool:
    identifier = item_id(item)
    if not identifier.startswith("minecraft:"):
        return False
    name = identifier.removeprefix("minecraft:")
    return name == "bundle" or name.endswith("_bundle")


def stack_equal(left: Any | None, right: Any | None) -> bool:
    if left is None or right is None:
        return left is None and right is None

    try:
        return (
            item_id(left) == item_id(right)
            and int(left.data) == int(right.data)
            and int(left.amount) == int(right.amount)
            and int(left.max_stack_size) == int(right.max_stack_size)
            and bool(left.is_similar(right))
        )
    except Exception:
        return False


def stacks_mergeable(left: Any, right: Any) -> bool:
    """Return whether two detached ItemStacks may be compacted together.

    Endstone 0.11 ItemStack.is_similar() compares type + item metadata but not
    the aux/data value, so data must be checked separately here.
    """

    try:
        return (
            item_id(left) == item_id(right)
            and int(left.data) == int(right.data)
            and int(left.max_stack_size) == int(right.max_stack_size)
            and int(left.max_stack_size) > 1
            and bool(left.is_similar(right))
            and bool(right.is_similar(left))
        )
    except Exception:
        return False


def _movable_stack(item: Any) -> bool:
    if is_bundle(item):
        return False
    try:
        amount = int(item.amount)
        maximum = int(item.max_stack_size)
        # Keep malformed / oversized custom stacks pinned. Repartitioning them
        # could silently destroy server-specific semantics.
        return maximum >= 1 and 1 <= amount <= maximum
    except Exception:
        return False


def _is_wood_item(name: str) -> bool:
    base = name[len("stripped_") :] if name.startswith("stripped_") else name
    for species in WOOD_SPECIES:
        prefix = species + "_"
        if base.startswith(prefix):
            remainder = base[len(prefix) :]
            if any(("_" + remainder).endswith(suffix) for suffix in WOOD_SUFFIXES):
                return True
    return name in {"bamboo_block", "stripped_bamboo_block", "bamboo_mosaic"}


def _category(name: str) -> int:
    if name in WEAPON_NAMES or name.endswith(WEAPON_SUFFIXES):
        return CATEGORY_WEAPONS
    if name in TOOL_NAMES or name.endswith(TOOL_SUFFIXES):
        return CATEGORY_TOOLS
    if name in FOOD_NAMES:
        return CATEGORY_FOOD
    if name in VALUABLE_NAMES or name.startswith("raw_") and name in {"raw_iron", "raw_gold", "raw_copper"}:
        return CATEGORY_VALUABLES
    if name in ARMOR_NAMES or name.endswith(ARMOR_SUFFIXES):
        return CATEGORY_ARMOR
    if name in BREWING_NAMES or name.endswith("_potion"):
        return CATEGORY_BREWING
    if name in REDSTONE_NAMES or name.endswith(("_button", "_pressure_plate")):
        return CATEGORY_REDSTONE
    if _is_wood_item(name):
        return CATEGORY_WOOD
    if any(token in name for token in STONE_TOKENS):
        return CATEGORY_STONE
    if any(token in name for token in PLANT_TOKENS):
        return CATEGORY_PLANTS
    if name in BLOCK_NAMES or name.endswith(BLOCK_SUFFIXES):
        return CATEGORY_BLOCKS
    if name in MATERIAL_NAMES:
        return CATEGORY_MATERIALS
    return CATEGORY_MISC


def _strip_color(name: str) -> tuple[str, int]:
    for color, rank in COLOR_RANK.items():
        prefix = color + "_"
        if name.startswith(prefix):
            return name[len(prefix) :], rank
    return name, len(COLOR_RANK)


def _wood_family(name: str) -> tuple[str, int]:
    # Treat wood species like ChestSort treats its color/wood secondary key:
    # group all logs together, all planks together, etc., then order species.
    stripped = name
    if stripped.startswith("stripped_"):
        stripped = stripped[len("stripped_") :]
        stripped_suffix = "_stripped"
    else:
        stripped_suffix = ""

    for species, rank in WOOD_RANK.items():
        prefix = species + "_"
        if stripped.startswith(prefix):
            family = stripped[len(prefix) :] + stripped_suffix
            return family, rank
        marker = "_" + species + "_"
        if marker in stripped:
            family = stripped.replace(marker, "_", 1) + stripped_suffix
            return family, rank

    if name.startswith("bamboo_"):
        return name[len("bamboo_") :], WOOD_RANK["bamboo"]
    return name, len(WOOD_RANK)


def _tier_family(name: str) -> tuple[str, int]:
    for tier, rank in TIER_RANK.items():
        prefix = tier + "_"
        if name.startswith(prefix):
            return name[len(prefix) :], rank
    return name, len(TIER_RANK)


def _family_key(name: str, category: int) -> tuple[str, int, int, str]:
    color_family, color_rank = _strip_color(name)

    if category == CATEGORY_WOOD:
        family, wood_rank = _wood_family(name)
        return family, wood_rank, color_rank, name

    if category in {CATEGORY_WEAPONS, CATEGORY_TOOLS, CATEGORY_ARMOR}:
        family, tier_rank = _tier_family(name)
        armor_order = {
            "helmet": 0,
            "chestplate": 1,
            "leggings": 2,
            "boots": 3,
            "horse_armor": 4,
        }
        slot_rank = next((rank for suffix, rank in armor_order.items() if family.endswith(suffix)), 99)
        return family, tier_rank, slot_rank, name

    # Group dye variants (wool, concrete, terracotta, etc.) by the base item,
    # with a predictable vanilla-like color sequence as the secondary key.
    if color_family != name:
        return color_family, color_rank, 0, name

    # Keep polished variants next to their base material rather than under P.
    if name.startswith("polished_"):
        base = name[len("polished_") :]
        return base, 1, 0, name

    if name == "wet_sponge":
        return "sponge", 1, 0, name
    if name == "carved_pumpkin":
        return "pumpkin", 1, 0, name

    return name, 0, 0, name


def stack_sort_key(item: Any) -> tuple[int, str, int, int, str, int]:
    name = item_name(item)
    category = _category(name)
    family, secondary, tertiary, fallback = _family_key(name, category)
    return category, family, secondary, tertiary, fallback, int(item.data)


def _compact(items: list[Any]) -> list[Any]:
    """Merge equivalent detached ItemStacks without constructing new stacks.

    Every output stack reuses one of the detached ItemStack copies returned by
    Inventory.get_item(). Because each input amount is <= max_stack_size, the
    number of output stacks can never exceed the number of inputs in a group.
    """

    groups: list[_MergeGroup] = []
    for item in items:
        match: _MergeGroup | None = None
        for group in groups:
            if stacks_mergeable(group.items[0], item):
                match = group
                break
        if match is None:
            groups.append(
                _MergeGroup(
                    items=[item],
                    total=int(item.amount),
                    max_stack=int(item.max_stack_size),
                )
            )
        else:
            match.items.append(item)
            match.total += int(item.amount)

    compacted: list[Any] = []
    for group in groups:
        total = group.total
        maximum = group.max_stack
        needed = (total + maximum - 1) // maximum
        for index in range(needed):
            item = group.items[index]
            amount = min(maximum, total)
            item.amount = amount
            compacted.append(item)
            total -= amount
        if total != 0:
            raise RuntimeError("internal compaction accounting mismatch")

    return compacted


def sort_inventory(inventory: Any, first_slot: int, last_slot: int) -> SortResult:
    """Compact and sort a contiguous inventory range using public APIs only.

    Safety model:
    - snapshot the complete target range before any write;
    - pin bundles, malformed stacks and oversized stacks in place;
    - obtain a second detached copy for every movable item before mutating count;
    - abort if the second read differs from the snapshot;
    - compact only strict type/data/metadata-compatible stacks;
    - sort by category/family while keeping stable metadata order;
    - write only changed movable slots;
    - verify all changed slots and roll back the full range on any failure.
    """

    try:
        size = int(inventory.size)
    except Exception as exc:
        return SortResult(False, error=f"无法读取背包大小：{exc}")

    if size <= 0:
        return SortResult(False, error="背包大小无效")

    first = max(0, int(first_slot))
    last = min(int(last_slot), size - 1)
    if first > last:
        return SortResult(False, error="没有可整理的槽位")

    originals: dict[int, Any | None] = {}
    try:
        for slot in range(first, last + 1):
            originals[slot] = inventory.get_item(slot)
    except Exception as exc:
        return SortResult(False, error=f"读取物品失败，未进行任何修改：{exc}")

    writable_slots: list[int] = []
    work_items: list[Any] = []
    try:
        for slot in range(first, last + 1):
            original = originals[slot]
            if original is not None and not _movable_stack(original):
                continue

            writable_slots.append(slot)
            if original is None:
                continue

            # get_item() returns an independent Endstone ItemStack copy. Read a
            # second copy so the rollback snapshot is never mutated by merging.
            work = inventory.get_item(slot)
            if not stack_equal(original, work):
                return SortResult(False, error=f"槽位 {slot} 在整理前发生变化，未进行任何修改")
            work_items.append(work)

        movable = _compact(work_items)
        movable.sort(key=stack_sort_key)
    except Exception as exc:
        return SortResult(False, error=f"物品信息无法安全整理，未进行任何修改：{exc}")

    if len(movable) > len(writable_slots):
        # This should be impossible: compaction never increases stack count.
        return SortResult(False, error="整理结果超出可用槽位，未进行任何修改")

    expected: dict[int, Any | None] = {}
    for index, slot in enumerate(writable_slots):
        expected[slot] = movable[index] if index < len(movable) else None

    changed = [slot for slot in writable_slots if not stack_equal(originals[slot], expected[slot])]
    if not changed:
        return SortResult(True, changed_slots=0)

    def rollback() -> bool:
        ok = True
        for slot in range(first, last + 1):
            try:
                inventory.set_item(slot, originals[slot])
            except Exception:
                ok = False
        return ok

    try:
        # Remove every changed source first. This prevents a moved stack from
        # existing in both its old and new slot, even transiently, while the
        # transaction is being applied on the server thread.
        for slot in changed:
            inventory.set_item(slot, None)

        for slot in changed:
            if expected[slot] is not None:
                inventory.set_item(slot, expected[slot])

        for slot in changed:
            actual = inventory.get_item(slot)
            if not stack_equal(expected[slot], actual):
                restored = rollback()
                return SortResult(
                    False,
                    error=(
                        f"槽位 {slot} 写入后校验失败，"
                        + ("已恢复原内容" if restored else "且回滚未完全成功")
                    ),
                    fatal=True,
                )
    except Exception as exc:
        restored = rollback()
        return SortResult(
            False,
            error=f"写入失败：{exc}；" + ("已恢复原内容" if restored else "回滚未完全成功"),
            fatal=True,
        )

    return SortResult(True, changed_slots=len(changed))
