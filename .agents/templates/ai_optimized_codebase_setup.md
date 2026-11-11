# AI-Optimized Codebase Setup

**What this is:** the specification for building the technical foundation of a new Python backend repository. A planning agent reads it, together with the repository's PRD and TAD, and writes an implementation plan. An implementation agent executes that plan. The specification fixes the tooling, structure and conventions of the foundation, and names the few decisions that must be resolved from the PRD and TAD.
**Prepared by:** Rahul Parmar
**Version:** 1.6 — 2026-11-10
**Location:** copied unchanged into every new repository at `.agents/reference/ai_optimized_codebase_setup.md`.

---

## 1. Scope and operating model

### 1.1 What gets built

Starting from a repository that contains only planning documents and a small kit of agent tooling, the foundation is built in twelve sequential steps:

- validation tooling: Ruff, MyPy, Pyright, pytest
- structured JSON logging with correlation IDs
- a FastAPI application with typed settings, request-logging middleware and a canonical error model
- Docker packaging and a local Docker Compose setup
- a Supabase Postgres database with async SQLAlchemy access, CLI-managed migrations, health endpoints and database error handling
- shared utilities every future feature will use
- the README and the `CLAUDE.md` global rules that govern all later feature work

The foundation is deliberately application-agnostic. It accomplishes nothing for users yet; feature slices are built on top of it afterwards.

### 1.2 Prerequisites

Before planning starts, the repository must contain:

- the PRD and TAD for the application (default paths `.agents/PRD.md`, `.agents/TAD.md`)
- the Day-0 kit in Section 4

### 1.3 How the plan is written

The planning agent produces an implementation plan with **one task per step in Section 5, in the same order**. Every task carries five elements:

1. **Documentation research.** The planning agent locates the *current official documentation* for the tool or library the step introduces, reads it, writes what the step needs into the task, and cites the source that was used. This specification names *what* to research and *where to look* (official project documentation), never a fixed URL. Configuration is never derived from memory alone.
2. **Installation** — the `uv add` command(s).
3. **Files** — exactly the files to create or modify and what each must contain.
4. **Validation** — the checks that must pass before the task is complete; every tool set up in earlier steps participates.
5. **Commit boundary** — one commit per step, using the suggested message.

The plan also resolves the Decision Register (Section 3): for each parameter and decision it records the resolved value and quotes the PRD or TAD passage that justifies any override of a default. The plan is produced by invoking `/plan:plan-feature` with a feature description that names the paths of this specification, the PRD and the TAD, and gives the instruction to record any clarifying question, with the assumed answer, in the plan's NOTES section rather than stopping to ask; it is executed with `/implement:execute`. The plan is reviewed and approved by the project owner before execution.

### 1.4 How the plan is executed

- Steps run **sequentially, never in parallel** — they share `pyproject.toml` and the entry-point module.
- A fresh context window per step is acceptable. The context needed is the plan and the files the step creates or changes.
- **No step is complete while any validation check fails.** Never skip a check to move on.
- From Step 8 onward every step ends with the **suppression loop** (Section 5.0).
- `# type: ignore` and `# noqa` are forbidden without a documented reason on the same line.
- Dependencies are added with `uv add` / `uv add --dev` only. `pyproject.toml` dependency lists and `uv.lock` are never edited by hand.
- Files are staged explicitly for each commit. `git add .`, `git add -A` and `git add --all` are never used.

---

## 2. Fixed conventions

These apply to every repository built from this specification. They are not decision points.

### 2.1 Stack

| Concern | Choice |
|---|---|
| Language / runtime | Python 3.12 |
| Dependency and project tool | uv (`uv add`, `uv sync`, `uv run`) |
| Lint and format | Ruff — 88 characters, double quotes, rules `E W F I UP B SIM RUF`, `fixable = ["ALL"]` |
| Type checking | **Both** MyPy strict **and** Pyright strict must pass |
| Testing | pytest + pytest-asyncio (`asyncio_mode = "auto"`) + pytest-cov reporting on every run; `--strict-markers --strict-config` |
| Logging | structlog, JSON to stdout, correlation IDs via context variables |
| Web framework | FastAPI + Pydantic v2 + pydantic-settings; Uvicorn |
| Database | Supabase Postgres; migrations as SQL managed by the Supabase CLI (no Alembic); local development via `supabase start` |
| Database access | SQLAlchemy 2.0 async + asyncpg |
| Containers | Docker multi-stage build following uv's official Docker guidance; `docker-compose.yml` for local development; one image for all processes |
| Architecture | Vertical slice architecture per `.agents/reference/vertical-slice-architecture-setup-guide.md` |
| Agent tooling | Claude Code slash commands in `.claude/commands/`; global rules in `CLAUDE.md` |

### 2.2 Repository layout (vertical slice architecture)

```
app/
├── core/                 # Universal infrastructure — required by every slice
│   ├── config.py         # pydantic-settings Settings + cached get_settings()
│   ├── logging.py        # structlog setup, correlation-ID context vars
│   ├── middleware.py     # RequestLoggingMiddleware, CORS
│   ├── exceptions.py     # AppException, ErrorResponse, global handlers
│   ├── database.py       # async engine, session factory, Base, get_db()
│   ├── health.py         # /health, /health/db, /health/ready
│   ├── README.md         # the decision rule for what belongs here
│   └── tests/            # core unit tests (colocated)
├── shared/               # Utilities used by 3+ feature slices
│   ├── models.py         # SQLAlchemy mixins
│   ├── schemas.py        # pagination schemas
│   ├── utils.py          # utcnow(), format_iso()
│   └── tests/
├── {feature}/            # Vertical slices, added AFTER the foundation
│   ├── models.py · schemas.py · router.py · service.py · tests/
├── tests/                # Backend integration tests (HTTP-level, multi-slice)
│   └── conftest.py       # test_db_engine / test_db_session fixtures
└── main.py               # FastAPI entry point (see D1 for the worker variant)
```

