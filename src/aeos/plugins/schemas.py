from pydantic import BaseModel, ConfigDict, Field


class PluginSummary(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    version: str
    capabilities: list[str] = Field(default_factory=list)
    requires_approval: bool = True


class GitHubIssue(BaseModel):
    number: int
    title: str
    state: str
    html_url: str
    body: str | None = None
    labels: list[str] = Field(default_factory=list)


class GitHubWorkflowRun(BaseModel):
    id: int
    name: str | None = None
    status: str
    conclusion: str | None = None
    html_url: str
    head_branch: str | None = None
