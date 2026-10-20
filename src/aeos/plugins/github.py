from collections.abc import Iterable
from typing import Any

import httpx

from aeos.plugins.schemas import GitHubIssue, GitHubWorkflowRun, PluginSummary


class GitHubApiError(RuntimeError):
    """Raised when GitHub returns an unsuccessful response."""


class GitHubClient:
    """Small, read-only GitHub API client for diagnostic agent tools."""

    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api.github.com",
        client: httpx.Client | None = None,
    ) -> None:
        self._client = client or httpx.Client()
        self._owns_client = client is None
        self._client.base_url = httpx.URL(base_url.rstrip("/"))
        self._headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            self._headers["Authorization"] = f"Bearer {token}"

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "GitHubClient":
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()

    def plugin_summary(self) -> PluginSummary:
        return PluginSummary(
            name="github",
            version="0.1.0",
            capabilities=[
                "github.repository.read",
                "github.issues.read",
                "github.workflows.read",
                "github.workflow_logs.read",
            ],
            requires_approval=False,
        )

    def get_repository(self, owner: str, repository: str) -> dict[str, Any]:
        return self._request("GET", f"/repos/{owner}/{repository}")

    def list_issues(
        self,
        owner: str,
        repository: str,
        *,
        state: str = "open",
        labels: Iterable[str] = (),
    ) -> list[GitHubIssue]:
        params = {"state": state, "labels": ",".join(labels)}
        payload = self._request("GET", f"/repos/{owner}/{repository}/issues", params=params)
        return [self._issue_from_payload(item) for item in payload if "pull_request" not in item]

    def get_issue(self, owner: str, repository: str, number: int) -> GitHubIssue:
        payload = self._request("GET", f"/repos/{owner}/{repository}/issues/{number}")
        return self._issue_from_payload(payload)

    def list_workflow_runs(
        self,
        owner: str,
        repository: str,
        *,
        workflow: str | None = None,
        branch: str | None = None,
        per_page: int = 30,
    ) -> list[GitHubWorkflowRun]:
        path = f"/repos/{owner}/{repository}/actions/runs"
        if workflow:
            path = f"/repos/{owner}/{repository}/actions/workflows/{workflow}/runs"
        params = {"per_page": min(max(per_page, 1), 100)}
        if branch:
            params["branch"] = branch
        payload = self._request("GET", path, params=params)
        return [self._workflow_from_payload(item) for item in payload.get("workflow_runs", [])]

    def get_workflow_logs(self, owner: str, repository: str, run_id: int) -> bytes:
        response = self._client.get(
            f"/repos/{owner}/{repository}/actions/runs/{run_id}/logs",
            headers={**self._headers, "Accept": "application/vnd.github+json"},
            follow_redirects=True,
        )
        self._raise_for_status(response)
        return response.content

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        response = self._client.request(method, path, headers=self._headers, **kwargs)
        self._raise_for_status(response)
        return response.json()

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        if response.is_success:
            return
        detail = response.text[:500]
        raise GitHubApiError(f"GitHub API returned {response.status_code}: {detail}")

    @staticmethod
    def _issue_from_payload(payload: dict[str, Any]) -> GitHubIssue:
        return GitHubIssue(
            number=payload["number"],
            title=payload["title"],
            state=payload["state"],
            html_url=payload["html_url"],
            body=payload.get("body"),
            labels=[label["name"] for label in payload.get("labels", [])],
        )

    @staticmethod
    def _workflow_from_payload(payload: dict[str, Any]) -> GitHubWorkflowRun:
        return GitHubWorkflowRun(
            id=payload["id"],
            name=payload.get("name"),
            status=payload["status"],
            conclusion=payload.get("conclusion"),
            html_url=payload["html_url"],
            head_branch=payload.get("head_branch"),
        )