Rules: `app/core/` never imports feature slices or `app/shared/`. `app/shared/` holds only code used by three or more slices. Slices never import each other; cross-slice code goes through `app/shared/`. The decision rule for `app/core/`: if deleting every feature slice would still require this code, it belongs in core.

### 2.3 Naming and code style

- Verbose names, always: `organisation_id`, `document_status`, `created_at` — never `id`, `status`, `run`.
- `snake_case` functions and variables; `PascalCase` classes; `UPPER_SNAKE_CASE` constants.
- Full type hints on every function signature.
- Google-style docstrings with `Args:` and `Returns:` on every public function.
- Files ≤ 500 lines; functions ≤ 50 lines; constants, configuration and long strings in their own modules.
- KISS and YAGNI: no abstractions or features before they are needed.

### 2.4 Logging convention

- `from app.core.logging import get_logger` then `log = get_logger(__name__)` — the module variable is named `log`.
- Event names use the **hybrid dotted namespace**: `domain.component.action_state`, exactly three dot-separated parts. The domain is the package the code lives in — `core` for infrastructure, otherwise the feature-slice name — so logs can be filtered by slice. Examples: `core.request.dispatch_completed`, `core.health.db_check_failed`, `ingestion.document.validation_started`. States: `_started`, `_completed`, `_failed` (general); `_validated`, `_rejected` (validation).
- Every operation logs a start and a completion (or failure) pair, always with contextual key-value fields. Never a bare message.
- `request_id` is set by the request middleware from the `X-Request-ID` header (generated when absent) and attached to every log line during a request.
- A correlation ID that is not set is **omitted from the log line entirely** — never written as `null` or an empty string.
- Never log secrets, credentials, API keys or sensitive payload contents.

### 2.5 Error handling convention

- All application errors are raised as `AppException` (or a subclass) with: `error_code`, `http_status_code`, `message`, `retryable`.
- `error_code` format: `{DOMAIN}_{CATEGORY}_{DETAIL}` in upper snake case, e.g. `INGESTION_INPUT_NOT_PDF`, `SYSTEM_DATABASE_UNAVAILABLE`. The domain list is Decision D4.
- Canonical response body (`ErrorResponse` in `app/core/exceptions.py`): `error_code`, `message`, `request_id`, `retryable` — plus the job-level ID if Decision D2 adds one. Correlation IDs are read from the logging context when the response is built; callers never pass them.
- Every response with `http_status_code >= 500` carries a **generic, non-sensitive message** ("Service temporarily unavailable. Please try again later."). The handler substitutes it for whatever message was raised and logs the original; full diagnostics go to structured logs only.
- Unhandled exceptions are converted by the request middleware into the same `ErrorResponse` shape with a 500 status, the generic message, `retryable=False` and the `request_id`, never FastAPI's default body.
- `app/core/health.py` may raise `HTTPException` directly — the one infrastructure-only exception to the rule.

### 2.6 Testing convention

| Test type | Location | Marker |
|---|---|---|
| Unit | `app/{slice}/tests/` (colocated) | none |
| Integration | `app/tests/` | `@pytest.mark.integration` |
| Cross-stack E2E | root `tests/` — reserved, empty until needed | — |

- Unit tests: no real database, no HTTP, no external providers; mocks at slice boundaries.
- Integration tests: HTTP-level via `httpx.AsyncClient` + `ASGITransport`; real local Supabase; external providers still mocked.
- Integration tests **must** use the `test_db_engine` / `test_db_session` fixtures from `app/tests/conftest.py` and never import `engine` / `AsyncSessionLocal` from `app.core.database` directly. The module-level engine binds to the first event loop; pytest-asyncio creates a new loop per test. pytest exposes a `conftest.py` only to tests beneath it, which is one more reason integration tests live in `app/tests/` and nowhere else.
- Test names: `test_<function>_<condition>_<expected_result>`. Cover happy paths, edge cases, boundaries and failure paths.

### 2.7 Configuration and secrets

- All runtime configuration flows through `app/core/config.py` (pydantic-settings) and is documented in `.env.example` with comments. `.env` is git-ignored and never committed.
- No plaintext secrets anywhere in the repository. The database URL, API keys and tokens come from environment variables or managed secrets.

