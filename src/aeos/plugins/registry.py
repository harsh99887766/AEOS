from aeos.plugins.schemas import PluginSummary


class PluginRegistry:
    """In-process registry; production plugins should run in isolated containers."""

    def __init__(self) -> None:
        self._plugins: dict[str, PluginSummary] = {}

    def register(self, plugin: PluginSummary) -> None:
        if plugin.name in self._plugins:
            raise ValueError(f"Plugin already registered: {plugin.name}")
        self._plugins[plugin.name] = plugin

    def list_plugins(self) -> list[PluginSummary]:
        return sorted(self._plugins.values(), key=lambda plugin: plugin.name)
