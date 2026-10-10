from __future__ import annotations

import copy
import unittest
from dataclasses import dataclass

from endstone_item_sort.sorter import is_bundle, sort_inventory, stack_sort_key


@dataclass
class FakeType:
    id: str


@dataclass
class FakeItem:
    identifier: str
    amount: int = 1
    data: int = 0
    meta: str = ""
    max_stack_size: int = 64

    @property
    def type(self) -> FakeType:
        return FakeType(self.identifier)

    def is_similar(self, other: "FakeItem") -> bool:
        # Deliberately mirror Endstone 0.11: data is *not* part of
        # is_similar(), so sorter.py must check it explicitly.
        return self.identifier == other.identifier and self.meta == other.meta


class FakeInventory:
    def __init__(self, items: list[FakeItem | None]):
        self.items = copy.deepcopy(items)
        self.fail_on_set: int | None = None
        self.corrupt_on_set: int | None = None
        self.mutate_on_second_read: int | None = None
        self.read_counts: dict[int, int] = {}

    @property
    def size(self) -> int:
        return len(self.items)

    def get_item(self, slot: int):
        self.read_counts[slot] = self.read_counts.get(slot, 0) + 1
        value = copy.deepcopy(self.items[slot])
        if self.mutate_on_second_read == slot and self.read_counts[slot] == 2 and value is not None:
            value.amount += 1
        return value

    def set_item(self, slot: int, item):
        if self.fail_on_set == slot:
            self.fail_on_set = None
            raise RuntimeError("injected write failure")
        value = copy.deepcopy(item)
        if self.corrupt_on_set == slot and value is not None:
            self.corrupt_on_set = None
            value.amount += 1
        self.items[slot] = value