### 2.8 Canonical validation commands

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy app/
uv run pyright app/
uv run pytest -m "not integration"      # fast, no database
uv run pytest                           # all, requires `supabase start`
```

`/validate:validate` runs these plus a local-server smoke test and a Docker build check.

---

## 3. Decision Register

Resolved by the planning agent from the PRD and TAD and recorded in the plan with the justifying passage. Everything not listed here is fixed by Section 2.

### 3.1 Parameters

| Placeholder | Meaning | Default |
|---|---|---|
| `{{PROJECT_SLUG}}` | Package / image name (lower snake or kebab) | — |
| `{{APP_TITLE}}` | Human-readable application name for `Settings.app_name` | — |
| `{{APP_PORT}}` | API port for local and container runs | `8123` |
| `{{ENTRY_POINT}}` | FastAPI entry module — **derived from D1** | `app/main.py` |
| `{{JOB_ID_FIELD}}` | Name of the job-level correlation ID — **derived from D2** | none |

### 3.2 Decisions

| ID | Decision | Default | Override when the PRD/TAD says… | Consequences |
|---|---|---|---|---|
| **D1** | Process model | One `app` service; entry point `app/main.py` | The application has long-running, batch or queued work that must not block HTTP requests (a worker, a scheduler, a pipeline) | Two services from the same image: `api` (entry point `app/api.py`) and `worker` (`app/worker.py`); Docker Compose declares both; the Dockerfile bakes in no `CMD` |
| **D2** | Second correlation ID | None — `request_id` only | D1 resolved to a worker | A job-level context variable named after the PRD's unit of work, set at job start and cleared at job end by the worker, omitted from logs when unset, and included as an optional field in `ErrorResponse`. The request middleware never touches it |
| **D3** | Shared model mixins beyond timestamps | `TimestampMixin` only | Multi-tenant data (organisations/accounts) → `OrgScopedMixin`; records that expire on a schedule → `RetentionMixin`; records marked deleted rather than removed → `SoftDeleteMixin` | Each chosen mixin is created in Step 11 and applied to every future table. Tenant scoping is expensive to retrofit (a migration and a row-level-security policy per table), so it is decided here |
| **D4** | Error-code domain list | The feature-slice names from the TAD, plus `SYSTEM` for infrastructure | The TAD defines another natural taxonomy (e.g. numbered pipeline stages `STAGE{N}`) | Fixes the `{DOMAIN}` part of every `error_code`. Whatever the taxonomy, it must name the domain used for infrastructure errors (`SYSTEM` by default; `STAGE0` under a staged taxonomy), because Steps 8 and 10 raise errors in that domain. Recorded in `CLAUDE.md` at Step 12 |

### 3.3 Out of scope

This specification builds the Python backend foundation only. A separate frontend, authentication, feature slices, CI pipelines and cloud deployment are set up afterwards, on top of this foundation, through their own planning. They are not added during the sequence.

---

## 4. Day-0 kit

These files exist in the repository before planning starts. The planning agent verifies them.

| Path | Purpose |
|---|---|
| `.agents/PRD.md`, `.agents/TAD.md` | The requirements this foundation serves; Section 3 is resolved from them |
| `.agents/reference/ai_optimized_codebase_setup.md` | This specification |
| `.agents/reference/vertical-slice-architecture-setup-guide.md` | Researched by the planning agent for Steps 8, 10 and 11 |
| `.agents/templates/template_readme.md` | The structure, format and voice of `README.md`; followed in Step 12 |
| `.agents/templates/template_claude_md.md` | The structure, format and voice of `CLAUDE.md`; followed in Step 12 |
| `.claude/commands/git/commit.md` | `/git:commit` — used at every commit boundary |
| `.claude/commands/validate/validate.md` | `/validate:validate` — full local validation; its expected values are updated in Step 12 |
| `.gitignore` | Complete from day 0 (entries below), so no housekeeping commits interrupt the sequence |

Day-0 `.gitignore` entries:

```
# Python
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info
.venv

# Tool caches and coverage
.coverage
.mypy_cache/
.ruff_cache/
.pytest_cache/
.pyright/

# Secrets and local config
.env

# Agent working files
.agents/reports/
.agents/docs/

