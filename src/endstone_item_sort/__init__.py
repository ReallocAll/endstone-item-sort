from __future__ import annotations

__all__ = ["ItemSortPlugin"]


def __getattr__(name: str):
    # Keep utility modules importable in ordinary Python test environments
    # where the Endstone runtime module is not installed. Endstone resolves
    # the entry point lazily and will import the plugin class inside its own
    # Python environment.
    if name == "ItemSortPlugin":
        from .plugin import ItemSortPlugin

        return ItemSortPlugin
    raise AttributeError(name)
