#!/usr/bin/env bash
set -euo pipefail

file="${1:-clockmenu/menu.json}"
if [[ ! -f "$file" ]]; then
    echo "menu file not found: $file" >&2
    exit 1
fi

tmp="$(mktemp "${file}.tmp.XXXXXX")"
trap 'rm -f "$tmp"' EXIT

jq '
  def itemsort_button: {
    "text": "§l§b物品整理§r\n§7整理背包 · 末影箱",
    "icon": "",
    "submenu": "itemsort"
  };
  def itemsort_menu: {
    "title": "§l§b物品整理",
    "content": "§f请选择要整理的物品栏：",
    "buttons": [
      {
        "text": "§l§a整理背包§r\n§7整理主背包中的物品",
        "icon": "",
        "command": "itemsort inventory"
      },
      {
        "text": "§l§5整理末影箱§r\n§7整理末影箱中的物品",
        "icon": "",
        "command": "itemsort ender"
      },
      {
        "text": "§l§0返回个人设置",
        "icon": "",
        "submenu": "settings"
      }
    ]
  };

  .menus.itemsort = itemsort_menu
  | .menus.settings.buttons |= (
      map(select((.submenu // "") != "itemsort")) as $buttons
      | ($buttons | map(.submenu // "") | index("autofishing")) as $i
      | if $i == null
        then $buttons + [itemsort_button]
        else $buttons[0:($i + 1)] + [itemsort_button] + $buttons[($i + 1):]
        end
    )
  | .menus.main.buttons |= map(
      if (.submenu // "") == "settings"
      then .text = "§l§e个人设置§r\n§7状态显示 · 菜单钟 · PvP · 自动植树 · 自动钓鱼 · 整理 · 公共影音"
      else . end
    )
' "$file" > "$tmp"

jq empty "$tmp"
mv "$tmp" "$file"
trap - EXIT

echo "updated: $file"
