# AEOS

AEOS (Autonomous Engineering Orchestration System) is a safety-first platform
for coordinating engineering agents that can inspect repositories,
infrastructure, and CI/CD systems.

This repository is an intentionally small, platform-agnostic starter. It
defines the seams required by the project documentation without pretending
that cloud credentials, model providers, or destructive tools are configured.

## Design goals

- **Plugin-driven:** provider-specific capabilities live behind explicit
  plugin contracts.
- **Human-in-the-loop:** actions marked as dangerous require an approval before
  execution.
- **Ephemeral by default:** workspaces are temporary and are not used as
  permanent source-code storage.
- **Auditable:** orchestration events and action decisions have a dedicated
  audit boundary.
- **Portable:** local development uses standard Python tooling and Docker;
  CI can invoke the same commands on any runner.

## Repository layout

```text
docs/                    Architecture, ADRs, and API contract
src/aeos/                Application and domain packages
tests/                   Unit and integration tests
infra/docker/            Portable container definitions
infra/terraform/         Infrastructure placeholder
infra/scripts/           Local automation
configs/                 Environment configuration
```

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# macOS/Linux
# . .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
make test
python -m uvicorn aeos.main:app --reload
```

The API is then available at <http://127.0.0.1:8000/docs>.

### Windows troubleshooting

Always install and run tools through the same Python interpreter:

```powershell
python -m pip install -e ".[dev]"
python -m uvicorn aeos.main:app --reload
```

The `-e` option installs AEOS in editable mode, which makes the `aeos` package
inside `src/` importable. Installing only `uvicorn` is not enough; it gives
you the web-server command but does not install this project or its
dependencies.

If `python` and `pip` point to different installations, check them with:

```powershell
python -c "import sys; print(sys.executable)"
python -m pip --version
```

Both commands should refer to the same Python installation. Prefer
`python -m pip` instead of calling `pip` directly.

## Safety boundary

The starter does not connect to AWS, Kubernetes, GitHub, a model provider, or
a credential vault. Integrations must be added through plugins and must
preserve the approval, workspace, credential, and audit contracts documented
in [docs/architecture.md](docs/architecture.md).

## Development history

Meaningful implementation work, design reasoning, validation results, and
follow-up items are tracked in
[DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md). Contributors should add an entry
when completing a significant change.

## License

MIT. See [LICENSE](LICENSE).
