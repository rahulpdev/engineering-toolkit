# AI-Optimized Codebase Setup — Obsidian Plugin

**What this is:** the specification for building the technical foundation of a new Obsidian plugin repository in TypeScript. A planning agent reads it, together with the repository's PRD and TAD, and writes an implementation plan. An implementation agent executes that plan. The specification fixes the tooling, structure and conventions of the foundation, and names the few decisions that must be resolved from the PRD and TAD.
**Prepared by:** Rahul Parmar
**Version:** 1.5 — 2026-11-12
**Location:** copied unchanged into every new plugin repository at `.agents/reference/ai_optimized_codebase_setup_obsidian_plugin.md`.

---

## 1. Scope and operating model

### 1.1 What gets built

Starting from a repository that contains only planning documents and a small kit of agent tooling, the foundation is built in twelve sequential steps:

- validation tooling: linter and formatter, strict type checking, type-aware lint rules, unit tests
- structured JSON logging with a correlation ID on every event
- an application core — a TypeScript library holding every rule and operation, with no dependency on Obsidian — reached through ports (the short list of things it needs done, such as "read a note" or "tell me the time"), each supplied by an adapter in the plugin
- the plugin package: manifest, lifecycle, settings, the adapter for every port, and a production build to the single bundled file Obsidian loads
- tests that run inside a real copy of Obsidian at the oldest supported version and the latest
- release automation that satisfies the community directory's automated review
- the README and the `CLAUDE.md` global rules that govern all later feature work

The foundation is deliberately application-agnostic. It accomplishes nothing for users yet; feature slices are built on top of it afterwards.

### 1.2 Prerequisites

Before planning starts, the repository must contain:

- the PRD and TAD for the application (default paths `.agents/PRD.md`, `.agents/TAD.md`)
- the Day-0 kit in Section 4

### 1.3 How the plan is written

The planning agent produces an implementation plan with **one task per step in Section 5, in the same order**. Every task carries five elements:

1. **Documentation research.** The planning agent locates the *current official documentation* for the tool or library the step introduces, reads it, writes what the step needs into the task, and cites the source that was used. This specification names *what* to research and *where to look* (official project documentation, and the Obsidian plugin development reference in the Day-0 kit), never a fixed URL. Configuration is never derived from memory alone.
2. **Installation** — the `pnpm add` command(s).
3. **Files** — exactly the files to create or modify and what each must contain.
4. **Validation** — the checks that must pass before the task is complete; every tool set up in earlier steps participates, and every command follows the tooling rule in Section 2.3.
5. **Commit boundary** — one commit per step, using the suggested message.

The plan also resolves the Decision Register (Section 3): for each parameter and decision it records the resolved value and quotes the PRD or TAD passage that justifies any override of a default. The plan is produced by invoking `/plan:plan-feature` with a feature description that names the paths of this specification, the PRD and the TAD, and gives the instruction to record any clarifying question, with the assumed answer, in the plan's NOTES section rather than stopping to ask; it is executed with `/implement:execute`. The plan is reviewed and approved by the project owner before execution.

### 1.4 How the plan is executed

- Steps run **sequentially, never in parallel** — they share the workspace configuration and the plugin's entry module.
- A fresh context window per step is acceptable. The context needed is the plan and the files the step creates or changes.
- **No step is complete while any validation check fails.** Never skip a check to move on.
- From Step 8 onward every step ends with the **suppression loop** (Section 5.0).
- Suppression comments — every ESLint directive comment and every `@ts-` directive — are forbidden without a documented reason on the same line. Disabling a security rule or an `obsidianmd/*` rule is never permitted: the linter treats it as an error and the directory's scanner ignores the directive anyway.
- Dependencies are added with `pnpm add` / `pnpm add -D` only. `package.json` dependency lists and the lockfile are never edited by hand.
- Files are staged explicitly for each commit. `git add .`, `git add -A` and `git add --all` are never used.

---

## 2. Fixed conventions

These apply to every repository built from this specification. They are not decision points.

### 2.1 Stack

