# Execution Manifest: pubmed-lib 1.0 Transformation

manifest_id: pubmed-lib-1-0-transformation  
version: 1  
spec_source: Obsidian `PubMedLib/Transformation Spec.md` (2026-06-09 grill session)

## Goal

Ship `pubmed-lib` **1.0.0-alpha** (deterministic core library) then **1.0.0** (FastMCP server with five literature-review tools), replacing the nbdev alpha codebase with a uv-managed `src/` layout, ≥80% test coverage, and clean public API.

## Scope

### In scope

- [ ] **M1 (`1.0.0-alpha`):** `src/pubmed_lib/` — `PubMedClient`, parser, models, rate limiting, regex affiliation/email, citation formatting, tests, docs, uv CI
- [ ] **M2 (`1.0.0`):** `src/pubmed_mcp/` — FastMCP, 5 tools, stdio + SSE, `MCP_API_KEY` auth, MCP contract tests, MCP docs, README rewrite
- [ ] Migrate packaging to **uv** + `requires-python >= 3.11`
- [ ] Remove legacy flat `pubmed_lib/*.py` modules after port
- [ ] `PROJECT.md`, `MIGRATION.md`, `CHANGELOG.md`, repo `docs/`
- [ ] Replace `.github/workflows/test.yaml` nbdev-ci with uv pytest/ruff/mypy

### Out of scope

- [ ] v1.1: Entrez session cache, RAG chunking, `pubmed_parse_affiliation` MCP tool
- [ ] MkDocs / GitHub Pages redeploy
- [ ] `[llm]` extra (PydanticAI) — **deferred to 1.0.1** unless M2 completes early
- [ ] Porting `nbs/04_retriever.ipynb` helpers
- [ ] Keeping `viz.py`, unused `data.py` constants (`INSTITUTE`, `COUNTRY`, …)
- [ ] nbdev export pipeline for new code; editing notebook `#| export` cells
- [ ] PyPI publish automation (manual tag OK for 1.0.0)
- [ ] Obsidian vault sync (manual per `docs/contributing.md` checklist)

## Constraints

- **Do not modify** `nbs/` notebook logic except adding a one-line “deprecated — see `src/`” banner to `nbs/index.ipynb` (S20)
- **Do not touch** `.env` or commit secrets
- **Env vars (core):** `ENTREZ_EMAIL` required; `ENTREZ_API_KEY` optional
- **Env vars (MCP SSE):** `MCP_API_KEY` required (≥32 chars) when `--transport sse`
- **Default deps:** no `openai`, `instructor`, `pandas`, `matplotlib`, `seaborn`, `plotly`
- **Breaking change:** clean 1.0 API; no shims for `Search`, `Result`, `Autor`
- **Rate limits:** MCP default `max_results=20`, hard cap `200`; enforce Entrez delays in core
- **Implementer runs on completion of each milestone:**

```bash
cd /Users/matu/Xcode/pubmed_lib
uv sync --all-extras --dev
uv run ruff check src tests
uv run mypy src/pubmed_lib
uv run pytest --cov=pubmed_lib --cov-report=term-missing --cov-fail-under=80
```

## Architecture alignment

- **Stack:** Python 3.11+, uv, Biopython Entrez, Pydantic v2, FastMCP (M2 only)
- **Reuse (port logic, do not import legacy):**
  - `pubmed_lib/data.py` → `SEARCH_TAGS`, `get_from_env` only
  - `pubmed_lib/parser.py` → parser logic (strip LLM, fix bugs)
  - `pubmed_lib/search.py` → Entrez call patterns for `PubMedClient`
- **Touch map:** `src/pubmed_lib/`, `src/pubmed_mcp/`, `tests/`, `fixtures/`, `docs/`, `pyproject.toml`, `.github/workflows/`, root `README.md`
- **Delete after port:** `pubmed_lib/*.py` (flat package), `setup.py`, `Pipfile`, `Pipfile.lock`, `settings.ini` (optional keep for nbdev docs only — prefer remove)

---

## Milestone 1 — `1.0.0-alpha` (core library)

