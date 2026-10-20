import httpx
import pytest

from aeos.plugins.github import GitHubApiError, GitHubClient


def github_client(handler):
    return GitHubClient(
        token="test-token",
        base_url="https://github.test",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


def test_list_issues_excludes_pull_requests():
    def handler(request):
        assert request.url.path == "/repos/acme/platform/issues"
        assert request.headers["Authorization"] == "Bearer test-token"
        return httpx.Response(
            200,
            json=[
                {
                    "number": 7,
                    "title": "Broken build",
                    "state": "open",
                    "html_url": "https://github.test/acme/platform/issues/7",
                    "body": "CI is failing",
                    "labels": [{"name": "bug"}],
                },
                {"number": 8, "pull_request": {"url": "ignored"}},
            ],
        )

    with github_client(handler) as client:
        issues = client.list_issues("acme", "platform")

    assert len(issues) == 1
    assert issues[0].labels == ["bug"]


def test_workflow_runs_are_normalized():
    def handler(request):
        assert request.url.path == "/repos/acme/platform/actions/runs"
        return httpx.Response(
            200,
            json={
                "workflow_runs": [
                    {
                        "id": 42,
                        "name": "CI",
                        "status": "completed",
                        "conclusion": "failure",
                        "html_url": "https://github.test/runs/42",
                        "head_branch": "main",
                    }
                ]
            },
        )

    with github_client(handler) as client:
        runs = client.list_workflow_runs("acme", "platform", branch="main")

    assert runs[0].id == 42
    assert runs[0].conclusion == "failure"


def test_api_errors_are_explicit():
    def handler(_request):
        return httpx.Response(404, text='{"message":"Not Found"}')

    with github_client(handler) as client:
        with pytest.raises(GitHubApiError, match="404"):
            client.get_issue("acme", "platform", 99)