# OS
.DS_Store
```

---

## 5. Build sequence

Each step specifies: scope, documentation for the planning agent to research, installation, required files and behaviour, validation, and the commit. Placeholders in `{{…}}` come from Section 3. Bracketed `[D1]`-style items apply only when that decision is overridden.

### 5.0 The suppression loop (Steps 8–12)

Linters and type checkers tempt agents to silence warnings instead of fixing them. After a step's own validation passes:

1. Search for suppression comments: `grep -rnE "# (noqa|type: ignore)" app/`.
2. For every `noqa` or `type: ignore` found: remove it by fixing the code, or keep it with a documented reason on the same line.
3. Run `/validate:validate`.
4. Commit. Fixes are folded into the step's own commit, never left as trailing commits.

### Step 0 — Pre-flight

**Scope:** verify prerequisites and resolve the Decision Register. No code is written.

**Required outcome:**
- Every Day-0 kit file in Section 4 is present; anything missing is reported and the plan stops there.
- Section 3 is resolved: each parameter has a value; each decision D1–D4 records either "default" with the reason or the override with the quoted PRD/TAD passage.
- Any conflict between the PRD/TAD and the fixed conventions in Section 2 is listed for the project owner.

### Step 1 — Initialise the project

**Scope:** the uv scaffold and the first save point.

**Required outcome:**
- `uv init` run in the repository root with whatever options its current documentation gives for a flat, non-packaged project: the result is `main.py`, `pyproject.toml` and `.python-version` at the root, and `uv run main.py` prints the hello message.
- A git repository on branch `main`, with the scaffold, the planning documents and the Day-0 kit staged explicitly.

**Commit:** `chore: initial commit — uv scaffold, planning documents and agent tooling`

### Step 2 — Ruff (lint and format)

**Scope:** the first guardrail. Ruff gives the agent an automatic feedback loop: generate, get flagged, fix, repeat.

**Documentation to research:** Ruff's official documentation — the configuration reference and the rule reference.

**Install:** `uv add --dev ruff`

**Required outcome:**
- `[tool.ruff]` in `pyproject.toml`: `target-version = "py312"`, `line-length = 88`, exclusions for `.git`, `.venv`, `__pycache__` and tool caches.
- `[tool.ruff.lint]`: `select = ["E", "W", "F", "I", "UP", "B", "SIM", "RUF"]`, `fixable = ["ALL"]`, isort `known-first-party = ["app"]`, and `ignore = ["E501", "SIM108"]` with a comment on each: line length belongs to the formatter (long strings and URLs would otherwise force suppression comments), and an explicit `if`/`else` is preferred to a ternary for readability.
- `[tool.ruff.format]`: double quotes, space indentation.
- Nothing beyond Ruff is configured.
- `main.py` (a scratch file — anything in it may be overwritten) rewritten as a short script that deliberately triggers several selected rules, proving they are detected, then fixed with `ruff check --fix` and `ruff format` until clean.

**Validation:** `uv run ruff check .` and `uv run ruff format --check .` clean.
**Commit:** `chore: add Ruff linter with AI-optimised config and sample main.py`

### Step 3 — MyPy (type safety, first layer)

**Scope:** types give the agent explicit contracts; strict mode stops it guessing.

**Documentation to research:** MyPy's official documentation — the configuration file reference, especially strict mode and the individual flags it enables.

**Install:** `uv add --dev mypy`

**Required outcome:**
- `[tool.mypy]`: `python_version = "3.12"`, `strict = true`, `warn_return_any = true`, `warn_unreachable = true`, `no_implicit_reexport = true`, `pretty = true`.
- `main.py` rewritten as a typed test module exercising the strict rules: untyped and incomplete definitions, `Any` in generics, implicit `Optional`, `TypeVar` and generics, `Callable`, unreachable branches, typed dataclasses.

**Validation:** Ruff and `uv run mypy main.py` clean.
**Commit:** `chore: add MyPy strict-mode config and type-annotated main.py`

### Step 4 — Pyright (type safety, second layer)

**Scope:** Pyright is stricter than MyPy in different places (structural typing, narrowing, exhaustiveness). Both must pass, always.

**Documentation to research:** Pyright's official documentation — configuration, type-checking modes and the diagnostic rule list.

**Install:** `uv add --dev pyright`

**Required outcome:**
- `[tool.pyright]`: `pythonVersion = "3.12"`, `typeCheckingMode = "strict"`, exclusions for `.venv` and caches, and five rules strict mode leaves off: `reportImportCycles` and `reportUninitializedInstanceVariable` as `"error"`; `reportUnnecessaryTypeIgnoreComment`, `reportImplicitStringConcatenation` and `reportMissingSuperCall` as `"warning"` — high signal, but noisy enough around framework base classes that they inform rather than block. No `include` list: the path to check is passed on the command line.
- `main.py` expanded to cover Pyright-specific patterns: `Final` constants, `TypedDict`, `Protocol` structural subtyping, exhaustive `match` statements, flow-based narrowing.
- No `# type: ignore` without a documented reason on the same line.

**Validation:** Ruff, MyPy and `uv run pyright main.py` clean.
**Commit:** `chore: add Pyright strict-mode config and expand type-checker test suite`

### Step 5 — pytest (test infrastructure)

**Scope:** tests are the top of the validation pyramid and make every later step self-checking.

**Documentation to research:** pytest's official documentation (good practices, configuration) and pytest-asyncio's official documentation (modes, fixtures, event-loop scope).

**Install:** `uv add --dev pytest pytest-asyncio pytest-cov`

**Required outcome:**
- `[tool.pytest.ini_options]`: `asyncio_mode = "auto"`, `asyncio_default_fixture_loop_scope = "function"`, `testpaths = ["app", "tests"]`, `addopts = ["--cov", "--cov-report=term-missing", "--strict-markers", "--strict-config", "-q"]` (coverage is reported on every run and never enforced per run, so a partial run such as the integration tests alone still passes; the 80% target for `app/core` is read from the full-suite report), and the marker `integration: requires a running local Supabase (deselect with -m 'not integration')`.
- `[tool.coverage.run]`: `branch = true`, `source = ["main"]` for now (switched to `["app"]` in Step 6).
- `tests/test_main.py` covering every public function in `main.py`, including async tests and an async fixture. No `tests/__init__.py`.
- Anything Ruff flags in the process (e.g. `UP047` → PEP 695 syntax) migrated.

**Validation:** Ruff, MyPy, Pyright and `uv run pytest` all green.
**Commit:** `chore: add pytest, pytest-asyncio and pytest-cov test suite`

### Step 6 — Structured logging

**Scope:** greppable, machine-parseable logs. Every later step (Docker, API, database) is debugged through these logs, so they come before the infrastructure.

**Documentation to research:** structlog's official documentation — configuration, processors, context variables, JSON rendering — together with Section 2.4 of this specification.

**Install:** `uv add structlog`

**Required outcome:**
- `app/__init__.py`, `app/core/__init__.py` (empty).
- `app/core/logging.py`:
  - `setup_logging(log_level: str)` configuring structlog for JSON output to stdout
  - `get_logger(name)` returning a bound logger; modules use `log = get_logger(__name__)`
  - `request_id` as a `ContextVar` with `get_request_id()`, `set_request_id(value=None)` (generates a UUID when none is given) and `clear_request_id()`
  - `[D2]` a second `ContextVar` `{{JOB_ID_FIELD}}` with set/clear helpers
  - a processor that injects the correlation IDs into every event and **omits** any ID that is unset — never `null`, never an empty string
  - the event-name convention `domain.component.action_state` (exactly three dot-separated parts) documented in the module docstring with examples, plus a `validate_event_name()` helper used by tests
  - exception rendering via `exc_info` for full stack traces
