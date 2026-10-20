from fastapi import FastAPI

from aeos.config import get_settings
from aeos.plugins.github import GitHubClient
from aeos.plugins.registry import PluginRegistry
from aeos.plugins.schemas import PluginSummary

settings = get_settings()
registry = PluginRegistry()
with GitHubClient(token=settings.github_token, base_url=settings.github_api_url) as github:
    registry.register(github.plugin_summary())

app = FastAPI(
    title="AEOS API",
    description="Safety-first autonomous engineering orchestration API.",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.get("/api/v1/plugins", response_model=list[PluginSummary], tags=["plugins"])
def list_plugins() -> list[PluginSummary]:
    return registry.list_plugins()