class SorterTests(unittest.TestCase):
    def test_main_inventory_range_does_not_touch_hotbar(self):
        hotbar = [FakeItem(f"minecraft:hotbar_{i}") for i in range(9)]
        main = [FakeItem("minecraft:stone"), FakeItem("minecraft:apple"), None]
        inv = FakeInventory(hotbar + main)

        result = sort_inventory(inv, 9, 11)

        self.assertTrue(result.ok)
        self.assertEqual([x.identifier for x in inv.items[:9]], [f"minecraft:hotbar_{i}" for i in range(9)])
        self.assertEqual(inv.items[9].identifier, "minecraft:apple")
        self.assertEqual(inv.items[10].identifier, "minecraft:stone")
        self.assertIsNone(inv.items[11])

    def test_bundle_is_pinned(self):
        inv = FakeInventory(
            [
                FakeItem("minecraft:stone"),
                FakeItem("minecraft:red_bundle", meta="contents", max_stack_size=1),
                FakeItem("minecraft:apple"),
            ]
        )

        result = sort_inventory(inv, 0, 2)

        self.assertTrue(result.ok)
        self.assertTrue(is_bundle(inv.items[1]))
        self.assertEqual(inv.items[1].meta, "contents")
        self.assertEqual(inv.items[0].identifier, "minecraft:apple")
        self.assertEqual(inv.items[2].identifier, "minecraft:stone")

    def test_merge_partial_stacks_and_free_slots(self):
        inv = FakeInventory(
            [
                FakeItem("minecraft:iron_ingot", amount=32),
                FakeItem("minecraft:iron_ingot", amount=40),
                FakeItem("minecraft:iron_ingot", amount=64),
                None,
            ]
        )

        result = sort_inventory(inv, 0, 3)

        self.assertTrue(result.ok)
        stacks = [item for item in inv.items if item is not None]
        self.assertEqual([item.amount for item in stacks], [64, 64, 8])
        self.assertIsNone(inv.items[3])

    def test_metadata_variants_are_never_merged(self):
        inv = FakeInventory(
            [
                FakeItem("minecraft:stone", amount=20, meta="named-b"),
                FakeItem("minecraft:stone", amount=40, meta="named-a"),
                FakeItem("minecraft:stone", amount=30, meta="named-b"),
            ]
        )

        result = sort_inventory(inv, 0, 2)

        self.assertTrue(result.ok)
        by_meta = [(item.meta, item.amount) for item in inv.items if item is not None]
        self.assertEqual(by_meta, [("named-b", 50), ("named-a", 40)])
        self.assertIsNone(inv.items[2])

    def test_different_data_values_are_never_merged_even_if_is_similar(self):
        inv = FakeInventory(
            [
                FakeItem("minecraft:test_variant", amount=30, data=0, meta="same"),
                FakeItem("minecraft:test_variant", amount=40, data=1, meta="same"),
            ]
        )

        result = sort_inventory(inv, 0, 1)

        self.assertTrue(result.ok)
        self.assertEqual([(item.data, item.amount) for item in inv.items], [(0, 30), (1, 40)])

    def test_unstackable_items_are_reordered_but_not_merged(self):
        inv = FakeInventory(
            [
                FakeItem("minecraft:stone", amount=1),
                FakeItem("minecraft:diamond_pickaxe", amount=1, max_stack_size=1),
                FakeItem("minecraft:diamond_pickaxe", amount=1, max_stack_size=1),
            ]
        )

        result = sort_inventory(inv, 0, 2)

        self.assertTrue(result.ok)
        self.assertEqual(inv.items[0].identifier, "minecraft:diamond_pickaxe")
        self.assertEqual(inv.items[1].identifier, "minecraft:diamond_pickaxe")
        self.assertEqual(inv.items[2].identifier, "minecraft:stone")

    def test_oversized_stack_is_pinned(self):
        inv = FakeInventory(
            [
                FakeItem("minecraft:stone", amount=80, max_stack_size=64),
                FakeItem("minecraft:apple", amount=1),
                FakeItem("minecraft:dirt", amount=1),
            ]
        )

        result = sort_inventory(inv, 0, 2)

        self.assertTrue(result.ok)
        self.assertEqual(inv.items[0].identifier, "minecraft:stone")
        self.assertEqual(inv.items[0].amount, 80)
        self.assertEqual(inv.items[1].identifier, "minecraft:apple")
        self.assertEqual(inv.items[2].identifier, "minecraft:dirt")

    def test_category_sort_is_human_oriented(self):
        items = [
            FakeItem("minecraft:gunpowder", amount=10),
            FakeItem("minecraft:oak_log", amount=10),
            FakeItem("minecraft:redstone", amount=10),
            FakeItem("minecraft:iron_ingot", amount=10),
            FakeItem("minecraft:cooked_beef", amount=10),
            FakeItem("minecraft:iron_pickaxe", amount=1, max_stack_size=1),
            FakeItem("minecraft:diamond_sword", amount=1, max_stack_size=1),
            FakeItem("minecraft:iron_chestplate", amount=1, max_stack_size=1),
        ]
        ordered = sorted(items, key=stack_sort_key)
        self.assertEqual(
            [item.identifier for item in ordered],
            [
                "minecraft:diamond_sword",
                "minecraft:iron_pickaxe",
                "minecraft:cooked_beef",
                "minecraft:iron_ingot",
                "minecraft:iron_chestplate",
                "minecraft:redstone",
                "minecraft:oak_log",
                "minecraft:gunpowder",
            ],
        )

    def test_wood_and_color_families_group_naturally(self):
        items = [
            FakeItem("minecraft:spruce_log"),
            FakeItem("minecraft:oak_planks"),
            FakeItem("minecraft:oak_log"),
            FakeItem("minecraft:red_wool"),
            FakeItem("minecraft:white_wool"),
        ]
        ordered = sorted(items, key=stack_sort_key)
        self.assertEqual(
            [item.identifier for item in ordered],
            [
                "minecraft:oak_log",
                "minecraft:spruce_log",
                "minecraft:oak_planks",
                "minecraft:white_wool",
                "minecraft:red_wool",
            ],
        )

    def test_saplings_are_not_misclassified_as_wood_construction(self):
        items = [
            FakeItem("minecraft:oak_planks"),
            FakeItem("minecraft:oak_sapling"),
            FakeItem("minecraft:stone"),
        ]
        ordered = sorted(items, key=stack_sort_key)
        self.assertEqual(
            [item.identifier for item in ordered],
            ["minecraft:oak_planks", "minecraft:stone", "minecraft:oak_sapling"],
        )

    def test_second_read_mismatch_aborts_without_writes(self):
        original = [FakeItem("minecraft:iron_ingot", amount=20), FakeItem("minecraft:iron_ingot", amount=20)]
        inv = FakeInventory(original)
        inv.mutate_on_second_read = 0

        result = sort_inventory(inv, 0, 1)

        self.assertFalse(result.ok)
        self.assertFalse(result.fatal)
        self.assertEqual(inv.items, original)

    def test_write_exception_rolls_back_and_is_fatal(self):
        original = [FakeItem("minecraft:stone"), FakeItem("minecraft:apple")]
        inv = FakeInventory(original)
        inv.fail_on_set = 0

        result = sort_inventory(inv, 0, 1)

        self.assertFalse(result.ok)
        self.assertTrue(result.fatal)
        self.assertEqual(inv.items, original)

    def test_verification_failure_rolls_back_and_is_fatal(self):
        original = [FakeItem("minecraft:stone"), FakeItem("minecraft:apple")]
        inv = FakeInventory(original)
        inv.corrupt_on_set = 0

        result = sort_inventory(inv, 0, 1)

        self.assertFalse(result.ok)
        self.assertTrue(result.fatal)
        self.assertEqual(inv.items, original)

    def test_already_compacted_and_sorted_is_noop(self):
        original = [
            FakeItem("minecraft:diamond_sword", max_stack_size=1),
            FakeItem("minecraft:iron_ingot", amount=64),
            FakeItem("minecraft:iron_ingot", amount=8),
            FakeItem("minecraft:stone", amount=64),
            None,
        ]
        inv = FakeInventory(original)

        result = sort_inventory(inv, 0, 4)

        self.assertTrue(result.ok)
        self.assertEqual(result.changed_slots, 0)
        self.assertEqual(inv.items, original)


if __name__ == "__main__":
    unittest.main()
