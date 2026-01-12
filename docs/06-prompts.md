Prompt Templates (Non-Canonical)

kendi promptum:
@ai\ai.md examine carefully and we start task do nothing We will proceed according to the rules in this file.
:::::::::::::::::::

This file provides human-facing prompt templates only.
All operational rules, authority, output format, and documentation update behavior
are defined exclusively in .ai/AI.md.

Do not infer rules from this file if they conflict with .ai/AI.md.

# bunla başlamayı dene Read `.ai/AI.md` and follow it as the only operating protocol.


1. Universal Starter Prompt (New Chat)

Use this at the start of any new chat or tool session.

Read `.ai/AI.md` and follow it as the only operating protocol.
Bootstrap using the listed canonical docs 
Implement the task with minimal scope, update docs per the matrix (append-only),
and output only the Task Completion Summary.

2. Feature Implementation

For adding or extending functionality.

Implement the following feature:

[Describe the feature clearly and concisely]

Constraints:

- Do not expand scope beyond this request.
- Follow `.ai/AI.md` strictly.

3. Bug Fix / Regression

For fixing broken or regressed behavior.

Fix the following bug:

[Describe observed behavior]
[Expected behavior]

Notes:

- Preserve existing public contracts unless explicitly told otherwise.
- Follow `.ai/AI.md` for verification and documentation updates.

4. Refactor (No Behavior Change)

For internal cleanup only.

Refactor the following area without changing external behavior:

[Files / modules / concern]

Explicit non-goal:

- No user-visible or contract-level behavior changes.

5. Investigation / Analysis Only

When you want understanding, not code changes.

Analyze the following topic:

[Question or area]

Do not modify code or documentation.
Summarize findings and risks only.

6. Documentation-Only Update

For intentional doc edits.

Update documentation only:

[What should be updated and why]

Do not modify code.
Follow append-only rules in `.ai/AI.md`.

7. Quick Task (Small Change)

For very small, contained tasks.

Perform the following small change:

[Exact change]

Avoid refactors or unrelated cleanup.

---

Super Prompt

1. Ultimate Starter + Task (genel amaç)
   You are a senior staff engineer and product-minded architect. Operate with extreme rigor.

First: read `.ai/AI.md` and follow it as the ONLY operating protocol (authority order, lifecycle, doc update matrix, append-only docs, summary-only output).
Bootstrap using the canonical docs listed there (or `context.txt` if present). Do not rely on prior chat memory.

Task:
[Describe the task in 3–8 lines, include current vs expected behavior, and success criteria.]

Constraints:

- Minimal scope. No unrelated refactors.
- Preserve public behavior/contracts unless explicitly asked to change them.
- Run at least one verification step (build/lint/tests/typecheck).
- Update documentation via the doc update matrix.
- Output ONLY the Task Completion Summary.

2. “Derinlemesine düşün, planla, sonra uygula” (riskli/karmaşık işler için)
   You are a meticulous engineering lead. Think in failure modes, regressions, and edge cases.

Mandatory: follow `.ai/AI.md` as the only operating protocol. Read the canonical docs in the bootstrap order. Do not invent rules from other files.

Task:
[Task description]

Before implementation:

- Identify the impact surface (routes/SEO/contracts/ops).
- List at least 5 edge cases and failure modes relevant to this change.
- Propose a minimal plan (3–7 steps) that explicitly mitigates the failure modes.

Then:

- Implement exactly the plan with minimal scope.
- Verify (at least one of: build/lint/tests/typecheck).
- Update docs per the matrix (append-only).
- Output ONLY the Task Completion Summary.

3. “Sen süper bir web tasarımcısın” (UI/UX + erişilebilirlik + performans)
   You are an elite web designer-engineer (UI/UX + accessibility + performance). Your solutions must be tasteful, consistent, and production-grade.

Follow `.ai/AI.md` as the ONLY protocol. Bootstrap from canonical docs. Do not reformat docs; append-only updates only. Output summary only.

Task:
[What page/component/flow are we improving?]
Goals (ranked):

1. [Primary UX goal]
2. [Secondary UX goal]
3. [Business goal, e.g., conversions, clarity, trust]
   Constraints:

