# Integration Branch Setup

## Workflow

This project uses a branch-per-task workflow built around a permanent local `integration` branch that sits between `main` and short-lived work branches. Each piece of work is developed in its own git worktree at `worktrees/<type>-<name>`, on a branch named `<type>/<name>` branched off `integration`. The type is `feature`, `fix`, `chore` or `docs`, and it defaults to `feature`. Use `feature` for new behaviour, `fix` for correcting broken behaviour, `chore` for maintenance that changes no behaviour, and `docs` for documentation only. When the work is complete the branch merges back into `integration` via a `--no-ff` merge commit and the worktree and work branch are cleaned up. Merging `integration` into `main` is a separate manual process, deliberately out of scope of the two commands below.

Branch naming note: the branch prefix is the work type, such as `feature/`, never `integration/`. Git stores refs in a path hierarchy, so a branch named `integration` and a branch named `integration/<x>` cannot coexist — git treats `refs/heads/integration` as a file that blocks `refs/heads/integration/` from being a directory. Using `<type>/<name>` keeps the long-lived `integration` branch and per-task children compatible.

Two custom slash commands automate this workflow and depend on a fixed set of project conventions. `/new-worktree [type] <name>` creates the worktree and branch off `integration` and installs dependencies via `uv sync`. `/merge-worktrees [type] <name>` switches the main repo to `integration`, merges the work branch in with `--no-ff`, runs the validation suite, and on success removes the worktree and deletes the work branch. For a given piece of work, the two commands must receive the same type and name. Both commands hardcode these assumptions: the project is Python managed by `uv` (`pyproject.toml` at the repo root); a local `integration` branch already exists, ideally with an `origin/integration` upstream so the warn-only fetch staleness check has something to compare against; all worktrees live under `worktrees/` at the repo root and that folder is ignored by git; the project source lives under `app/`; and `pytest`, `mypy`, and `pyright` are declared as project dev dependencies so they run under `uv run`. The project has no web server, no health check, and no port logic.

## A. One-time setup

Complete every step below before invoking `/new-worktree` or `/merge-worktrees` for the first time. Each step exists to satisfy a precondition built into one or both commands.

### Step 1 — Verify you are in the project root

```
pwd
```

You should see your repo's root path. Every step below runs from here.

### Step 2 — Verify the project is managed by Python + uv

```
test -f pyproject.toml && echo "OK" || echo "MISSING pyproject.toml"
```

Neither command will run without a `pyproject.toml` at the repo root. If it is missing, run `uv init` to convert the project before continuing.

### Step 3 — Verify uv is installed

```
uv --version
```

If `uv` is not found, install it (see https://docs.astral.sh/uv/getting-started/installation/) before continuing.

### Step 4 — Confirm the repo is clean

```
git status
```

It should show `nothing to commit, working tree clean`. If it does not, commit, stash, or discard local changes before continuing.

### Step 5 — Switch to `main` and update

```
git switch main
git pull
```

All project-wide setup below happens on `main` so that `integration` inherits it.

### Step 6 — Verify the application source lives under `app/`

```
test -d app && echo "OK" || echo "MISSING app/"
```

Create the `app/` directory and move your project source into it before continuing. Commit the change on `main`.

### Step 7 — Verify `pytest`, `mypy`, and `pyright` are declared dev dependencies

Open `pyproject.toml` and confirm all three are listed (typically under `[dependency-groups]` or `[project.optional-dependencies]`). If any are missing, add them:

```
uv add --dev pytest mypy pyright
```

Commit the resulting changes to `pyproject.toml` and `uv.lock` on `main` before continuing.

### Step 8 — Add ignore rules

```
cat >> .gitignore <<EOF
worktrees/
.venv/
__pycache__/
.pytest_cache/
.mypy_cache/
EOF
```

`/new-worktree` creates every worktree under `worktrees/<type>-<name>`. The `worktrees/` rule keeps worktree contents (including each `.venv`) out of the parent repo's `git status`. The other entries cover artifacts that `uv sync`, `pytest`, and `mypy` will create at the main repo root if you ever run them there. Without these, `/merge-worktrees` Step 10 will block on a "dirty main repo" condition that has nothing to do with your actual changes.

If you prefer a personal-only ignore that is not committed to the repo, append the same five lines to `.git/info/exclude` instead and skip Step 9.

**Pytest config caveat:** if you use `[tool.pytest.ini_options]` in `pyproject.toml`, do not put `worktrees` in `testpaths` or `rootdir`. `/merge-worktrees` Step 14 runs `pytest --ignore=worktrees`, which suppresses default discovery into that directory, but `testpaths` overrides `--ignore`. With a `testpaths` that resolves under `worktrees/`, the merge command will fail with a confusing pytest collection error.

### Step 9 — Commit the `.gitignore` change on `main`

```
git add .gitignore
git commit -m "chore: ignore local worktrees folder"
```

### Step 10 — Create the `integration` branch off `main`

```
git switch -c integration
```

You are now on `integration`, which inherits the ignore rules. Both commands require this branch to exist locally.

### Step 11 — Push `integration` to GitHub

```
git push -u origin integration
```

This sets `origin/integration` as the upstream tracking branch so the warn-only `git fetch origin integration` staleness check inside both commands has a remote to compare against.

Setup is complete. Stay on `integration` for normal planning. Use `/new-worktree [type] <name>` to start a piece of work and `/merge-worktrees [type] <name>` to finish it.
