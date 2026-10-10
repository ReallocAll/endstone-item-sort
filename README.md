# ItemSort

A lightweight, pure-Python inventory sorter for [Endstone](https://github.com/EndstoneMC/endstone). It uses the public Python API and does not depend on Bedrock internals or native extensions.

## Features

- Sorts the player's **main inventory** (slots 9–35) without touching the hotbar, armor, or off-hand.
- Sorts all accessible slots in the player's **Ender Chest**.
- Combines compatible partial stacks up to their maximum size before ordering items by category and family.
- Keeps bundles, invalid stacks, and oversized stacks in their original positions.
- Checks item type, data value, stack capacity, and metadata similarity before merging.
- Takes a pre-write snapshot, checks the written result, and attempts a rollback on failure. After a write failure, further sorting is disabled until the next restart.
- Provides one `/itemsort` command with native subcommand completion.

Ordinary chests, barrels, and shulker boxes are **not supported**: the target Endstone Python API does not expose their block inventories. They will not be modified.

## Requirements

- Python 3.10 or newer
- Endstone Python API 0.11

No additional runtime Python dependencies are required. The package does not pin individual Endstone development builds or Minecraft versions.

## Installation

Install the built wheel into the same Python environment as Endstone, then **restart the server**:

```bash
uv pip install --python /path/to/endstone/.venv/bin/python dist/endstone_item_sort-0.4.0-py3-none-any.whl
```

Do not install an older C++/native ItemSort build alongside this package.

## Commands

| Command | Description |
| --- | --- |
| `/itemsort` | Display help |
| `/itemsort inventory` | Sort the 27 main inventory slots |
| `/itemsort ender` | Sort the Ender Chest |
| `/itemsort status` | Display availability |

The `item_sort.command.use` permission is granted to all players by default. All subcommands share a single root command and one enum overload, so the native command interface can complete their names.

## Configuration and ClockMenu

ItemSort has **no plugin configuration file**. Sorting boundaries and safety checks are fixed in this release.

An optional integration script is provided at `menu/clockmenu-jq.sh`. From the server's `plugins` directory, run:

```bash
/path/to/repository/menu/clockmenu-jq.sh clockmenu/menu.json
```

It requires `jq`, adds an **Item Sorting** submenu under personal settings, and can be rerun without duplicating its button. It edits the supplied JSON file in place and does not create a backup; inspect its menu assumptions before using it with a customized ClockMenu.

## Development

Install [uv](https://docs.astral.sh/uv/), then run:

```bash
uv run --with pytest --with ruff ruff check .
uv run --with pytest --with ruff pytest -q
uv build --wheel
```

To test an installed wheel without depending on a local checkout:

```bash
uv pip install --python /path/to/python --no-deps dist/endstone_item_sort-0.4.0-py3-none-any.whl
```

GitHub Actions runs lint, tests, wheel building, and an isolated installed-wheel metadata check. The workflow stores wheels as CI artifacts only; it does not publish packages or releases.

## License

GPL-3.0-only. See [LICENSE](LICENSE). The sorting behavior was designed with reference to common inventory-organizing conventions (including [ChestSort](https://github.com/mfnalex/ChestSort)); no upstream source files or assets are bundled.