- `app/core/tests/__init__.py` and `app/core/tests/test_logging.py` covering: JSON shape; `request_id` injected when set and generated when absent; `[D2]` job ID present when set, absent (not null) when unset, cleared correctly; log-level filtering; exception rendering; event-name validation.
- `app/main.py`: a temporary demo runnable with `uv run python -m app.main` showing a start/complete pair and a failure logged with `exc_info`. Replaced in Step 8.
- `pyproject.toml`: coverage `source = ["app"]`.

**Validation:** Ruff, `uv run mypy app/ main.py`, Pyright and pytest green; the demo prints JSON lines carrying `request_id` and no null fields.
**Commit:** `feat(logging): add structured logging with correlation IDs`

### Step 7 — Remove the validation scaffold

**Scope:** the scratch files have done their job. They are removed in one commit, now that the logging tests keep the suite non-empty.

**Required outcome:**
- `main.py`, `tests/test_main.py` and `tests/__init__.py` (if present) removed with `git rm`.
- `pyproject.toml`: coverage `source = ["app"]`; `testpaths` stays `["app", "tests"]` — root `tests/` is reserved for future cross-stack E2E tests and stays empty.

**Validation:** Ruff, `uv run mypy app/`, `uv run pyright app/` and pytest green; the passing test count equals the logging tests from Step 6.
**Commit:** `chore: remove validation scaffold`

### Step 8 — FastAPI, settings, middleware and the error model

**Scope:** the application skeleton, with configuration, request correlation and the canonical error response defined once, before Docker needs an entry point to run.

**Documentation to research:** the vertical slice architecture guide (`.agents/reference/vertical-slice-architecture-setup-guide.md`) for infrastructure patterns and the core/shared rules; FastAPI's official documentation on lifespan events, middleware and exception handlers; pydantic-settings' official documentation.

**Install:** `uv add fastapi "uvicorn[standard]" pydantic pydantic-settings python-dotenv` and `uv add --dev httpx`

**Required outcome:**
- `app/core/config.py`: `class Settings(BaseSettings)` with `model_config` reading `.env` (UTF-8, case-insensitive); fields, all typed with descriptions: `app_name = "{{APP_TITLE}}"`, `version = "0.1.0"`, `environment = "development"`, `log_level = "INFO"`, `api_prefix = "/api/v1"`, `allowed_origins: list[str]` with a development default of `["http://localhost:3000", "http://localhost:{{APP_PORT}}"]`; `get_settings()` cached with `functools.lru_cache`; no database fields yet.
- `app/core/middleware.py`: `RequestLoggingMiddleware` on Starlette's `BaseHTTPMiddleware`, as in the vertical slice architecture guide; sets `request_id` from the `X-Request-ID` header or generates one via `set_request_id()`; logs `core.request.dispatch_started` (method, path, client_host) and `core.request.dispatch_completed` (status_code, duration_ms); on an unhandled exception logs `core.request.dispatch_failed` with `exc_info=True` and returns the generic 500 `ErrorResponse` itself — `error_code "SYSTEM_INTERNAL_ERROR"` in the D4 infrastructure domain, the generic message, `retryable=False`, the `request_id` — so unhandled exceptions never reach FastAPI's default error body; adds `X-Request-ID` to every response; clears the request context afterwards; `[D2]` never sets or clears `{{JOB_ID_FIELD}}` — that belongs to the worker. `setup_middleware(app)` adds it plus `CORSMiddleware` using `settings.allowed_origins`.
- `app/core/exceptions.py`: `class AppException(Exception)` with `error_code`, `http_status_code`, `message`, `retryable=False`; a `DatabaseError(AppException)` subclass (wired in Step 10); `class ErrorResponse(BaseModel)` with `error_code`, `message`, `request_id: str | None`, `[D2]` `{{JOB_ID_FIELD}}: str | None`, `retryable`; `app_exception_handler` logs `core.exception.handler_invoked` with the error code and status, then returns `ErrorResponse` JSON with the exception's status and the correlation IDs read from the logging context — callers never pass them; for any status `>= 500` it substitutes the generic message and logs the original, so no internal detail can leak; `setup_exception_handlers(app)` registers this one handler — unhandled exceptions are the middleware's job.
- `{{ENTRY_POINT}}`, replacing the Step 6 demo: lifespan that calls `setup_logging(settings.log_level)`, logs `core.application.startup_completed` with environment, yields, logs `core.application.shutdown_completed`; `FastAPI(title=settings.app_name, version=settings.version, lifespan=…)`; `setup_middleware(app)`; `setup_exception_handlers(app)`; `GET /` returning `{"message": settings.app_name, "version": settings.version, "docs": "/docs"}`; a `__main__` block running uvicorn on `{{APP_PORT}}`.
  `[D1]` the entry point is `app/api.py`; `app/main.py` is removed with `git rm`; `app/worker.py` is a stub that calls `setup_logging`, logs `core.worker.startup_completed` and `core.worker.shutdown_completed`, and exits cleanly (the real loop arrives with the first feature that needs it).
