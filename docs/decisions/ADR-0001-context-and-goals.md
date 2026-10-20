# ADR-0001: Context and Goals

## Status

Accepted

## Decision

Build AEOS as a Python/FastAPI orchestration core with explicit plugin
contracts. Provider integrations run outside the core process where possible,
and all mutating operations pass through an approval boundary.

## Context

AEOS must coordinate multiple engineering domains while remaining portable
across cloud providers and CI platforms. The documentation also requires
ephemeral workspaces, least-privilege credentials, auditability, and future
third-party plugins.

## Consequences

- The core stays provider-agnostic and can be deployed in a container.
- Plugin manifests and permissions become a stable compatibility contract.
- Integrations take longer to build because isolation and approval are
  deliberate requirements.
- A persistent event and knowledge store will be needed before production use.
