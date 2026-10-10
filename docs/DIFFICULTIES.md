# Difficulties, decisions and outcomes

Record actual events. Status values: resolved in planning, verified fixed, open, or anticipated risk. A design mitigation is not a verified code fix.

| Date IST | Difficulty encountered | Action and reason | Evidence / outcome | Status |
|---|---|---|---|---|
| 2026-10-09 | Problem statement spans consumers, sellers and buyers | Recommended registered small-business buyer and ordinary domestic goods invoices | STRATEGY.md; segment still awaits user interviews | Resolved in planning |
| 2026-10-09 | Attached proposal assumes unserved sub-threshold market and unique AI/follow-up | Checked incumbent primary pages; removed blanket novelty claims | Clear and Zoho sources in RESEARCH.md | Resolved in planning |
| 2026-10-09 | Proposal used FastAPI contrary to team stack | Locked Django with Next.js, PostgreSQL and Allauth | MVP_SPEC.md | Resolved in planning |
| 2026-10-09 | One-tap “fix” could misrepresent supplier document correction | Separated transcription edits, correction requests and revised-document checks | MVP_SPEC.md workflow and statuses | Resolved in planning |
| 2026-10-09 | Some government pages failed direct retrieval | Retained indexed official evidence, recorded access limits and deferred unverified applicability assertions | RESEARCH.md; no full current-law verification claimed | Open |
| 2026-10-09 | Deadline and effort initially unknown | Asked early; initial deadline was Sunday evening, later corrected by the user | Superseded by Sunday 11 October 09:00 IST; conservative combined-hour budget | Resolved in planning; effort interpretation open |
| 2026-10-09 | First reminder request lacked thread destination | Retried with current-thread destination | Tool confirmed active daily automation: log-hackathon-team-contributions | Verified fixed |

## Anticipated risks — not incidents yet

### Implementation incidents on 10 October

- **Corrected deadline and brand:** user changed deadline to Sunday 09:00 IST and product name to Sahi GST. Updated all planning documents and replaced the calendar gates. Internal submission is 07:00 IST.
- **GitHub CLI absent:** existing Git Credential Manager account was available with required access. Created private Salman-a-gamer/Sahi-GST through GitHub API without printing credentials.
- **Network/file sandbox restrictions:** dependency installation and production export initially failed. Reran narrowly scoped installs/builds with reviewed access; both completed.
- **OCR identifier errors:** real Tesseract.js scan misread two GSTINs; human confirmation corrected them. A total discrepancy then generated the expected supplier request. Improved label handling for goods description and stated round-off. No claim of perfect extraction.
- **PostgreSQL encoding:** Windows default WIN1252 could not store the rupee sign in JSON. Initialized a separate UTF-8 local cluster; the complete 10-test suite then passed on PostgreSQL. The original local cluster was not destructively deleted.
- **Hosting:** user has Vercel, not Render/Neon accounts. Verified official Django support and prepared a single-project deployment; sign-in completed, free PostgreSQL provisioning still to complete.
- **Reminder state:** found the previously created reminder paused. Updated name/deadline while preserving that paused state.

| Risk | Planned response | Owner |
|---|---|---|
| Vision extraction mistakes | Critical-field confirmation, nulls and held-out tests | B + A testing |
| API/network failure | Timeout, retry and explicitly manual fallback | B |
| Over-scoping | Gate stretch features behind live core loop | Both |
| Tax false positives | Scoped rules, explicit prerequisites, abstention | B + knowledgeable reviewer |
| Frontend/backend drift | Freeze shared schema and integrate early | Both |
| Deployment trouble | Hosted skeleton early; reserve and simple topology | B |
| Unclear customer value | Interview owners/bookkeeper and observe task | A |
| Missed submission | 07:00 internal deadline, signed-out link checks | A |

### Team continuation on 10 October

- **Dashboard automation used too much allowance:** user explicitly requested a different workflow. Recorded in AGENTS.md and HANDOFF.md: human handles setup/deployment/uploads; Codex handles focused code/debugging and provides exact short steps.
- **Earlier browser action blocked by usage review:** continuing Neon setup was not executed because automatic approval review could not run after a usage limit. It was not an unsafe-action determination. That earlier setup is superseded by the friend's working deployment; no bypass attempted.
- **Separate repositories could drift:** fetched friend's four commits and fast-forwarded this clean checkout to `3c349a8`; added teammate remote. Both histories preserved. New changes go to Salman's repo; friend receives exact merge steps for the live source.
- **Stale project status:** live API health/session checks returned 200 and PostgreSQL. Synthetic review/parsing/draft/isolation audit passed; test record removed. Replaced “no public URL” status with verified evidence and remaining limits.
- **Field confirmation remained checked after edits:** patched frontend to clear confirmation on every field edit and explain that findings apply to entered values. TypeScript check passes; manual deployed verification remains on the handoff checklist.
- **Friend's deployment configuration:** observed four commits fixing root requirements, metadata, WSGI discovery and bundled backend files. Root WSGI loads and backend's 10-test suite passes after integration. The rerun used local SQLite smoke-test mode; previous PostgreSQL suite and current live PostgreSQL API evidence are recorded separately.

## Append template

### Invoice extraction branch on 10 October

- **Collaboration assumptions:** fetched teammate/main and verified local code contains all friend's current commits plus our one documentation/confirmation commit. Started feature/invoice-extraction. GitHub reports Salman has read-only access to Rayyan's repo; documented collaborator/PR setup and the temporary Git merge handoff.
- **Parser missed common layouts:** reproduced unsupported whitespace labels, next-line values and tax-rate-plus-amount lines with five synthetic text fixtures. Added conservative label/date/currency/section handling. Unknown/conflicting values remain null.
- **Overlapping labels:** regression detected Supplier GSTIN being misread as supplier name. Excluded GSTIN from party-name labels and preferred the most complete label, avoiding Total taxable value being read as invoice total.
- **Verification:** 14 backend tests pass in local SQLite smoke-test mode. This change is parsing code only; no frontend build or cloud deployment was needed. Real image tests remain a human task, not a completed accuracy benchmark.

- Date/time IST:
- Owner:
- Observed problem and reproduction:
- Impact on user/demo/deadline:
- Attempts and evidence:
- Chosen fix and reason:
- Verification performed and outcome:
- Remaining limitation:
- Related commit/artifact:

Never write “fixed” without verification. Record failed attempts when they explain the final decision, without including secrets or customer data.