- `.env.example`: application settings only, each with a comment; no database yet.
- `pyproject.toml`: project description set; ruff `known-first-party = ["app"]` confirmed.
- Tests:
  - `app/core/tests/test_config.py`: defaults; environment-variable override; `get_settings()` caching; `allowed_origins` parsing
  - `app/core/tests/test_middleware.py`: generates `request_id`; honours the header; logs started/completed; on an unhandled exception logs failed with `exc_info` and returns the generic 500 `ErrorResponse` carrying `request_id` with no internal message leaked; header on the response; context cleared. Fixtures typed with `starlette.types` `Scope`/`Receive`/`Send` — no `type: ignore`
  - `app/core/tests/test_exceptions.py`: `AppException` → `ErrorResponse` shape and status; correlation IDs taken from the logging context; the `>= 500` generic-message substitution
  - `app/tests/__init__.py` and `app/tests/test_api.py` via `httpx.AsyncClient` + `ASGITransport`: root JSON; `/docs` returns 200; startup log emitted; CORS headers; `X-Request-ID` echoed
  - `[D1]` `app/tests/test_worker.py`: the stub starts and stops with the two log events

**Validation:**
- Local run: uvicorn on `{{APP_PORT}}`; `GET /` and `/docs` respond; a request with `X-Request-ID: test-123` produces a JSON log line with `request_id "test-123"` and the response echoes the header.
- `pytest -v` with coverage above 80% for `app/core`; Ruff, `mypy app/`, `pyright app/` clean.
- Suppression loop (Section 5.0).

**Commit:** `feat(api): set up FastAPI with pydantic-settings, request logging middleware and error model`

### Step 9 — Docker

**Scope:** a reproducible environment the agent can build, run and read logs from. Ordered after FastAPI so the container has a real entry point and the validation is meaningful.

**Documentation to research:** uv's official documentation on Docker integration (its multi-stage build, cache-mount and `--no-editable` guidance), and Docker Compose's official reference for volumes and `env_file`.

**Required outcome:**
- `pyproject.toml`: `[build-system]` with hatchling and `[tool.hatch.build.targets.wheel] packages = ["app"]`, so `uv sync --no-editable` can build and install the project wheel.
- `Dockerfile`, multi-stage: builder from the official slim Python 3.12 image with the uv binary copied from uv's official image at a **pinned version**; `UV_COMPILE_BYTECODE=1`, `UV_LINK_MODE=copy`; layer 1 installs dependencies only (`uv sync --locked --no-install-project --no-dev`) with a uv cache mount and bind mounts of `uv.lock` and `pyproject.toml`, so it is invalidated only when those change; layer 2 copies the source and runs `uv sync --locked --no-dev --no-editable`; the runtime stage is the same slim base as a non-root user, copies only `/app/.venv`, sets `PATH` to the venv, exposes `{{APP_PORT}}`, and bakes in **no `CMD`** — each service declares its command in Compose.
- `.dockerignore`: `.venv`, `__pycache__`, `*.pyc`, all tool caches, `.coverage`, `.git`, `.env`, and the agent folders `.agents/` and `.claude/` — planning documents and commands have no place in the image.
- `docker-compose.yml`: service `app` built from `.`, image `{{PROJECT_SLUG}}:local`, command running uvicorn on `{{ENTRY_POINT}}`'s app with `--host 0.0.0.0 --port {{APP_PORT}} --reload`, port mapping `{{APP_PORT}}:{{APP_PORT}}`, volumes `.:/app` plus an anonymous `/app/.venv` so the host copy never overwrites the container's venv, `env_file: .env` with `required: false`.
  `[D1]` two services from the same image: `api` (the uvicorn command) and `worker` (`python -m app.worker`), same volumes and env_file.

**Validation:** `docker compose build` succeeds and the image size is reported; `docker compose up -d` then `GET /` and `/docs` respond on `{{APP_PORT}}`; `docker compose logs` shows structured JSON with `request_id` and the startup event; `docker compose down`; all four tools still green.
**Commit:** `feat(docker): add Docker setup with uv multi-stage build`

### Step 10 — Database, health checks and database errors

**Scope:** Supabase Postgres through async SQLAlchemy, migrations through the Supabase CLI, health endpoints, and the database branch of the error model. The provider is Supabase throughout; only the connection string differs between local and cloud.

**Prerequisites:** Docker running; the Supabase CLI installed.

**Documentation to research:** the vertical slice architecture guide; SQLAlchemy's official documentation on the asyncio extension (async engine, `async_sessionmaker`, `DeclarativeBase`); Supabase's official documentation on local development with the CLI and on database migrations.

**Install:** `uv add "sqlalchemy[asyncio]" asyncpg`