| ID | Action | Target path(s) | Acceptance criterion |
|----|--------|----------------|----------------------|
| S1 | Replace packaging with uv src-layout; pin Python 3.11 | `pyproject.toml`, `NEW: .python-version`, `uv.lock` | `uv sync --dev` succeeds; `[project] name = "pubmed-lib"`, `requires-python = ">=3.11"`, `[tool.setuptools.packages.find] where = ["src"]` |
| S2 | Scaffold core package exports | `NEW: src/pubmed_lib/__init__.py` | Exports `PubMedClient`, `Article`, `Author`, `SearchResponse`, `__version__ = "1.0.0-alpha"` |
| S3 | Port env helpers | `NEW: src/pubmed_lib/config.py` | `get_from_env("email", "ENTREZ_EMAIL")` raises `ValueError` when unset; unit test passes |
| S4 | Port search field constants | `NEW: src/pubmed_lib/constants.py` | `SEARCH_TAGS` matches keys in legacy `pubmed_lib/data.py` lines 40–64; `SearchField` enum covers `Title/Abstract` → `[tiab]` |
| S5 | Implement Entrez rate limiter | `NEW: src/pubmed_lib/rate_limit.py` | `RateLimiter.acquire()` enforces delay; rejects `max_results > 200` with `ValueError`; unit test passes |
| S6 | Add PubMed XML test fixtures | `NEW: fixtures/pubmed_article_minimal.xml`, `NEW: fixtures/pubmed_article_no_keywords.xml`, `NEW: fixtures/pubmed_article_structured_abstract.xml`, `NEW: fixtures/pubmed_author_collective.xml` | Files parseable by Bio.Entrez.read in a smoke test |
| S7 | Implement ID parser | `NEW: src/pubmed_lib/parser/ids.py` | `parse_pubmed_ids(pubmed_data)` returns dict with `pubmed`, optional `doi`/`pmc`; test against minimal fixture |
| S8 | Implement article parser (bug-fixed) | `NEW: src/pubmed_lib/parser/article.py` | Handles missing `KeywordList` (empty list), structured `AbstractText`, `MedlineDate` via `int(year)`; tests for each fixture variant pass |
| S9 | Implement author parser (no LLM) | `NEW: src/pubmed_lib/parser/author.py` | Returns `Author` dict; skips `CollectiveName`; extracts email via regex; no network/import of `llm`; no `print()` calls |
| S10 | Implement Pydantic models + summary | `NEW: src/pubmed_lib/models/author.py`, `NEW: src/pubmed_lib/models/article.py`, `NEW: src/pubmed_lib/models/search.py` | `Article.summary` non-empty string; `Author.email` optional; model tests pass |
| S11 | Regex affiliation helpers | `NEW: src/pubmed_lib/affiliation.py` | `extract_email(text)` finds `user@sub.example.com`; returns `None` when absent; unit tests pass |
| S12 | Citation formatter | `NEW: src/pubmed_lib/citation.py` | `format_citation(article, style="apa")` returns non-empty str for minimal `Article`; tests for `apa`, `vancouver`, `bibtex` |
| S13 | Implement PubMedClient | `NEW: src/pubmed_lib/client.py` | `search()`, `fetch()`, `search_articles()`, `get_article()` use rate limiter; `api_key` optional; integration test with mocked `Bio.Entrez` passes |
| S14 | Wire parser pipeline | `NEW: src/pubmed_lib/parser/__init__.py` | `parse_entrez_article(dict)` → `Article`; end-to-end test from fixture dict to validated `Article` |
| S15 | Unit tests — parser | `NEW: tests/unit/test_parser_*.py`, `NEW: tests/conftest.py` | All parser edge cases from spec §Core API pass |
| S16 | Unit tests — models, affiliation, citation, rate_limit | `NEW: tests/unit/test_models.py`, `NEW: tests/unit/test_affiliation.py`, `NEW: tests/unit/test_citation.py`, `NEW: tests/unit/test_rate_limit.py` | `uv run pytest tests/unit` passes |
| S17 | Integration tests — client | `NEW: tests/integration/test_client.py` | Mocked Entrez returns fixture XML; `search_articles` returns `SearchResponse` with `truncated` flag when applicable |
| S18 | Dev tooling config | `pyproject.toml` (`[tool.pytest]`, `[tool.ruff]`, `[tool.mypy]`, `[dependency-groups] dev`) | `uv run ruff check src tests` and `uv run mypy src/pubmed_lib` exit 0 |
| S19 | M1 documentation | `NEW: docs/library.md`, `NEW: docs/models.md`, `NEW: docs/migration.md`, `NEW: MIGRATION.md`, `NEW: CHANGELOG.md`, `NEW: PROJECT.md` | Files exist; migration table maps `Search`→`PubMedClient`, `Result`→`Article` |
| S20 | Retire legacy package | Delete `pubmed_lib/*.py`, `setup.py`, `Pipfile`, `Pipfile.lock`; banner in `nbs/index.ipynb` | `import pubmed_lib` resolves to `src/pubmed_lib`; no duplicate `search.py`/`PubmedSearch.py` |
| S21 | Replace CI workflow | `.github/workflows/test.yaml` | Workflow runs `uv sync --dev`, `ruff`, `mypy`, `pytest --cov-fail-under=80`; no `nbdev-ci` |
| S22 | **M1 gate** | — | `uv run pytest --cov=pubmed_lib --cov-fail-under=80` passes; `python -c "from pubmed_lib import PubMedClient"` works; git tag `v1.0.0-alpha` ready |

---

## Milestone 2 — `1.0.0` (MCP server)

