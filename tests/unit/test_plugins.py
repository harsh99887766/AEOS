from aeos.plugins.registry import PluginRegistry
from aeos.plugins.schemas import PluginSummary


def test_registry_returns_plugins_in_name_order():
    registry = PluginRegistry()
    registry.register(PluginSummary(name="kubernetes", version="0.1.0"))
    registry.register(PluginSummary(name="aws", version="0.1.0"))

    assert [plugin.name for plugin in registry.list_plugins()] == ["aws", "kubernetes"]


def test_registry_rejects_duplicate_plugins():
    registry = PluginRegistry()
    plugin = PluginSummary(name="github", version="0.1.0")
    registry.register(plugin)

    try:
        registry.register(plugin)
    except ValueError as error:
        assert str(error) == "Plugin already registered: github"
    else:
        raise AssertionError("Expected duplicate registration to fail")