**Required outcome:**
- Supabase: `supabase init` (creating `supabase/config.toml` and `supabase/.gitignore`); `supabase start`; `supabase migration new initial_schema` (an empty migration is acceptable); `supabase db reset` applies it. Migrations are SQL files managed by the Supabase CLI — Alembic is not added. The local database listens on port 54322.
- `app/core/database.py`: `engine = create_async_engine(settings.database_url, pool_pre_ping=True, pool_size=5, max_overflow=10, echo=settings.environment == "development")` — SQL is echoed in development only; `AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)`; `class Base(DeclarativeBase)`; `async def get_db() -> AsyncGenerator[AsyncSession, None]` yielding a session and closing it in `finally`.
- `app/core/config.py`: `database_url: str` added — required, no default, described.
- `app/core/health.py`, a router with no prefix: `GET /health` → `{"status": "healthy", "service": "api"}` with no dependencies; `GET /health/db` executes `SELECT 1` via `Depends(get_db)` and returns `{"status": "healthy", "service": "database", "provider": "supabase"}`, or on failure logs `core.health.db_check_failed` with `exc_info` and raises `HTTPException(503)`; `GET /health/ready` performs the same database check and returns `{"status": "ready", "environment": settings.environment, "database": "connected"}`, or 503. This module may raise `HTTPException` directly.
- `app/core/exceptions.py`: `DatabaseError` → `error_code "SYSTEM_DATABASE_UNAVAILABLE"` (domain per D4), `http_status_code 503`, `retryable=True`, generic message.
- `{{ENTRY_POINT}}`: health router included; on startup log `core.database.connection_initialized`; on shutdown `await engine.dispose()` and log `core.database.connection_closed`.
- `.env.example`, database section: `DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:54322/postgres`; commented Supabase Cloud variants for the direct connection and the session pooler (port 5432), with the warning that the transaction pooler (port 6543) must not be used because it does not support the named prepared statements asyncpg relies on; and a note that containers reach the local stack via `host.docker.internal`.
- `docker-compose.yml`: `DATABASE_URL` for the container(s) using `host.docker.internal:54322`. No Postgres service is added — Supabase runs its own stack.
- `.gitignore`: `.env` confirmed ignored; entries added by `supabase init` kept.
- `pyproject.toml`: `[tool.ruff.lint] ignore = ["B008"]` with a comment (FastAPI `Depends()` in parameter defaults).
- `app/core/README.md`: the decision rule for what belongs in `app/core`, `app/shared` or a slice, with a table of examples drawn from the TAD's planned slices.
- Tests:
  - `app/tests/conftest.py`: function-scoped async fixtures `test_db_engine` (fresh engine, disposed after) and `test_db_session`; the docstring states the event-loop rule — integration tests use these fixtures and never import the module-level engine
  - `app/core/tests/test_database.py`: engine creation; `get_db()` lifecycle; `Base` configured — with `settings.database_url` mocked
  - `app/core/tests/test_health.py`: `/health` 200 without a database; `/health/db` 200 with an overridden `get_db`; 503 when the session raises; `/health/ready`
  - `app/tests/test_database_integration.py` (`@pytest.mark.integration`, using the fixtures): `SELECT 1`; session lifecycle; transaction rollback; connection-pool behaviour

**Validation:** with `supabase start` running, `uv run pytest -m "not integration"` passes without touching the database and `uv run pytest -m integration` passes against it; the full suite passes with coverage; Ruff, `mypy app/`, `pyright app/` clean; `/health`, `/health/db` and `/health/ready` respond locally and from `docker compose up`; `supabase db reset` applies the migration cleanly; suppression loop.
**Commit:** `feat(core): set up Supabase Postgres database infrastructure, health checks and error handling`

### Step 11 — Shared infrastructure

**Scope:** the utilities every future slice will use, created once so AI-generated code stays uniform.

**Documentation to research:** the vertical slice architecture guide's "used by 3+ features" rule; SQLAlchemy's official documentation on mixins and `declared_attr`; Section 2.2 and Decision D3 of this specification.

**Required outcome:**
- `app/shared/__init__.py` (empty).
- `app/shared/models.py`: `TimestampMixin` with `created_at` and `updated_at` as `DateTime(timezone=True)`, not null, `default=utcnow`, `onupdate=utcnow`, declared the way the ORM's current documentation gives for columns shared through a mixin. `[D3]` `OrgScopedMixin`: `organisation_id` as a not-null, indexed foreign key to the organisations table (the migration must also add a row-level-security policy keyed on it). `[D3]` `RetentionMixin`: `expires_at` nullable `DateTime(timezone=True)`. `[D3]` `SoftDeleteMixin`: `deleted_at` nullable `DateTime(timezone=True)`.
- `app/shared/schemas.py`: `PaginationParams(BaseModel)` with `page` (default 1, `ge=1`), `page_size` (default 20, `ge=1`, `le=100`), computed `offset = (page - 1) * page_size`; `PaginatedResponse[T](BaseModel, Generic[T])` with `items`, `total`, `page`, `page_size`, computed `total_pages` (rounded up). `ErrorResponse` already lives in `app/core/exceptions.py` and is not duplicated. Any enumeration the PRD defines for the whole application — typically a status lifecycle such as `queued` / `processing` / `succeeded` / `failed` — is added here as a `StrEnum` with the PRD's exact values, so every slice and the API share one definition.
- `app/shared/utils.py`: `utcnow()` → timezone-aware UTC datetime; `format_iso(dt)` → ISO 8601 string.
- Tests: `app/shared/tests/__init__.py`; `test_models.py` (mixin columns exist with timezone-aware types and callable defaults); `test_schemas.py` (pagination defaults, bounds, offset, `total_pages`; enum values where one was added); `test_utils.py` (timezone awareness, ISO formatting); and `app/tests/test_shared_models_integration.py` (`@pytest.mark.integration`) persisting a throwaway model through `test_db_session` and checking both timestamps are set — it lives under `app/tests/` because that is where the database fixtures are visible and where integration tests belong.

**Validation:** unit tests pass without a database; the integration test is marked and passes against local Supabase; Ruff, MyPy, Pyright clean; suppression loop.
**Commit:** `feat(shared): add cross-feature utilities — mixins, schemas, utils`

### Step 12 — README, global rules and final validation

**Scope:** document the foundation for humans and encode its conventions for every future agent session. Both documents follow a template so that every repository built from this specification reads the same way: the same sections in the same order, the same formatting, the same voice. The content differs per application; the shape does not.