| Concern | Choice |
|---|---|
| Language | TypeScript 5.x, `strict` mode, plus the stricter compiler flags in Step 3 |
| Runtime | Obsidian's own (Electron on desktop, Capacitor on mobile); Node for build, tests and tooling, at the current long-term-support version |
| Package manager and workspace | pnpm, one workspace holding the `core` and `plugin` packages (and any package Decision D2 adds); lockfile committed |
| Bundler | esbuild, as the official plugin template uses, producing one `main.js` with every dependency bundled and `obsidian`, `electron`, `@codemirror/*`, `@lezer/*` and Node built-ins left external |
| Lint | ESLint with the official Obsidian plugin rule set (`eslint-plugin-obsidianmd`, the same rules the directory's scanner runs) and typescript-eslint's type-checked rules, in one flat configuration |
| Format | Prettier |
| Type checking | `tsc --noEmit` per package |
| Testing | Vitest for unit tests, with the `obsidian` module aliased to a shim; `wdio-obsidian-service` for tests inside a real Obsidian |
| Schemas | Zod — one definition that validates data while the program runs and yields the static type |
| Identifiers | `crypto.randomUUID()` from the Web Crypto API, available in Obsidian and Node |
| Logging | JSON Lines (one JSON object per line) through a log-sink port; the plugin adapter writes diagnostics with `console.debug` / `warn` / `error`, never `console.log` |
| Architecture | Vertical slice architecture inside the core per `.agents/reference/vertical-slice-architecture-setup-guide.md`; ports and adapters between the core and everything outside it |
| Agent tooling | Claude Code slash commands in `.claude/commands/`; global rules in `CLAUDE.md` |

### 2.2 Repository layout

```
<repo>/
├── manifest.json                  # the plugin manifest — at the root, as the directory requires
├── versions.json                  # plugin version → minimum Obsidian version
├── styles.css                     # the plugin's CSS; Obsidian loads it automatically
├── package.json                   # workspace root; `build` here produces main.js at the root
├── pnpm-workspace.yaml
├── packages/
│   ├── core/                      # the application core — no dependency on `obsidian`
│   │   └── src/
│   │       ├── core/              # plumbing every feature needs
│   │       │   ├── ports.ts       # the port interfaces
│   │       │   ├── api.ts         # the operation registry, versions, Result type
│   │       │   ├── errors.ts      # AppError and error codes
│   │       │   ├── logging.ts     # event construction and the log-sink port
│   │       │   ├── ids.ts         # identifier generation
│   │       │   ├── testing/       # in-memory adapters and a pretend clock for every test
│   │       │   └── README.md      # the decision rule for what belongs here
│   │       ├── shared/            # code used by 3+ feature slices
│   │       ├── {feature}/         # vertical slices, added AFTER the foundation
│   │       │   ├── operations.ts · rules.ts · schemas.ts · README.md · *.test.ts
│   │       └── index.ts           # the core's public surface
│   └── plugin/                    # the Obsidian plugin — thin
│       ├── src/
│       │   ├── main.ts            # lifecycle only
│       │   ├── adapters/          # one adapter per port, using Obsidian's API
│       │   └── settings/          # the settings tab
│       └── esbuild.config.mjs
├── __mocks__/obsidian.ts          # the shim the unit tests use in place of `obsidian`
├── e2e-tests/                     # tests inside a real Obsidian
├── test-vault/                    # fixture vault for development and e2e tests
├── scripts/                       # build checks, version bump, manifest check
└── .github/workflows/
```

Rules: `packages/core/` never imports `obsidian`, Electron or a Node module; a build check fails if it does. `core/core/` is infrastructure only and never imports a feature slice or `shared/`. `shared/` holds only code used by three or more slices. Slices never import each other's internals; a slice uses only what another slice publishes. `main.ts` does lifecycle and nothing else. The scanner ignores `scripts/`, `__mocks__/`, `e2e-tests/`, `test-vault/`, `docs/` and `*.test.*` files, so those names are kept exactly.

### 2.3 Naming and code style

- Verbose names, always: `noteId`, `operationName`, `createdAt` — never `id`, `op`, `ts`.
- `camelCase` functions, variables and object properties; `PascalCase` types, classes and Zod schemas; `UPPER_SNAKE_CASE` constants. Data written to the vault keeps the field names the PRD fixes.
- Every exported function has a TSDoc comment (`/** … */`) stating what it does, with `@param` and `@returns`.
- Files ≤ 300 lines; functions ≤ 50 lines; constants, configuration and long strings in their own modules.
- Every word shown to the user lives in one messages module, never inline in a feature.
- KISS and YAGNI: no abstractions or features before they are needed.
- Commands and scripts never bring in a second programming language or an undeclared package — for example, no Python one-liner in a TypeScript project. General command-line tools such as `git`, `grep` and `curl` are allowed. A further package becomes a declared dependency first.

### 2.4 Logging convention

- Every log line is one JSON object with at least `event`, `level`, `timestamp` (UTC, ISO 8601) and the contextual fields of the operation.
- The minimum level written is a setting, `info` by default.
- Event names use the **hybrid dotted namespace**: `domain.component.action_state`, exactly three dot-separated parts. The domain is the package or slice the code lives in — `core` for infrastructure, otherwise the feature-slice name — so logs can be filtered by slice. Examples: `core.jobs.tick_completed`, `core.vault.write_deferred`, `capture.note.creation_started`. States: `_started`, `_completed`, `_failed` (general); `_validated`, `_rejected` (validation).
- Every operation logs a start and a completion (or failure) pair, always with contextual key-value fields. Never a bare message.
- Every operation carries a `correlationId`, generated when the request is made and passed explicitly through every call it causes; it appears on every log line the operation writes. A correlation ID that is not set is **omitted from the line entirely** — never written as `null` or an empty string.
- Logs never contain note content, a licence key, a secret or anything that looks like one.
- Diagnostics go to the log; anything the user must see goes through the notice port as a plain-language message.

### 2.5 Error handling convention

- Inside the core, failures are values, not exceptions: every operation returns a `Result` — `{ ok: true, correlationId, outcome }` or `{ ok: false, correlationId, error }` — and never throws across the core's boundary.
- The error carries `errorCode`, `message`, `retryable` and optional `details`. `errorCode` format: `{DOMAIN}_{CATEGORY}_{DETAIL}` in upper snake case, e.g. `CAPTURE_INPUT_EMPTY`, `CORE_STORE_UNAVAILABLE`. The domain list is Decision D4.
- Every failure has a stable code used in the log, in the plugin's messages to the user and in support documentation.
- The plugin shows a failure to the user as one plain-language notice naming what happened and what to do; the diagnostic detail goes to the log only.
- Event handlers in the plugin never throw: each is wrapped so that one bad file cannot break the handler for all files.
- No floating promises: every promise is awaited or explicitly handled, enforced by the type-aware lint rule.

### 2.6 Testing convention

| Test type | Location | Runner |
|---|---|---|
| Core unit | beside the code, `*.test.ts` | Vitest, no shim needed — the core imports nothing from `obsidian` |
| Plugin unit | beside the code, `*.test.ts` | Vitest, with `obsidian` aliased to `__mocks__/obsidian.ts` |
| Inside a real Obsidian | `e2e-tests/` | `wdio-obsidian-service`, against `earliest` (the manifest's minimum version) and `latest` |

- Core tests are fixtures in, expected results out: an in-memory adapter for every port and a pretend clock, kept once in `core/core/testing/` and reused by every slice, so no file system and no Obsidian.
- The shim stays minimal: empty classes and simple functions for what the plugin package touches. A shim reflects assumptions about the API, so the real-Obsidian tests are what prove the integration.
- Test names: `describe` the function, `it` states the condition and the expected result.
- Every feature must cover happy paths, edge cases, boundary conditions and failure paths.

### 2.7 Configuration and secrets

- User settings are loaded with `Object.assign({}, DEFAULT_SETTINGS, await this.loadData())`, validated with a Zod schema, and saved on change. Settings migrations are named, idempotent steps recorded in the saved data; a corrupt settings file is never overwritten with an empty object.
- Anything secret is held in Obsidian's secret storage with only its identifier in settings, with a fallback for app versions that lack secret storage.
- No secret, token or credential is committed to the repository or written to a note, an export or a log.

### 2.8 Canonical validation commands

Workspace-root scripts, each running across every package:

```bash
pnpm lint            # eslint . --max-warnings 0 — zero errors, zero warnings
pnpm format:check    # prettier --check .
pnpm typecheck       # tsc --noEmit in every package
pnpm test            # vitest run, with coverage
pnpm build           # the production build; produces main.js at the repository root
pnpm e2e             # wdio-obsidian-service against earliest and latest Obsidian
pnpm check:manifest  # manifest and versions.json rules (Step 11)
```

Step 12 writes these into `/validate:validate` as its checks, in this order. Until then, the command runs whichever of these scripts already exist.

---

## 3. Decision Register

Resolved by the planning agent from the PRD and TAD and recorded in the plan with the justifying passage. Everything not listed here is fixed by Section 2.

### 3.1 Parameters

| Placeholder | Meaning | Rule or default |
|---|---|---|
| `{{PLUGIN_ID}}` | The manifest `id` | Lowercase letters and hyphens; must not contain `obsidian`; must not end with `plugin`; unique in the directory; **cannot change after publication** |
| `{{PLUGIN_NAME}}` | The manifest `name` | Short, English, Basic Latin; no "Obsidian", "Plugin" or a core feature's name |
| `{{PLUGIN_DESCRIPTION}}` | The manifest `description` | Starts with an action statement, ends with a period, ≤ 250 characters, no emoji |
| `{{MIN_OBSIDIAN_VERSION}}` | The manifest `minAppVersion` | The oldest Obsidian version the plugin works on; the real-Obsidian tests run against it |
| `{{AUTHOR}}`, `{{LICENCE}}` | Manifest `author`; the `LICENSE` file | From the PRD/TAD |
| `{{NODE_VERSION}}` | Node for build and tests | The current long-term-support release |

### 3.2 Decisions

| ID | Decision | Default | Override when the PRD/TAD says… | Consequences |
|---|---|---|---|---|
| **D1** | Platform | Mobile-capable: `isDesktopOnly: false` | The plugin needs a Node or Electron API, or a desktop-only Obsidian feature such as the status bar | `isDesktopOnly: true`; Node imports allowed in the plugin package only, never in the core; mobile emulation dropped from the acceptance gates |
| **D2** | Headless client | None | The PRD requires driving the core outside Obsidian (a test client, a command-line tool, a second host) | A `packages/test-client/` (or named) package supplying an adapter for every port that runs without Obsidian and a command line that runs any operation, built in Step 8 and used by the core scenario tests and `/validate:validate` |
| **D3** | Plugin-owned data | Settings only, in `data.json` via `loadData` / `saveData` | The PRD defines data the plugin keeps beyond its settings (a store, a log, records) | A store port in the core and a store adapter in the plugin writing to a folder the TAD names; logs may then also go to a file through the log-sink port |
| **D4** | Error-code domain list | The feature-slice names from the TAD, plus `CORE` for infrastructure | The TAD defines another natural taxonomy | Fixes the `{DOMAIN}` part of every `errorCode`. Whatever the taxonomy, it must name the domain used for infrastructure errors (`CORE` by default), because Steps 6 and 8 raise errors in that domain. Recorded in `CLAUDE.md` at Step 12 |

### 3.3 Out of scope

This specification builds the plugin repository's foundation only. Any server, service or database the application also needs lives in its own repository with its own specification. Feature slices, the directory submission itself and marketing of the listing are done afterwards, on top of this foundation.

---

## 4. Day-0 kit

These files exist in the repository before planning starts. The planning agent verifies them.

| Path | Purpose |
|---|---|
| `.agents/PRD.md`, `.agents/TAD.md` | The requirements this foundation serves; Section 3 is resolved from them |
| `.agents/reference/ai_optimized_codebase_setup_obsidian_plugin.md` | This specification |
| `.agents/reference/vertical-slice-architecture-setup-guide.md` | Researched by the planning agent for Steps 8 and 11 |
| `.agents/reference/obsidian-community-plugin-development.md` | The Obsidian plugin development reference: policies, manifest, guidelines, testing, release; researched by the planning agent for Steps 1, 2, 9, 10 and 11 |
| `.agents/templates/template_readme.md` | The structure, format and voice of `README.md`; followed in Step 12 |
| `.agents/templates/template_claude_md.md` | The structure, format and voice of `CLAUDE.md`; followed in Step 12 |
| `.claude/commands/git/commit.md` | `/git:commit` — used at every commit boundary |
| `.claude/commands/validate/validate.md` | `/validate:validate` — full local validation; its checks are written in Step 12 |
| `.gitignore` | Complete from day 0 (entries below), so no housekeeping commits interrupt the sequence |

Day-0 `.gitignore` entries:

```
# Dependencies and build output
node_modules/
main.js              # built in releases, never committed
dist/
*.tsbuildinfo
coverage/

# Development vault state
test-vault/.obsidian/workspace*.json
test-vault/.obsidian/plugins/*/main.js

# Real-Obsidian test harness
.wdio-obsidian-cache/

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

1. Search every code file in the repository for suppression comments: `git grep --untracked -nE "eslint-(disable|enable)|/\* *eslint |@ts-" -- '*.ts' '*.mts' '*.cts' '*.js' '*.mjs' '*.cjs'`.
2. For every match: remove it by fixing the code, or keep it with a documented reason on the same line. A disabled security or `obsidianmd/*` rule is always removed.
3. Run `/validate:validate`.
4. Commit. Fixes are folded into the step's own commit, never left as trailing commits.

### Step 0 — Pre-flight

**Scope:** verify prerequisites and resolve the Decision Register. No code is written.

**Required outcome:**
- Every Day-0 kit file in Section 4 is present; anything missing is reported and the plan stops there.
- Section 3 is resolved: each parameter has a value that satisfies its rule; each decision D1–D4 records either "default" with the reason or the override with the quoted PRD/TAD passage.
- Any conflict between the PRD/TAD and the fixed conventions in Section 2 is listed for the project owner.

### Step 1 — Initialise the workspace

**Scope:** the official template, restructured into a workspace, and the first save point.

**Documentation to research:** the Obsidian plugin development reference on the official sample-plugin template and its files; pnpm's official documentation on workspaces.

**Required outcome:**
- The repository is generated from Obsidian's official sample-plugin template (not forked), so its esbuild configuration, lint configuration, version-bump script and GitHub workflows are present from the start.
- The template's plugin source moves to `packages/plugin/`; an empty `packages/core/` is created; `pnpm-workspace.yaml` lists both; the root `package.json` gains the scripts in Section 2.8 (each initially delegating to the packages that exist) and a `build` script that produces `main.js` at the repository root.
- `manifest.json` at the root holds the Section 3.1 values; `versions.json` maps the initial version to `{{MIN_OBSIDIAN_VERSION}}`; the template's placeholder `fundingUrl`, sample classes and sample code are removed; `LICENSE` names the real author and licence.
- A `.nvmrc` (or equivalent) pins `{{NODE_VERSION}}`.
- A scratch file `packages/core/src/scratch.ts` (anything in it may be overwritten) with a trivially runnable function; running it with the TypeScript runner the current Node or workspace documentation recommends prints a hello line.
- A git repository on branch `main`, with the workspace, the planning documents and the Day-0 kit staged explicitly.

**Commit:** `chore: initial commit — plugin template as a pnpm workspace, planning documents and agent tooling`

### Step 2 — Lint and format

**Scope:** the first guardrail, and the one the directory itself enforces.

**Documentation to research:** the `eslint-plugin-obsidianmd` README and its configuration document (which rules the scanner runs, which it keeps at error, which paths it ignores); ESLint's flat-configuration documentation; Prettier's documentation.

**Install:** `pnpm add -D -w eslint typescript-eslint eslint-plugin-obsidianmd prettier`, plus the supporting packages their current documentation names (a loader for a TypeScript-format ESLint config; the package that stops ESLint and Prettier disagreeing)

**Required outcome:**
- One root `eslint.config.mts` applying `eslint-plugin-obsidianmd`'s recommended configuration to the plugin package and typescript-eslint's recommended rules to every package, with `parserOptions.projectService` on so type information is available to Step 4. The `obsidianmd` package version is pinned exactly: its rule semantics have changed between minor versions.
- `no-console` configured as the plugin rule set has it: `warn`, `error` and `debug` only.
- A `.prettierrc` matching the template's `.editorconfig` (tabs, single quotes), and `eslint-config-prettier` so the two tools never disagree.
- Root scripts `lint` (failing on any warning, so every Obsidian rule acts at error level), `format` and `format:check`.
- `scratch.ts` rewritten to trigger several rules deliberately, proving they are detected, then fixed until `pnpm lint` and `pnpm format:check` are clean.

**Validation:** `pnpm lint` and `pnpm format:check` clean.
**Commit:** `chore: add ESLint with the Obsidian rule set and Prettier`

### Step 3 — Strict type checking

**Scope:** TypeScript's compiler is the type checker; strict mode plus the flags the template and this specification require.

**Documentation to research:** TypeScript's official documentation on `tsconfig` compiler options, especially the `strict` family and the additional checks below.

**Required outcome:**
- A root `tsconfig.base.json` with `strict: true` and additionally `noImplicitReturns`, `noFallthroughCasesInSwitch`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noUnusedLocals`, `noUnusedParameters`, `isolatedModules`, `verbatimModuleSyntax`; `lib` includes `ES2021` and `DOM`; target `ES2021`.
- Each package's `tsconfig.json` extends the base. The core's `types` list excludes Node.
- Root script `typecheck` running `tsc --noEmit` in every package, plus a root project covering every TypeScript file outside the packages (scripts, tests, configuration).
- `scratch.ts` expanded to exercise the strict rules: implicit `any`, unchecked index access, optional property exactness, exhaustive `switch`, unused symbols; iterate until clean.

**Validation:** `pnpm typecheck`, `pnpm lint`, `pnpm format:check` clean.
**Commit:** `chore: add strict TypeScript configuration for every package`

### Step 4 — Type-aware lint rules and boundary rules

**Scope:** the second layer. Rules that use the compiler's type information to catch what the compiler alone does not, and the rules that keep the core clean.

**Documentation to research:** typescript-eslint's documentation on type-checked configurations and on `no-floating-promises`, `no-deprecated` and `switch-exhaustiveness-check`; ESLint's `no-restricted-imports`; the current documentation on detecting circular imports in a TypeScript workspace.

**Install:** the package the import-cycle check needs, as its current documentation names it

**Required outcome:**
- typescript-eslint's `strict-type-checked` configuration enabled for every package; `@typescript-eslint/no-deprecated` raised to `error` (Obsidian deprecates APIs and the linter can see it); `no-floating-promises` at `error`; `no-unsafe-type-assertion` at `error`, so a cast that overrides the checker needs a suppression comment like any other.
- Boundary rules in the core package: `no-restricted-imports` forbidding `obsidian`, `electron`, `@codemirror/*`, `@lezer/*` and every Node built-in; a rule forbidding imports from another slice's internals (anything under `packages/core/src/<slice>/` other than its `index.ts`).
- An import-cycle check across every package, wired into `pnpm lint`: any circular import fails it.
- `scratch.ts` expanded to trip each new rule once, then fixed.

**Validation:** all checks clean; a deliberate `import 'obsidian'` in the core fails `pnpm lint`, as does a deliberate circular import, and each is then removed.
**Commit:** `chore: add type-aware lint rules and core boundary rules`

### Step 5 — Unit tests

**Scope:** the test runner, the Obsidian shim, and coverage.

**Documentation to research:** Vitest's official documentation on workspace configuration, `resolve.alias`, coverage and `vi.useFakeTimers`; the Obsidian plugin development reference on shimming the `obsidian` module.

**Install:** `pnpm add -D -w vitest`, plus the coverage provider Vitest's current documentation names

**Required outcome:**
- A root `vitest.config.ts` (or workspace file) covering every package; `obsidian` aliased to `__mocks__/obsidian.ts` for the plugin package only — the core must not need it.
- `__mocks__/obsidian.ts`: minimal empty classes (`Plugin`, `Notice`, `TFile`, `TFolder`, `Modal`, `PluginSettingTab`, `Setting`), a `Platform` object and `normalizePath`, grown only as the plugin package's tests require.
- Coverage enabled on every run, reported to the terminal, with `coverage/` ignored by git, and a threshold in the configuration that fails the run when line coverage of `packages/core/` falls below 80%. A threshold is raised as coverage grows and never lowered to make a run pass.
- `packages/core/src/scratch.test.ts` covering every function in `scratch.ts`, including an async case using fake timers.
- Root script `test` = `vitest run`.

**Validation:** `pnpm test`, `pnpm typecheck`, `pnpm lint`, `pnpm format:check` all green.
**Commit:** `chore: add Vitest with the Obsidian shim and coverage`

### Step 6 — Structured logging

**Scope:** greppable, machine-parseable logs through a port, so the core can log without knowing where lines go.

**Documentation to research:** Section 2.4 of this specification; the JSON Lines format description; the Obsidian plugin development reference on console output levels.

**Required outcome:**
- `packages/core/src/core/ids.ts`: `newId()` returning `crypto.randomUUID()`.
- `packages/core/src/core/ports.ts`: the `LogSink` port — `write(line: LogEvent): void` — and the `ClockPort` — `now(): Date`.
- `packages/core/src/core/logging.ts`: a `LogEvent` type (`event`, `level`, `timestamp`, `correlationId?`, further fields); `createLogger(sink, clock, minimumLevel)` returning `log.info/warn/error/debug(event, fields)`; a `withCorrelation(correlationId)` helper producing a child logger whose every event carries the ID; the three-part event-name rule enforced by a `validateEventName()` helper; an unset correlation ID omitted from the object, never `null`.
- Tests: event shape; correlation ID present when set and absent (not null) when not; level filtering; event-name validation; sink receives one object per event.
- A temporary demo, `packages/core/src/demo.ts`, writing a start/complete pair and a failure to a console sink; runnable from the command line. Replaced in Step 8.

**Validation:** all checks green; the demo prints one JSON object per line with no null fields.
**Commit:** `feat(core): add structured logging with correlation IDs`

### Step 7 — Remove the validation scaffold

**Scope:** the scratch files have done their job. They are removed in one commit, now that the logging tests keep the suite non-empty.

**Required outcome:**
- `packages/core/src/scratch.ts` and `scratch.test.ts` removed with `git rm`.
- Any lint or test configuration that named them is cleaned up.

**Validation:** all checks green; the passing test count equals the logging tests from Step 6.
**Commit:** `chore: remove validation scaffold`

### Step 8 — The application core

**Scope:** the core's skeleton: ports, the operation registry, the error model, settings schema and public surface. This is the analogue of an API layer: every request into the core goes through it.

**Documentation to research:** the vertical slice architecture guide (feature folders, the `core/` and `shared/` rules, one operation spanning features); Zod's official documentation (schemas, `z.infer`, discriminated unions, `safeParse`); Section 2.5 of this specification.

**Install:** `pnpm add --filter core zod`

**Required outcome:**
- `ports.ts` completed: `NoticePort` (`notice(message)`), `SecretsPort` (`get/set/delete`), `VaultPort` (the read, write, create, rename, trash and change-notice functions the TAD names; writes take the expected previous value so a conflicting user edit can be detected), `[D3]` `StorePort` (`readFile`, `writeFileAtomic`, `appendLine`, `listFolder`, `deleteFile`), plus `LogSink` and `ClockPort` from Step 6.
- `errors.ts`: `AppError` with `errorCode`, `message`, `retryable`, `details?`; the shared codes `CORE_TARGET_NOT_FOUND`, `CORE_INPUT_INVALID`, `CORE_CONFIRMATION_REQUIRED`, `[D3]` `CORE_STORE_UNAVAILABLE` (domain per D4).
- `api.ts`: the `Result` type from Section 2.5; `defineOperation({ name, version, request: ZodSchema, outcome: ZodSchema, handler })`; a registry; `execute(request)` that validates the request against the schema for that name and version, generates a `correlationId` when none is supplied, runs the handler with a correlated logger, validates the outcome, and never lets an exception escape — any thrown error becomes `{ ok: false }` with `CORE_INTERNAL_ERROR` and is logged with the stack. `query()` likewise for read-only requests. An `actor` field (`user` | `application`) on every request.
- `settings.ts`: the Zod schema for user settings with defaults, and `parseSettings(unknown)` returning validated settings or the defaults for a corrupt file (never throwing).
- `shared/dates.ts`: `toIsoUtc(date)` and `fromIso(string)`; the folder exists for later cross-slice helpers.
- `core/core/README.md`: the decision rule for what belongs in `core/core/`, `shared/`, a slice or the plugin package, with a table of examples drawn from the TAD's planned slices.
- `core/core/testing/`: an in-memory adapter for every port and a pretend clock (Section 2.6), used by every core test and excluded from the public surface.
- `index.ts`: the public surface — `createCore(adapters)` taking one adapter per port and returning `{ execute, query }` — and nothing else exported.
- `scripts/check-core-boundary.ts`: fails if `packages/core/package.json` depends on `obsidian`, or if any file under `packages/core/src/` mentions `obsidian`; wired into `pnpm lint`.
- Tests: `execute` rejects a malformed request before the handler runs; a thrown handler error becomes a failed `Result`, is logged, and does not propagate; outcomes are validated; the `correlationId` on the result equals the one on every log line; `parseSettings` returns defaults for garbage; the boundary script fails on a planted import.
- `[D2]` `packages/test-client/`: a file-based adapter for every port (the file system for the vault and store, a real or pretend clock, printing for notices, memory for secrets) and a `createTestClient(vaultPath)` that wires them into `createCore`; a command line, `<vaultPath> <operationName> [jsonPayload]`, that runs any registered operation or query and prints its `Result` as JSON. A scenario test runs one operation through it against `test-vault/`.
- The Step 6 demo removed with `git rm`.

**Validation:** all checks green; `pnpm lint` includes the boundary check; suppression loop.
**Commit:** `feat(core): add ports, operation registry, error model and settings schema`

### Step 9 — The plugin package

**Scope:** a loadable plugin that wires Obsidian to the core, with a production build the directory can reproduce.

**Documentation to research:** the Obsidian plugin development reference on lifecycle, `register*` helpers, settings (declarative definitions at 1.13 and the `display()` fallback below it), secret storage, the manifest and the guidelines table; Obsidian's official developer documentation for the same topics; esbuild's documentation on `external`, `format`, `target` and `metafile`.

**Install:** `pnpm add --filter plugin -D obsidian esbuild`, with `obsidian` pinned to an exact version whose API matches `{{MIN_OBSIDIAN_VERSION}}` or later, plus whatever the official template's esbuild configuration imports to list Node built-ins as externals

**Required outcome:**
- `packages/plugin/src/main.ts`: a default-exported class extending `Plugin`. `onload` does only registration: commands, the settings tab, the ribbon icon if any, and `createCore` with the adapters; vault scans or anything expensive run inside `this.app.workspace.onLayoutReady(...)`; every listener, interval and DOM event goes through `registerEvent`, `registerInterval`, `registerDomEvent` or `register`; `onunload` releases nothing by hand that was registered, and load/unload are idempotent so hot reload works. `onExternalSettingsChange` reloads settings.
- `packages/plugin/src/adapters/`: one file per port. `LogSink` → `console.debug/warn/error` by level (`[D3]` plus an append to the log file through the store adapter); `ClockPort` → `Date`; `NoticePort` → `new Notice(...)`; `SecretsPort` → `this.app.secretStorage` with a fallback when absent; `VaultPort` → `processFrontMatter` for front matter, `vault.process` for bodies, the metadata cache for reads, `fileManager.renameFile` and `trashFile`, `normalizePath` on every path, `instanceof TFile` never a cast, and one write at a time per file via a per-file promise queue; `[D3]` `StorePort` → the vault adapter API for the hidden store folder, writing small files via temporary file and rename.
- `packages/plugin/src/settings/`: `DEFAULT_SETTINGS` (including the minimum log level from Section 2.4), the load/save helpers from Section 2.7, and a settings tab that uses declarative definitions when `{{MIN_OBSIDIAN_VERSION}}` ≥ 1.13.0 and the imperative `display()` otherwise; no top-level heading; sentence case; save on change.
- One command, `ping`, that runs a trivial core operation and shows its outcome as a notice — proof that the wiring works end to end. No default hotkey; the plugin ID not included in the command ID.
- `packages/plugin/esbuild.config.mjs`: entry `src/main.ts`, `bundle: true`, `format: 'cjs'`, `target: 'es2021'`, externals per Section 2.1, `treeShaking: true`, `outfile` the repository-root `main.js`; dev build with inline source maps and watch; production build minified without source maps; a `metafile` written for the Step 11 size budget. Root `build` runs the type check then this production build; root `dev` runs the watch build.
- `styles.css` present (empty if nothing is styled yet); class names prefixed with `{{PLUGIN_ID}}-`; no inline styles, no `innerHTML`.
- `test-vault/` committed with a minimal fixture and a `.hotreload` marker; a documented way to point the dev vault at the build (directory symlink, or copying output, or the Obsidian command-line `plugin:reload`).
- Plugin unit tests, against the shim: settings load with defaults and survive a `null` `loadData()`; the vault adapter queues writes to one file; the secrets adapter falls back when secret storage is absent; the `ping` command calls `execute` with `actor: 'user'`.

**Validation:** `pnpm build` produces `main.js` at the root with no `obsidian` code bundled; the plugin loads in the development vault, the `ping` command shows its notice, and disabling then re-enabling leaves no console error; all checks green; suppression loop.
**Commit:** `feat(plugin): add plugin lifecycle, port adapters, settings and production build`

### Step 10 — Tests inside a real Obsidian

**Scope:** proof that the plugin works at both ends of the supported range, run automatically.

**Documentation to research:** the `wdio-obsidian-service` README and its sample plugin (installing the service, `browserVersion` values `earliest` and `latest`, the helpers for commands and vault reset, the Linux virtual framebuffer requirement); the Obsidian plugin development reference on real-Obsidian testing.

**Install:** `pnpm add -D -w wdio-obsidian-service`, plus the WebdriverIO packages its README names for the runner, the test framework and the reporter

**Required outcome:**
- `e2e-tests/wdio.conf.mts` configured for two capabilities, `earliest` and `latest`, each sandboxing a copy of `test-vault/` and installing the built plugin.
- `e2e-tests/smoke.e2e.ts`: the plugin is enabled; the `ping` command runs and its notice appears; the settings tab opens, and a setting changed there is saved and read back; the vault adapter writes front matter to a fixture note, and a write whose expected previous value no longer matches is reported as a conflict, not applied; `[D1 default]` the same passes under mobile emulation; disabling and re-enabling the plugin produces no console errors.
- Root script `e2e`; a GitHub workflow running it on every merge to `main` and nightly, with the harness's Obsidian download cache persisted between runs.
- A `check_for_new_obsidian` workflow that triggers the e2e run when a new Obsidian version is published, following the sample plugin's pattern.

**Validation:** `pnpm e2e` passes locally against both versions; the workflow passes on a pushed branch; suppression loop.
**Commit:** `test(e2e): add real-Obsidian smoke tests at the minimum and latest versions`

### Step 11 — Release automation and directory readiness

**Scope:** everything the community directory's automated review will check, enforced before a release exists.

**Documentation to research:** the Obsidian plugin development reference on release mechanics, the release workflow, attestation, the scanner's checks and common failures; Obsidian's official documentation on releasing with GitHub Actions and on submission requirements.

**Required outcome:**
- `scripts/version-bump.ts` (from the template, adjusted for the workspace and rewritten in TypeScript): copies the new version to `manifest.json` and adds a `versions.json` entry when `minAppVersion` changed; `.npmrc` sets `tag-version-prefix=""` so tags carry no `v`.
- `scripts/check-manifest.ts` (root script `check:manifest`): `id`, `name`, `description` and `version` satisfy the Section 3.1 rules; `fundingUrl` absent or real; `versions.json` valid JSON and consistent; `package.json` version equals the manifest version.
- `scripts/check-bundle-size.ts`: reads the esbuild metafile and fails above a budget (default 1 MB, generous against the scanner's reported limit).
- A test beside each script (`*.test.ts`), run by `pnpm test`: each check passes on valid input and fails, naming the problem, on each kind of broken input.
- `.github/workflows/ci.yml`: on every push and pull request — `pnpm install --frozen-lockfile`, `lint`, `format:check`, `typecheck`, `test`, `build`, `check:manifest`, `check-bundle-size`, `pnpm audit --audit-level=high`, and the official `scanner-lint` action so the directory's own rules run in CI.
- `.github/workflows/release.yml`: on a version tag — install, build, attest `main.js`, `manifest.json` and `styles.css` individually, and create a **draft** GitHub release with those three files attached individually, never zipped.
- `.github/dependabot.yml` for `npm` and `github-actions`, with `obsidian` pinned exactly in `devDependencies` so bumps are deliberate.
- `NOTICES.md` listing every third-party dependency licence that requires attribution (empty section if none yet).

**Validation:** `pnpm check:manifest` and the size check pass; CI is green on a pushed branch; a dry-run tag on a throwaway branch produces a draft release with the three attested assets, then is deleted; suppression loop.
**Commit:** `chore(release): add version bump, manifest and size checks, CI and attested release workflow`

### Step 12 — README, global rules and final validation

**Scope:** document the foundation for humans and encode its conventions for every future agent session. Both documents follow a template so that every repository built from this specification reads the same way: the same sections in the same order, the same formatting, the same voice. The content differs per application; the shape does not.

The two files divide the material between them and never repeat it. `CLAUDE.md` is normative: every rule, convention and constraint an agent must obey lives there and nowhere else. `README.md` is descriptive: how to install, run and use the plugin, for a human reader — and it carries the disclosures the directory requires (network use, accounts, payment, outside-vault access, server-side telemetry, third-party licences). Where a reader of one file needs something held by the other, the file carries a one-line pointer to it, never a restatement.

**Documentation to read:** `.agents/templates/template_readme.md` and `.agents/templates/template_claude_md.md`, in full, together with the Appendix of this specification, before writing either file. **Documentation to research:** the Obsidian plugin development reference on README disclosures.

**Required outcome:**
- `README.md`, following `.agents/templates/template_readme.md` with its stack blocks taken from the Appendix — its section order, headings, formatting and voice are kept exactly; the content describes the product the PRD and TAD define, is written from the PRD, the TAD, this specification and the code only, states nothing beyond them, and includes every disclosure the developer policies require.
- `CLAUDE.md`, following `.agents/templates/template_claude_md.md` with its stack blocks taken from the Appendix — its section order, headings, formatting and voice are kept exactly; the rules are generated from Section 2 of this specification, the PRD, the TAD and every standing rule the plan establishes, with the architecture section showing the workspace tree and the application's planned slices, the error handling section carrying the D4 domain list, and the development commands section carrying Section 2.8. The template's code examples are kept as written: they show format and claim nothing about this application. Real code is pointed to, never copied: the template's reference table names, for each pattern the repository already implements, the file to imitate. Long reference material goes in `.agents/reference/`, not in `CLAUDE.md`.
- Where a template section has nothing to say for this application, it is kept with a one-line statement to that effect rather than removed, so the shape stays stable across repositories.
- `.claude/commands/validate/validate.md`: its Checks section written with each command followed by its expected result, using only the tools Section 2.3 allows:
  - the scripts in Section 2.8, in that order
  - a bundle check: `main.js`, `manifest.json` and `styles.css` at the root, `obsidian` left external, and `main.js` within the Step 11 size budget
  - `[D2]` one operation run through the test client's command line against a copy of `test-vault/`, confirming that its log lines carry the `correlationId` of its `Result`

**Validation:** `/validate:validate` passes end to end; every standing rule in the plan appears in `CLAUDE.md`; and every fact `CLAUDE.md` states is checked against the repository — each path in the architecture tree and the reference table exists (a planned slice is checked against the TAD instead), each version in the tech stack matches the lockfile, and each development command has been run and succeeded (one that would create a version or a release is confirmed to exist instead). `README.md` is checked the same way: what it says of the product against the PRD and TAD, and its commands, settings table and disclosures against the repository.
**Commit:** `docs: add README and global development rules (CLAUDE.md)`

---

## 6. Definition of done

The foundation is complete when all of the following hold:

- [ ] `pnpm lint`, `pnpm format:check` and `pnpm typecheck` report zero issues in every package.
- [ ] `pnpm test` passes with coverage reported and its thresholds met; `pnpm e2e` passes against both the minimum and the latest Obsidian.
- [ ] No suppression comment exists without a documented reason on the same line, and none disables a security or `obsidianmd/*` rule (the suppression search in Section 5.0 returns nothing unjustified).
- [ ] `pnpm build` produces `main.js` at the root with no Obsidian, Electron, CodeMirror or Node code bundled, within the size budget.
- [ ] The core package has no dependency on `obsidian` and the boundary check proves it.
- [ ] The plugin loads in the development vault, the `ping` command works, and disable/enable leaves no console error.
- [ ] `check:manifest` passes; CI and the release workflow are green; a draft release carries three individually attested assets.
- [ ] Every log line is one JSON object with a three-part event name; no line carries a `null` correlation ID, note content or a secret.
- [ ] `CLAUDE.md` and the manifest describe the repository as it actually is; `README.md` describes the product the PRD and TAD define, states nothing beyond them and carries every required disclosure.
- [ ] One commit per step, in sequence, each passing validation at the time it was made.
- [ ] The plan records the resolved Decision Register with its justifications.

---

## 7. Expected final layout

```
.
├── .agents/
│   ├── PRD.md · TAD.md
│   ├── reference/  (ai_optimized_codebase_setup_obsidian_plugin, vertical-slice-architecture-setup-guide, obsidian-community-plugin-development)
│   └── templates/  (template_readme, template_claude_md)
├── .claude/commands/  (git/commit, validate/validate)
├── .github/
│   ├── workflows/  (ci, release, e2e, check_for_new_obsidian)
│   └── dependabot.yml
├── packages/
│   ├── core/src/   (core/{ports,api,errors,logging,ids,settings,testing/,README}, shared/dates, index)
│   ├── plugin/src/ (main, adapters/, settings/) + esbuild.config.mjs
│   └── test-client/                  [D2 only]
├── __mocks__/obsidian.ts
├── e2e-tests/  (wdio.conf, smoke.e2e)
├── test-vault/
├── scripts/  (check-core-boundary, check-manifest, check-bundle-size, version-bump)
├── manifest.json · versions.json · styles.css
├── package.json · pnpm-workspace.yaml · pnpm-lock.yaml · tsconfig.base.json
├── eslint.config.mts · .prettierrc · vitest.config.ts · .nvmrc · .npmrc
├── .gitignore · LICENSE · NOTICES.md
├── CLAUDE.md · README.md
```

---

## 8. Provenance

The step sequence — validation tooling first, then logging, then the application skeleton, then packaging, then the environment-level tests, then release and documentation — and the principle of researching official documentation before configuring each tool come from Cole Medin's Dynamous Agentic Coding Live Workshop #2, "Creating an AI-Optimized Codebase", and its instructor guide. That workshop builds a Python web service; this specification adapts its principles to a TypeScript Obsidian plugin as the guide invites, and departs from it in these ways: the compiler is the first type-safety layer and type-aware lint rules the second, because TypeScript carries its own types; one linter hosts both the directory's rules and the type-aware rules; the runtime is Obsidian's, so tests run under Node and inside a real Obsidian rather than in a container; there is no server, database or container, so the packaging step is a bundle and a release the directory can verify; the core is separated from the host through ports so it can be tested without Obsidian; the tooling and `.gitignore` are in place from day 0; a structured `Result`/`AppError` error model replaces thrown exceptions; the suppression loop runs after every step from Step 8; the Decision Register isolates the few application choices; and `CLAUDE.md` is written at the end from the fixed conventions.

---

## Appendix — Stack blocks for README.md and CLAUDE.md

The README and `CLAUDE.md` templates are shared by every kind of project. Each `[Stack block: name]` slot in them is filled in Step 12 with the block of the same name below. A block's own square-bracket slots are filled from the PRD, the TAD and the code, like any other slot. If a slot names a block that is not below, stop and report it; never write the block yourself. A block that says "Not applicable" is kept with that line, so the shape stays the same across repositories.

### CLAUDE.md blocks

#### correlation-ID rule

````markdown
[The correlation-ID rule for this application, beginning: `correlationId` on every log line an operation writes]
````

#### secret storage rule

````markdown
Use Obsidian's secret storage; never store credentials in plaintext
````

#### type safety rules

````markdown
- Full type annotations on every function signature
- The compiler's strict mode and the type-checked lint rules must both pass
- No `// eslint-disable` or `// @ts-` comment without a documented reason on the same line, and never one that disables a security or `obsidianmd/*` rule
````

#### documentation comment rule

````markdown
**TSDOC ON ALL EXPORTED FUNCTIONS**

- `/** … */` with `@param` and `@returns`
````

#### tech stack

````markdown
### Application core

- **Language:** [language and version, with the Node version used for build and tests]
- **Package manager:** [package manager and version, with the workspace's packages]
- **Framework:** Not applicable — the core is plain TypeScript behind ports, with [schema library and version floor] for validation
- **ORM:** Not applicable — notes are reached only through the vault port
- **Logging:** [logging mechanism (output format)]
- **Database:** Not applicable — [where plugin-owned data is kept]
- **Lint/format:** [linter, rule sets and formatter, with versions (indentation, quote style, line width)]
- **Type checking:** [the compiler mode and the type-checked lint configuration (both required)]
- **Testing:** [unit test runner and real-Obsidian test harness, with version floors]

### Plugin

- **Obsidian API:** [`obsidian` types version; minimum app version; desktop-only or mobile-capable]
- **Bundler:** [bundler and the single file it produces]
- **Interface:** [the settings approach and the interface elements the plugin uses]
- **Data access:** Ports only (the plugin package supplies one adapter per port; nothing else touches the vault)
````

#### architecture

````markdown
```
packages/
├── core/src/               # Application core — never imports `obsidian`, Electron or Node
│   ├── core/               # Universal infra — required by all slices
│   │   ├── ports.ts        # The port interfaces
│   │   ├── api.ts          # Operation registry, versions, Result
│   │   ├── errors.ts       # AppError and error codes
│   │   ├── logging.ts      # Logger, correlation ID, LogSink port
│   │   ├── ids.ts          # Identifier generation
│   │   ├── testing/        # In-memory adapters and a pretend clock for every test
│   │   └── README.md       # The decision rule for what belongs here
│   ├── shared/             # Cross-feature utilities (3+ slice rule)
│   ├── {feature}/          # Vertical slices: [the slice names from the TAD]
│   │   ├── operations.ts
│   │   ├── rules.ts
│   │   ├── schemas.ts
│   │   ├── README.md
│   │   └── *.test.ts       # Colocated unit tests (no Obsidian, no file system)
│   └── index.ts            # The core's public surface
├── plugin/src/             # The Obsidian plugin — thin
│   ├── main.ts             # Lifecycle only
│   ├── adapters/           # One adapter per port, using Obsidian's API
│   └── settings/           # The settings tab
[└── any further package this application has, one line each with its purpose]
__mocks__/obsidian.ts       # The shim unit tests use in place of `obsidian`
e2e-tests/                  # Tests inside a real Obsidian
test-vault/                 # Fixture vault for development and e2e tests
scripts/                    # Build checks, version bump, manifest check
```

**Rules:**

- `packages/core/` — never imports `obsidian`, Electron or a Node module; the boundary check fails the lint step if it does
- `core/core/` — infrastructure only; never imports feature slices or `shared/`
- `shared/` — only code used by **3 or more** feature slices; never feature-specific logic
- Each feature slice is self-contained; a slice uses only what another slice publishes through its `index.ts`
- `main.ts` does lifecycle and nothing else
- [The process-model rule for this application: what Obsidian loads, and any other program built from this repository]
````

#### naming

````markdown
- Functions, variables and object properties: `camelCase`
- Types, classes and Zod schemas: `PascalCase`
- Fields: verbose — `customerId`, `orderStatus`, `createdAt` (never `id`, `status`)
- Constants: `UPPER_SNAKE_CASE`
````

#### documentation comments

````markdown
### TSDoc (required on all exported functions)

```ts
/**
 * Finds a single customer by its identifier.
 *
 * Reads the customer's note through the vault port and returns its
 * validated fields if the note exists.
 *
 * @param customerId - Identifier of the customer to find.
 * @param vault - The vault port the note is read through.
 * @returns The customer if found, `null` otherwise.
 */
export async function findCustomerById(
	customerId: string,
	vault: VaultPort,
): Promise<Customer | null> {
```
````

#### ORM models

````markdown
Not applicable — a plugin has no ORM. Its data shapes are the schemas below.
````

#### schemas

````markdown
```ts
import * as z from 'zod';

export const CustomerSchema = z.object({
	customerId: z.string(),
	customerStatus: CustomerStatusSchema,
	createdAt: z.string(),
});

export type Customer = z.infer<typeof CustomerSchema>;
```

> **Vault data exception:** Fields written to a note keep exactly the names the PRD fixes (e.g., `id`, `status`), however short. Variables, properties and types inside the code must always use verbose names. When a schema describes vault data, its keys are the PRD's names and the code maps them to verbose names where it reads them.
````

#### logger setup

````markdown
```ts
// `log` is the logger an operation is given; it already carries the correlationId
log.info('orders.checkout.validation_started', { orderId });
```
````

#### logging example

````markdown
**Never log secrets, licence keys, credentials, or note contents.**

```ts
// Operation start + completion pair
log.info('orders.checkout.validation_started', { orderId });

const validation = validateOrder(order);

log.info('orders.checkout.validation_completed', {
	orderId,
	lineItemCount: validation.lineItemCount,
	totalAmount: validation.totalAmount,
});

// Error with structured context
log.error('orders.checkout.validation_failed', {
	orderId,
	errorCode: 'ORDERS_INPUT_EMPTY_CART',
});
```

[How the correlation ID is set and carried, beginning: **`correlationId`** is generated by `execute` / `query` when the caller supplies none, and reaches every log line through the logger each operation is given.]
````

#### test locations

````markdown
| Test type              | Location                     | Runner                                                |
| ---------------------- | ---------------------------- | ----------------------------------------------------- |
| Core unit              | beside the code, `*.test.ts` | Vitest, no shim                                       |
| Plugin unit            | beside the code, `*.test.ts` | Vitest, `obsidian` aliased to `__mocks__/obsidian.ts` |
| Inside a real Obsidian | `e2e-tests/`                 | `wdio-obsidian-service`, `earliest` and `latest`      |
[one row per further test type this application has]
````

#### test rules

````markdown
- `e2e-tests/` is reserved for tests inside a real Obsidian — never place unit tests there
- Core unit tests: no Obsidian, no file system, no network -- the in-memory adapters and pretend clock in `core/core/testing/` stand in for every port
- Plugin unit tests run against the shim; the shim reflects assumptions, so the real-Obsidian tests are what prove the integration
- Test names: `describe` the function, `it` states the condition and the expected result
- Async tests need no special marker -- an `async` test function is awaited
- In-memory adapters live in `core/core/testing/` -- always use them, never write a second stand-in for a port inside a slice
- Coverage thresholds fail the test run when coverage falls; raise a threshold as coverage grows, never lower one to make a run pass
````

#### unit test example

````markdown
```ts
describe('validateOrder', () => {
	it('returns ORDERS_INPUT_EMPTY_CART when the order has no line items', () => {
		const validation = validateOrder({ orderId: 'order-1', lineItems: [] });

		expect(validation).toEqual({
			ok: false,
			error: expect.objectContaining({
				errorCode: 'ORDERS_INPUT_EMPTY_CART',
				retryable: false,
			}),
		});
	});
});
```
````

#### second test example

````markdown
### Real-Obsidian test example

```ts
describe('place order command', () => {
	it('shows the confirmation notice when the order is placed', async () => {
		await browser.executeObsidianCommand('[plugin id]:place-order');

		await expect($('.notice')).toHaveText(expect.stringContaining('Order placed'));
	});
});
```
````

#### error model

````markdown
```ts
return {
	ok: false,
	error: {
		errorCode: 'ORDERS_INPUT_EMPTY_CART',
		message: 'An order must contain at least one line item.',
		retryable: false,
	},
};
```

- Inside the core, failures are values: return a failed result with an `AppError`; never throw across the core's boundary
- Messages shown to the user are **intentionally plain**
- An `AppError`'s `message` is a diagnostic for the log; what the user sees comes from the messages module, keyed by `errorCode`
- Notices must be non-sensitive; put full diagnostics in structured logs only
- `execute` / `query` convert any thrown error into a failed `Result` with the internal-error code automatically
- `execute` / `query` attach the `correlationId` to every `Result`; handlers never pass it
- Event handlers in the plugin never throw, and no promise is left floating

**`Result` shape** (canonical across all operations and queries):

```ts
type Result<TOutcome> =
	| { ok: true; correlationId: string; outcome: TOutcome }
	| { ok: false; correlationId: string; error: AppError };

interface AppError {
	errorCode: string; // [the error-code format]
	message: string;
	retryable: boolean;
	details?: Record<string, unknown>;
}
```
````

#### minimum patterns

````markdown
a documented exported function, a start + completion log pair, a returned `AppError`, an operation definition, a port adapter, a unit test and a real-Obsidian test
````

#### development commands

````markdown
pnpm install                                               # Install all dependencies

# Running the plugin
pnpm dev                                                   # Watch build into the development vault
[one line per additional program, such as a headless client]

# Database
# Not applicable — a plugin has no database

# Tests
pnpm test                                                  # Unit tests with coverage (fast)
pnpm e2e                                                   # Tests inside a real Obsidian (earliest and latest)

# Lint, format, type checking (run all before committing)
pnpm lint && pnpm format:check
pnpm typecheck

# Build and release
pnpm build                                                 # Production build; writes main.js at the root
pnpm check:manifest                                        # Manifest and versions.json rules
[version-bump command]                                     # Bump the version in every file that carries it

# Containers
# Not applicable — a plugin runs inside Obsidian
````

#### fourth agent instruction

````markdown
**Keep the core free of host imports** per Section 3
````

#### fifth agent instruction

````markdown
**Error codes and failed results** per Section 7
````

### README blocks

#### standard features

````markdown
- **Structured JSON logs** — [the correlation IDs this application carries, beginning with `correlationId` on every log line an operation writes]; contextual fields such as `errorCode` where applicable
- **Diagnostic command** — one command that confirms the plugin and its application core respond
````

#### architecture diagram

````markdown
```
┌─────────────────────────────────────────────────────────┐
│  Obsidian  (minimum version [version] · [platforms])    │
└──────────────────────┬──────────────────────────────────┘
                       │ plugin API
┌──────────────────────▼──────────────────────────────────┐
│  Plugin  (lifecycle · settings · one adapter per port)  │
└──────────────────────┬──────────────────────────────────┘
                       │ ports
┌──────────────────────▼──────────────────────────────────┐
│  Application core  (no dependency on Obsidian)          │
│  [the feature slices]                                   │
└──────────────────────┬──────────────────────────────────┘
                       │ [the link to the next tier]
[one box per further tier, such as a headless client or a remote service, in the same form]
┌──────────────────────▼──────────────────────────────────┐
│  The vault  (Markdown notes)                            │
│  [where plugin-owned data is kept]                      │
└─────────────────────────────────────────────────────────┘
```

[The process model — what Obsidian loads, and any other program built from this repository — and that the code is organised as vertical slices under `packages/core/src/`. The repository tree is in `CLAUDE.md`, Section 3.]
````

#### installation

````markdown
[How a user installs the plugin: from Obsidian's community plugin directory once it is listed there, or by copying `main.js`, `manifest.json` and `styles.css` from the latest release into the vault's plugin folder.]

To work on the plugin:

1. Clone the repository and change into it.
2. Install dependencies.
3. No environment file is needed.
4. Build the plugin into the development vault and enable it there.

The commands for each step are in [`CLAUDE.md`, Section 9](CLAUDE.md).
````

#### running

````markdown
Run the watch build and open the development vault in Obsidian; the commands are in [`CLAUDE.md`, Section 9](CLAUDE.md).

The plugin reloads in the development vault after each build. Its log lines appear in Obsidian's developer console[, and where else they are written].
````

#### health checks

````markdown
Run **[the diagnostic command's name]** from the command palette. A notice confirms that the plugin and its application core respond.

[With a headless client: the one command that runs the same check without Obsidian, in a `bash` block.]
````

#### API reference

````markdown
> The plugin has no HTTP API. Its internal API is the set of operations and queries below, called in-process through `execute` and `query`.

### Authentication

Not applicable — operations are called in-process, by the plugin and by [any other host this application has].

### Operations

[One subsection per operation or query. Each subsection: a `####` heading of the form `` `name` (version n) — What it does ``, one sentence, the request as a JSON block, then one JSON result block per distinct result, labelled in bold:]

#### `placeOrder` (version 1) — Create an order

Record an order for processing.

```json
{
  "name": "placeOrder",
  "version": 1,
  "actor": "user",
  "payload": { "customerId": "…", "lineItems": [ … ] }
}
```

**Result** (succeeded):

```json
{
  "ok": true,
  "correlationId": "7c4a8d09-ca72-4024-b234-2d6e9a872b51",
  "outcome": { "orderId": "550e8400-e29b-41d4-a716-446655440000", "status": "queued" }
}
```
````

#### error codes

````markdown
All errors follow the format [the error-code format]. The `retryable` field indicates whether the same request may succeed if tried again unchanged.

| Code                       | Retryable | Meaning                         |
| -------------------------- | --------- | ------------------------------- |
| [`DOMAIN_CATEGORY_DETAIL`] | [Yes/No]  | [one line]                      |
| `BILLING_PROVIDER_TIMEOUT` | Yes       | Payment provider call timed out |
````

#### configuration

````markdown
All configuration is through the plugin's settings tab in Obsidian. No environment file is needed.

| Setting     | Default       | Description                                  |
| ----------- | ------------- | -------------------------------------------- |
| [`Setting`] | [default]     | [one line — one row per setting]             |

[Where the settings are stored, and where any further configuration reference lives, e.g. a TAD section.]

**Database connection strings:** Not applicable — a plugin has no database. [Where plugin-owned data is kept.]
````

#### disclosures

````markdown
Obsidian's developer policies require each of the following to be stated here.

- **Network use** — [None, or each remote service the plugin contacts, when, and why it is needed]
- **Accounts** — [None, or which features need an account and with whom]
- **Payment** — [None, or which features need payment]
- **Files outside the vault** — [None, or what is read or written outside the vault and why]
- **Telemetry** — [None, or what is collected, where it is sent, and how to turn it off]
- **Third-party licences** — [where the licence notices of bundled and copied code are listed]
````

#### logs answer

````markdown
Logs are structured JSON, one object per line, written to [where log lines go]. Each entry carries [the correlation IDs this application carries, beginning with `correlationId`] and `errorCode` where applicable. [Where to look for ad-hoc investigation, e.g. Obsidian's developer console.]
````
