# AEOS Architecture

## Context

AEOS coordinates specialist agents that can reason about source code,
CI/CD, cloud infrastructure, Kubernetes, security, and historical incidents.
The platform must act on real systems without turning an AI model into an
unrestricted operator.

## Runtime boundaries

```text
Client
  -> FastAPI API
  -> Orchestrator
       -> Agent graph / task planner
       -> Plugin registry
            -> Isolated AWS, Kubernetes, GitHub, or future plugin containers
       -> Approval service
       -> Ephemeral workspace manager
       -> Credential broker / Vault
       -> Audit event sink
       -> Knowledge store (vector database)
```

The current starter exposes only the API and plugin registry. The remaining
boundaries are intentionally represented as extension points before external
systems are connected.

## Non-negotiable safety rules

1. Plugin manifests declare capabilities and permissions before installation.
2. Dangerous actions are denied until a user supplies an explicit approval.
3. Credentials are brokered to tools and are never included in model prompts.
4. Repository work happens in an ephemeral workspace that is destroyed after
   the task.
5. Agents have a bounded retry count and must stop for human assistance after
   repeated failures.
6. Every proposed, approved, denied, and executed action is auditable.

## Recommended implementation phases

1. Add task and event models plus an event-driven orchestration service.
2. Add approval and audit persistence.
3. Add a workspace manager with cleanup guarantees.
4. Add one read-only GitHub plugin, then progressively add write operations.
5. Add isolated Docker plugin runners and Vault-backed credentials.
6. Add LangGraph workflows and a Qdrant/Chroma knowledge adapter.
7. Add a React or Streamlit client for live events and approval prompts.

## GitHub plugin

The initial GitHub integration is deliberately read-only. It provides
repository metadata, issue lookup/listing, workflow-run lookup, and workflow
log retrieval for diagnostic agents. A token is optional for public
repositories and is read from `AEOS_GITHUB_TOKEN`; it is never placed in
agent prompts.

Issue creation, branch writes, and pull-request creation are not part of this
first slice. They must be implemented through an approval-aware action service
before being exposed to agents.