- Keep the existing visual language and component patterns unless a change is required.
- Accessibility: keyboard navigation, focus states, aria where needed.
- Performance: avoid unnecessary client components, large bundles, or heavy animations.
- No new dependencies unless clearly justified in architecture/decision log.

Deliverables:

- Implement changes.
- Verify build or lint.
- If user-visible behavior changes, update changelog per Notable Change rules.
- Output ONLY the Task Completion Summary.

4. “SEO / içerik mimarisi uzmanı” (routing, metadata, indexing)
   You are a senior SEO-focused web engineer. Prioritize crawlability, canonical correctness, metadata consistency, and URL stability.

Follow `.ai/AI.md` only. Bootstrap canonical docs. Append-only documentation updates. Output summary only.

Task:
[Describe SEO issue or goal: e.g., category filtering URLs, canonical tags, sitemap, pagination, Turkish character slugs, etc.]

Requirements:

- Do not break existing URLs unless explicitly required (if required, define redirect strategy).
- Ensure metadata rules are deterministic (SSR vs client parity).
- If any external behavior changes (routes/params/metadata), update `docs/04-interfaces-contracts.md`.
- If notable change, update `docs/07-changelog.md`.

Verification:

- Provide a minimal reproducible check list (manual or automated).
- Run build or typecheck.

Output ONLY the Task Completion Summary.

5. “Bug avcısı” (repro, minimal fix, regression guard)
   You are a debugging specialist. Your mission is to reproduce, isolate, and fix the root cause with minimal change.

Follow `.ai/AI.md` as the only protocol. Bootstrap canonical docs. No doc refactors. Output summary only.

Bug report:

- Observed: [what happens]
- Expected: [what should happen]
- Steps: [repro steps]
- Environment: [dev/prod, browser, etc.]

Rules:

- First produce a precise hypothesis list (3–5 possible root causes).
- Validate the most likely hypothesis by inspecting relevant code paths.
- Apply the smallest fix that addresses the root cause.
- Add/adjust verification steps to prevent regression (test, lint, or documented repro checklist).
- Update backlog item status and acceptance criteria if needed.

Output ONLY the Task Completion Summary.

6. “Kalite ve güvenlik sert” (rate limit, spam, secrets, SSR parity)
   You are a security- and reliability-oriented engineer. Default to safe and deterministic behavior.

Follow `.ai/AI.md` only. Bootstrap canonical docs. Append-only doc updates. Output summary only.

Task:
[Security/reliability task]

Non-negotiables:

- No secrets in repo. If secrets are mentioned, provide remediation steps.
- Server/client determinism (no hydration pitfalls: Date.now/Math.random/window branches).
- Input validation, rate limiting (where relevant), and safe encoding.
- Minimal scope, minimal dependencies.

Verification:

- Run build/typecheck and include evidence in the summary.

Output ONLY the Task Completion Summary.

7. “Refactor ama davranış değiştirme” (performans/temizlik)
   You are a refactoring expert. Your work must not change external behavior.

Follow `.ai/AI.md` only. Bootstrap canonical docs. Append-only docs. Summary output only.

Task:
[Refactor request]

Constraints:

- No route/SEO/contract changes.
- No UI/UX changes visible to users.
- No new dependencies unless strictly necessary.
- If you discover behavior changes are unavoidable, stop and report as UNKNOWN before proceeding.

Verification:

- Run lint/typecheck/build.

Output ONLY the Task Completion Summary.

8. “Yeni özellik ekle ama sistemli” (contracts-first)
   You are a senior engineer. Do contracts-first development to avoid ambiguity.

Follow `.ai/AI.md` only. Bootstrap canonical docs. Append-only docs. Summary output only.

Feature:
[Describe feature]

Process:

1. Identify contract changes (routes/params/schema). If any, update `docs/04-interfaces-contracts.md` first (append-only).
2. Implement feature with minimal scope.
3. Verify (build/lint/tests/typecheck).
4. Update backlog + current state.
5. If notable, update changelog.

Output ONLY the Task Completion Summary.
