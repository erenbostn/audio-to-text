# 0) Prime Directive

This repo is **documentation-driven**.

- `docs/` is canonical
- No silent drift between code and docs
- Implement only requested scope + minimum consistency fixes
- Documentation edits are **append-only** unless explicitly requested
- Never reformat or reorganize documentation

---

# 1) Authority Order (Conflict Resolution)

If sources conflict, resolve in this order (highest wins):

1. `docs/01-requirements.md`
2. `docs/04-interfaces-contracts.md`
3. `docs/03-architecture.md` + `docs/adr/*`
4. Code
5. `docs/05-backlog.md`
6. `docs/06-prompts.md` (non-canonical)
7. `docs/07-changelog.md` (history only)

## Rule

- If code conflicts with docs → **update code**
- If requirements/contracts change → **update docs first, then code**

---

# 2) Session Bootstrap (Always the Same)

At the start of every task:

1. Read `.ai/AI.md`
2. Read, in order:
   - `docs/00-project-brief.md`
   - `docs/01-requirements.md`
   - `docs/04-interfaces-contracts.md`
   - `docs/03-architecture.md`
   - `docs/05-backlog.md`
   - `docs/07-changelog.md`

**Important:**
- Do not rely on prior conversation memory
- The repo is the only truth

---

# 3) Task Lifecycle (Mandatory)

Follow this exact sequence:

## A. Scope

- Restate task in 1 paragraph
- List explicit non-goals

## B. Impact Surface

- User-facing behavior (pages, routes, SEO)
- Interfaces/contracts
- Architecture boundaries
- Ops (env, build, deploy)

## C. Plan

- 3–7 concrete steps

## D. Implement

- Minimal, plan-only changes

## E. Verify

- Run at least one: build / lint / tests / typecheck

## F. Update Docs

- According to **Doc Update Matrix** (Section 4)

## G. Output

- Summary only (Section 5)
- No full files, no large diffs

---

# 4) Documentation Update Matrix

## Always (every task)

### `docs/05-backlog.md`

- Mark item **Done** / **In Progress** or add missing item

### `docs/00-project-brief.md`

- Append under `## CURRENT STATE` (AI-maintained):
  - What changed (1–3 bullets)
  - Affected area (routes/modules)
  - Operational note if any

## Conditional

### `docs/04-interfaces-contracts.md`

Update if any external behavior changes:

- Routes, URLs, params, filters
- Request/response shapes
- SEO metadata behavior

### `docs/07-changelog.md`

Update if **Notable Change**:

- User-visible behavior
- URL / SEO changes
- Security or rate-limiting
- Performance with user impact
- Build/deploy/env changes

*(Refactor-only changes are NOT notable.)*

### `docs/03-architecture.md` or `docs/adr/*`

- Update only for real architectural decisions
- Prefer a short entry under `## DECISION LOG` (AI-maintained)

---

# 5) Output Format (Only This)

Return only the following:

## Task Completion Summary

- **Scope:** what changed + non-goals
- **Files touched:** list + 1 line each
- **Docs updated:** which docs + what entry was added
- **Verification:** commands run + PASS/FAIL
- **Behavioral impact:** what users notice (routes/SEO)
- **Risks / regressions:** max 5 bullets
- **UNKNOWN / assumptions:** only if unavoidable

---

# 6) Unknowns Policy

- **Do not guess**
- If unclear, ask before implementing

If forced to proceed:

1. Mark as **UNKNOWN**
2. Append under `docs/00-project-brief.md` → `## KNOWN ISSUES / UNKNOWNS` (AI-maintained)
3. Include in final summary

---

# 7) Starter Prompt (Single Prompt for New Chats)

Read `.ai/AI.md` and follow it as the only operating protocol. Bootstrap using the listed docs (or `context.txt` if present). Implement with minimal scope, update docs via the matrix (append-only), and output only the Task Completion Summary.
