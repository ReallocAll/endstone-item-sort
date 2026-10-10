from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "src" / "endstone_item_sort" / "plugin.py"


def class_literal(name: str):
    tree = ast.parse(PLUGIN.read_text(encoding="utf-8"))
    cls = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "ItemSortPlugin"
    )
    for node in cls.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"class literal not found: {name}")


class CommandMetadataTests(unittest.TestCase):
    def test_only_one_top_level_command_is_registered(self):
        commands = class_literal("commands")
        self.assertEqual(set(commands), {"itemsort"})

    def test_root_command_and_single_enum_overload(self):
        usages = class_literal("commands")["itemsort"]["usages"]
        self.assertEqual(
            usages,
            [
                "/itemsort",
                "/itemsort (inventory|ender|status)<action: ItemSortAction>",
            ],
        )

    def test_action_enum_is_registered_exactly_once(self):
        usages = class_literal("commands")["itemsort"]["usages"]
        joined = "\n".join(usages)
        self.assertEqual(joined.count("<action: ItemSortAction>"), 1)
        self.assertNotIn("<action: str>", joined)
        self.assertNotIn("<action: string>", joined)
        self.assertNotIn("<action: message>", joined)
        self.assertNotIn("[args: message]", joined)

    def test_declared_version(self):
        self.assertEqual(class_literal("version"), "0.4.0")


if __name__ == "__main__":
    unittest.main()