The two files divide the material between them and never repeat it. `CLAUDE.md` is normative: every rule, convention and constraint an agent must obey lives there and nowhere else. `README.md` is descriptive: how to install, run and use the system, for a human reader. Where a reader of one file needs something held by the other, the file carries a one-line pointer to it, never a restatement — restatements drift.

**Documentation to read:** `.agents/templates/template_readme.md` and `.agents/templates/template_claude_md.md`, in full, before writing either file.

**Required outcome:**
- `README.md`, following `.agents/templates/template_readme.md` — its section order, headings, formatting and voice are kept exactly; the content describes the product the PRD and TAD define, is written from the PRD, the TAD, this specification and the code only, and states nothing beyond them. The template's sections cover, at minimum: overview and key features; badges; table of contents; getting started and running the services for a non-technical user (prerequisites and the order of operations, pointing to `CLAUDE.md` for the commands); how it works; API reference (every endpoint the TAD defines, the status lifecycle, the error codes); testing (a pointer to `CLAUDE.md`); configuration; FAQs; contributing (a pointer to `CLAUDE.md`); licence.
- `CLAUDE.md`, following `.agents/templates/template_claude_md.md` — its section order, headings, formatting and voice are kept exactly; the rules are generated from Section 2 of this specification, the PRD, the TAD and every standing rule the plan establishes. The template's code examples are kept as written: they show format and claim nothing about this application. Real code is pointed to, never copied: the template's reference table names, for each pattern the repository already implements, the file to imitate. The template's sections cover, at minimum: core principles; tech stack; architecture (the repository tree with the application's planned slices from the TAD, and the layout rules); code style; logging; testing conventions; error handling (including the D4 domain list); development commands (setup, running the services, Supabase, tests, lint/format/type checking, Docker); agent instructions (never `git add .` / `-A`; never edit dependencies in `pyproject.toml` by hand; no suppression comments without a documented reason; never import across slices). Long reference material goes in `.agents/reference/`, not in `CLAUDE.md`.
- Where a template section has nothing to say for this application, it is kept with a one-line statement to that effect rather than removed, so the shape stays stable across repositories.
- `.claude/commands/validate/validate.md`: expected test count, entry point, port and service names replaced with the real values.

**Validation:** `/validate:validate` passes end to end; every standing rule in the plan appears in `CLAUDE.md`; and every fact `CLAUDE.md` states is checked against the repository — each path in the architecture tree and the reference table exists (a planned slice is checked against the TAD instead), each version in the tech stack matches `pyproject.toml`, and each development command has been run and succeeded (one that would create a migration is confirmed to exist instead). `README.md` is checked the same way: what it says of the product against the PRD and TAD, and its ports, commands and configuration table against the repository.
**Commit:** `docs: add README and global development rules (CLAUDE.md)`

---

## 6. Definition of done

The foundation is complete when all of the following hold:

- [ ] `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy app/`, `uv run pyright app/` report zero issues.
- [ ] `uv run pytest` passes with local Supabase running; `uv run pytest -m "not integration"` passes without it.
- [ ] No `noqa` or `type: ignore` exists without a documented reason on the same line (the Section 5.0 search finds none without one).
- [ ] `GET /`, `/docs`, `/health`, `/health/db`, `/health/ready` respond correctly both locally and from `docker compose up`.
- [ ] Every request log line carries `request_id`; no log line contains a `null` correlation ID.
- [ ] An `AppException` and an unhandled exception both return the `ErrorResponse` shape; 5xx bodies are generic.
- [ ] `supabase db reset` applies the initial migration cleanly.
- [ ] `CLAUDE.md` and `.env.example` describe the repository as it actually is; `README.md` describes the product the PRD and TAD define and states nothing beyond them.
- [ ] One commit per step, in sequence, each passing validation at the time it was made.
- [ ] The plan records the resolved Decision Register with its justifications.

---

## 7. Expected final layout

```
.
├── .agents/
│   ├── PRD.md · TAD.md
│   ├── reference/  (ai_optimized_codebase_setup, vertical-slice-architecture-setup-guide)
│   └── templates/  (template_readme, template_claude_md)
├── .claude/commands/  (git/commit, validate/validate)
├── app/
│   ├── core/    (config, logging, middleware, exceptions, database, health, README, tests/)
│   ├── shared/  (models, schemas, utils, tests/)
│   ├── tests/   (conftest, test_api, test_database_integration)
│   └── main.py                       [D1 worker: api.py + worker.py instead]
├── supabase/  (config.toml, migrations/…_initial_schema.sql)
├── tests/                            (reserved for E2E, empty)
├── Dockerfile · .dockerignore · docker-compose.yml
├── .env.example · .gitignore · .python-version
├── pyproject.toml · uv.lock
├── CLAUDE.md · README.md
```

---

## 8. Provenance

The step sequence and the principle of researching official documentation before configuring each tool come from Cole Medin's Dynamous Agentic Coding Live Workshop #2, "Creating an AI-Optimized Codebase", and its instructor guide. This specification departs from that workshop in these ways: Supabase with CLI-managed migrations instead of a Postgres container with Alembic; both type checkers mandatory; the tooling and `.gitignore` in place from day 0 rather than created mid-sequence; FastAPI before Docker; one scaffold-cleanup commit; a structured `AppException`/`ErrorResponse` error model; the suppression loop after every step from Step 8; the Decision Register; and `CLAUDE.md` written at the end from the fixed conventions.
