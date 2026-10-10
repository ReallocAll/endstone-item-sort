# Development conventions

- Treat `src/endstone_item_sort/` and `tests/` as the maintained project. Keep the package pure Python and use public Endstone APIs only.
- Do not change the version, Python requirement, or declared Endstone API line without a concrete compatibility reason and tests.
- Preserve the single `/itemsort` command and its single enum usage; avoid duplicate custom enum registrations.
- Never merge item stacks without matching type, data, maximum stack size, and both-direction metadata similarity. Preserve the hotbar and pinned special items.
- All writes must use snapshots, verification, rollback attempts, and process-level fail-close. Add regression tests for safety-sensitive changes.
- No player or server data, credentials, logs, local `clockmenu/menu.json`, wheels, caches, or build outputs belong in the repository.
- Use uv, Hatchling, Ruff, and pytest. Run `ruff check .`, `pytest -q`, and `uv build --wheel` before merging.
- Keep player-facing messages brief and free of implementation details. Keep the README in English.
- The repository is private; never publish PyPI packages or public GitHub releases through CI.
