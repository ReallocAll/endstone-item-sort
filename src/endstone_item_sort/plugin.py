from __future__ import annotations

from endstone import Player
from endstone.command import Command, CommandSender
from endstone.plugin import Plugin

from .sorter import SortResult, sort_inventory


class ItemSortPlugin(Plugin):
    api_version = "0.11"
    version = "0.4.0"
    description = "Inventory sorting for Endstone servers"

    # Keep a single top-level command. The first usage preserves /itemsort as a
    # help entry point. The second usage registers exactly one custom enum and
    # therefore one native autocomplete branch for all supported actions.
    #
    # Do not split the enum into several usages with the same enum type name:
    # Endstone custom enum names live in the command registry, so repeating the
    # same enum type causes "Enum ... already exists" suffixing/warnings.
    commands = {
        "itemsort": {
            "description": "整理背包或末影箱",
            "usages": [
                "/itemsort",
                "/itemsort (inventory|ender|status)<action: ItemSortAction>",
            ],
            "permissions": ["item_sort.command.use"],
        }
    }

    permissions = {
        "item_sort.command.use": {
            "description": "允许使用物品整理功能",
            "default": True,
        }
    }

    def __init__(self) -> None:
        super().__init__()
        self._writes_enabled = True
        self._disabled_reason = ""

    def on_enable(self) -> None:
        self.logger.info(f"ItemSort v{self.version} enabled.")

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if command.name != "itemsort":
            return False

        if not isinstance(sender, Player):
            sender.send_message("§c该命令只能由玩家使用。")
            return True

        if not args:
            self._send_help(sender)
            return True

        action = args[0].lower()
        if action == "inventory":
            return self._sort_player_inventory(sender)
        if action == "ender":
            return self._sort_ender_chest(sender)
        if action == "status":
            self._send_status(sender)
            return True

        # The native command enum should reject unknown actions before this
        # callback is reached. Keep a defensive fallback for API/runtime drift.
        self._send_help(sender)
        return True

    def _sort_player_inventory(self, player: Player) -> bool:
        if not self._ensure_writable(player):
            return True

        # Slots 0..8 are the hotbar. Keep them untouched; sort only the main
        # 3x9 storage area. Armor/off-hand are exposed separately by Endstone.
        result = sort_inventory(player.inventory, 9, 35)
        self._finish(player, result, "背包")
        return True

    def _sort_ender_chest(self, player: Player) -> bool:
        if not self._ensure_writable(player):
            return True

        chest = player.ender_chest
        result = sort_inventory(chest, 0, int(chest.size) - 1)
        self._finish(player, result, "末影箱")
        return True

    def _finish(self, player: Player, result: SortResult, label: str) -> None:
        if result.ok:
            if result.changed_slots == 0:
                player.send_tip(f"§7{label}已经整理好了。")
            else:
                player.send_tip(f"§a{label}整理完成")
            return

        if result.fatal:
            self._writes_enabled = False
            self._disabled_reason = result.error
            self.logger.error(
                "ItemSort disabled further writes for this process after a transactional write failure: "
                + result.error
            )
            player.send_message("§c整理失败。为保护物品，本次服务器运行期间已暂停整理功能。")
            return

        player.send_message(f"§c{label}整理失败，请稍后再试。")
        self.logger.warning(f"{label} sort failed: {result.error}")

    def _ensure_writable(self, player: Player) -> bool:
        if self._writes_enabled:
            return True
        player.send_message("§c物品整理当前不可用，请等待服务器重启后再试。")
        return False

    def _send_help(self, player: Player) -> None:
        player.send_message("§e/itemsort inventory §7- 整理背包")
        player.send_message("§e/itemsort ender §7- 整理末影箱")
        player.send_message("§e/itemsort status §7- 查看状态")

    def _send_status(self, player: Player) -> None:
        if self._writes_enabled:
            player.send_message("§a物品整理：正常")
        else:
            player.send_message("§c物品整理：暂时不可用")
