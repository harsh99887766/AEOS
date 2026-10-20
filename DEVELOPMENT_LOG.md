# AEOS Development Log

This file records meaningful repository changes so contributors can understand
what was implemented, why it was implemented, and how it was validated.

## How to maintain this log

Add a new entry at the top of the **Change history** section for each
meaningful implementation change. Each entry should include:

- **Date:** local date of the change
- **Area:** affected subsystem
- **Change:** what was added or modified
- **Reason:** the requirement or design motivation
- **Validation:** tests, lint, or other checks that were run
- **Follow-up:** known next steps, if any

Routine formatting-only edits do not need a separate entry unless they affect
behavior or contributor workflow.

## Current state

AEOS currently contains a small FastAPI application and a provider-agnostic
plugin boundary. The first concrete plugin is a read-only GitHub diagnostic
client. It can retrieve repository metadata, issues, workflow runs, and
workflow logs without requiring live GitHub access during tests.

The repository does **not** yet connect to:

- GitHub write operations
- AWS or Kubernetes
- LangGraph or LangChain
- A credential vault
- A persistent audit store
- A vector knowledge database
- A frontend

These integrations must preserve the safety rules in
[`docs/architecture.md`](docs/architecture.md).

## Change history

### 2026-10-20 — Initial AEOS scaffold

- **Area:** repository structure and application foundation
- **Change:** Created the `src/`, `tests/`, `docs/`, `configs/`, and `infra/`
  structure for a scalable Python service.
- **Change:** Added a FastAPI application with a health endpoint.
- **Change:** Added Pydantic Settings configuration and `.env.example`.
- **Change:** Added pytest, Ruff, Docker, Makefile, OpenAPI, architecture
  documentation, and ADR-0001.
- **Reason:** Established a portable foundation based on the AEOS project
  documentation while keeping provider integrations behind explicit
  boundaries.
- **Validation:** The initial test suite passed with 4 tests; Ruff passed.
- **Follow-up:** Implement orchestration, approval, workspace, audit, and
  knowledge-layer boundaries.

### 2026-10-20 — Read-only GitHub diagnostic plugin

- **Area:** GitHub integration
- **Change:** Added
  [`GitHubClient`](src/aeos/plugins/github.py) with read-only operations for:
  repository metadata, issues, workflow runs, and workflow logs.
- **Change:** Added typed `GitHubIssue` and `GitHubWorkflowRun` response
  models.
- **Change:** Added explicit `GitHubApiError` handling for unsuccessful API
  responses.
- **Change:** Added optional `AEOS_GITHUB_TOKEN` and configurable
  `AEOS_GITHUB_API_URL` settings.
- **Change:** Registered the GitHub plugin in the FastAPI application with
  declared capabilities.
- **Reason:** GitHub read operations provide the information needed to
  diagnose broken builds safely. Write operations are intentionally deferred
  until an approval-aware action service exists.
- **Validation:** Added mocked HTTP tests and verified the full suite with
  7 passing tests. Ruff passed.
- **Follow-up:** Add approval-gated issue, branch, commit, and pull-request
  actions.

## Safety and contribution notes

- Never commit real tokens or credentials. Use `.env` locally; it is ignored
  by Git.
- Keep GitHub write operations separate from read-only diagnostic operations.
- Any mutating tool must declare its capabilities and pass through the
  approval boundary before execution.
- Add or update tests with each behavior change.
- Update this file when a meaningful change is completed.