| ID | Action | Target path(s) | Acceptance criterion |
|----|--------|----------------|----------------------|
| S23 | Add MCP optional deps + script entry | `pyproject.toml` | `[project.optional-dependencies] mcp = ["fastmcp>=2.0"]`; `[project.scripts] pubmed-mcp = "pubmed_mcp.server:main"` |
| S24 | MCP auth middleware | `NEW: src/pubmed_mcp/auth.py` | SSE mode raises/ exits if `MCP_API_KEY` missing or `<32` chars; stdio skips auth; unit test passes |
| S25 | MCP tool handlers | `NEW: src/pubmed_mcp/tools.py` | Five functions return JSON strings matching `Article`/`SearchResponse` schema; mock `PubMedClient` in tests |
| S26 | FastMCP server + CLI | `NEW: src/pubmed_mcp/server.py`, `NEW: src/pubmed_mcp/__init__.py` | `pubmed-mcp --help` shows `--transport stdio\|sse`; registers tools `pubmed_search`, `pubmed_fetch`, `pubmed_search_fetch`, `pubmed_get_article`, `pubmed_format_citation` |
| S27 | MCP contract tests | `NEW: tests/mcp/test_tools.py`, `NEW: tests/mcp/test_server.py` | Tool JSON outputs validate against Pydantic models; SSE startup fails without `MCP_API_KEY` |
| S28 | MCP documentation + README | `NEW: docs/mcp.md`, `NEW: docs/contributing.md`, `README.md` | README MCP-first with `mcp.json` example; documents `ENTREZ_EMAIL`, SSE auth, rate caps |
| S29 | Bump version to 1.0.0 | `src/pubmed_lib/__init__.py`, `CHANGELOG.md`, `pyproject.toml` | `__version__ == "1.0.0"` |
| S30 | **M2 gate** | — | `uv sync --extra mcp --dev` succeeds; `uv run pytest` passes; manual: `ENTREZ_EMAIL=... uv run pubmed-mcp` starts stdio; SSE rejects request without API key |

---

## Risks & human gates

| Risk | Mitigation |
|------|------------|
| Breaking all existing `Search`/`Result` imports | Document in `MIGRATION.md`; version bump to 1.0.0 |
| BioPython Entrez mock fragility | Use fixture XML + patch `Bio.Entrez.esearch`/`efetch` at module path `pubmed_lib.client` |
| FastMCP SSE API changes | Pin `fastmcp>=2.0,<3`; contract tests lock tool names |
| Package name `pubmed-lib` vs import `pubmed_lib` | Standard Python normalization; document in README |
| Self-ref dep in old `settings.ini` | Remove `settings.ini` in S20 |
| Live Entrez in CI | Default tests mocked; optional `@pytest.mark.live_entrez` excluded in CI |

**Human gate:** None — all 18 grill decisions locked. If `[llm]` extra is required for 1.0.0 (not 1.0.1), add steps S31–S33 before M2 gate (see deferred work below).

## Deferred work (1.0.1)

Add only if M2 completes before release deadline:

| ID | Action | Target path(s) | Acceptance criterion |
|----|--------|----------------|----------------------|
| S31 | `[llm]` extra deps | `pyproject.toml` | `llm = ["pydantic-ai>=0.0.49"]` |
| S32 | PydanticAI affiliation parser | `NEW: src/pubmed_lib/llm/affiliation.py`, `NEW: src/pubmed_lib/llm/providers.py`, `NEW: docs/llm.md` | `parse_affiliation_llm(..., provider="ollama")` mocked test passes; not imported by core |
| S33 | LLM unit tests | `NEW: tests/unit/test_llm.py` | Provider factory builds without live keys when mocked |

## Verification plan

### M1 (`1.0.0-alpha`)

- [ ] Automated: `uv sync --dev && uv run ruff check src tests && uv run mypy src/pubmed_lib && uv run pytest --cov=pubmed_lib --cov-fail-under=80`
- [ ] Manual: `ENTREZ_EMAIL=... uv run python -c "from pubmed_lib import PubMedClient; print(PubMedClient().search_articles('diabetes', max_results=3).returned)"` returns `<=3`

### M2 (`1.0.0`)

- [ ] Automated: `uv sync --all-extras --dev && uv run pytest`
- [ ] Manual stdio: Cursor `mcp.json` with `uv run pubmed-mcp` calls `pubmed_search` successfully
- [ ] Manual SSE: `MCP_API_KEY=... ENTREZ_EMAIL=... uv run pubmed-mcp --transport sse --port 8000` rejects unauthenticated HTTP request with 401

## Handoff

Pass this manifest to **restricted-coder**. Implement **S1→S22** first; stop at **M1 gate** for review/tag, then **S23→S30**. Do not implement deferred S31–S33 unless explicitly requested.

Obsidian wiki update: manual sync of `docs/*.md` → `~/Documents/Obsidian Vault/AI Research/PubMedLib/` on each milestone tag.
