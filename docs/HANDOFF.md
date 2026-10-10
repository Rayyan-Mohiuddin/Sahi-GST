# Sahi GST continuation and efficient collaboration

## Home-page polish — 11 October 2026

Branch `codex/focused-fintech-home`, based on pushed OCR checkpoint `f65262d`. Frontend-only implementation: focused landing, separate workspace with an explicitly synthetic demo-data toggle, severity-ordered findings with collapsed details, navy/ivory palette and locally bundled Inter/Noto fonts. No changes to extraction, rules, API, database schema or deployment configuration. Local checks: 47 Django SQLite tests, 14 frontend tests, TypeScript and production export pass. Desktop and 360px screenshots captured in `docs/ui-evidence/`; preview QA and Lighthouse pending. Keep this branch unmerged until preview flows are checked. At 360px the requested long headline at 40px makes the stacked invoice extend below an 800px viewport; it remains readable without horizontal overflow. Humans can test physical camera capture and review the exact copy while preview checks run.

Updated 10 October 2026. Deadline: **Sunday 11 October, 09:00 IST**; submission target **07:00 IST**.

## Current AI failure investigation — codex/ai-provider-diagnostics

Released: fix commit `66e1ca0`, merged by [PR #8](https://github.com/Rayyan-Mohiuddin/Sahi-GST/pull/8) as shared main `ca103b71042c1699acd2f3a478b0cced3d6d83b2`. User explicitly authorized deployment. Both existing Vercel preview and production integrations succeeded. Target production deployment: `https://vercel.com/rayyan-mohiuddins-projects/sahi-gst-d511/9utWjTF1U9zpFxssJSQmdCnybcND`, GitHub deployment ID `6980166177`, environment Production – sahi-gst-d511. After completion, `https://sahi-gst-d511.vercel.app/` returned 200 with Sahi GST branding and `/api/health/` returned 200 with `status: ok`. Live Gemini inference is still unverified. The older local main remains at `3c349a8`; current local feature branch holds the fix and release notes.

User supplied the production `/api/extract/` failure from 10 October 16:46:40 IST: app HTTP 502, function duration 1.37 seconds, request `76ptg-1791631000121-d9445ca938a1`, deployment `dpl_9Chj6Mpw18QnngGDLbSkqcHEzUn5`. Exact UI message maps to an unhandled upstream HTTP status. The app previously discarded that status/body and logged no provider diagnostic; Vercel's “No outgoing requests” summary does not resolve the cause. No provider outage, key problem or model problem has been proven. User reports “3.8 flash”; the exact environment string must be `gemini-3.8-flash`.

Patch: extraction errors log safe model/category/upstream HTTP/allowlisted Google status with a reference ID also returned to the user. Provider messages, credentials and invoice data are excluded. Retry the same model once after jittered delay only for HTTP 500/502/503/504, reducing the next socket timeout against a 45-second request budget (35 seconds maximum per attempt). No retry for key/access/model/quota errors, no provider/model switching. Existing explanation calls share the transport retry, but retain their existing rule-wording fallback response.

Model compatibility update: official [3.8 generateContent migration guide](https://ai.google.dev/gemini-api/docs/generate-content/latest-model) says to remove deprecated sampling parameters and use thinking levels. Removed the global temperature override; 3.8 now uses `thinkingLevel: low` (not unsupported `minimal`), while explicitly selected 2.5 Flash retains its supported budget/temperature. Default/example restored to the user's 3.8 model. Official pricing lists a free tier, but the actual account's quota/access is not verified. This corrects a documented compatibility gap, not a proven cause of the reported generic provider error.

Checks: all **44 Django tests pass in local SQLite mode** using Python 3.14, including 11 new transport/diagnostic/model-request tests; `git diff --check` passes. Both Vercel previews and production builds succeeded; live homepage/database health pass. Mock provider calls only; no live inference or full PostgreSQL test rerun claimed. Frontend and schema unchanged.

Next: refresh production, sign in and scan a synthetic invoice with consent. If it fails, share the visible reference/provider status or the matching `gemini_failure` log line; never share the key. The user reports Gemini 3.8 Flash; the dashboard's exact environment string has not been read or changed by this release. It should be `gemini-3.8-flash`.

## Current source/deployment

- Original repo: https://github.com/Salman-a-gamer/Sahi-GST
- Friend's repo and current deployed source: https://github.com/Rayyan-Mohiuddin/Sahi-GST
- Live demo: https://sahi-gst-d511.vercel.app/
- Imported friend's latest checked commit: `3c349a8`; four deployment fixes atop our baseline.
- This checkout preserves those fixes and adds docs plus field-confirmation/result-clarity corrections. Exact final commit: use `git log -1 --oneline` after this work is committed.
- User confirmed the workflow: one shared project, separate feature branches, pull-request review/merge, then teammate continues. Rayyan's deployed repo is the shared integration target; Salman accepted collaborator access and shared branch pushes now work. Local origin points to Salman's repo; teammate points to Rayyan's. No force-push or remote replacement is needed.

## Continue from your friend's Codex

The practical handoff is source code plus committed context. Ask him to commit/push all intended work and update this file with test results, blockers and relevant environment-variable **names**, never values. Then open the updated project folder in your own Codex and start a chat that reads AGENTS.md, this file and BACKEND_API.md. A Git clone brings code/docs; it does not bring his private chat history or hosting secrets.

To start a clean clone of the deployed source:

```powershell
git clone https://github.com/Rayyan-Mohiuddin/Sahi-GST.git Sahi-GST-team
cd Sahi-GST-team
git switch -c feature/invoice-review
```

If already using a clone of that repo, first run `git status` and save your work, then `git pull --ff-only`. Do not reset/force-push to synchronize divergent work.

To bring this session's updates into the friend's existing clone, **the friend** can run:

```powershell
git status
git remote add salman https://github.com/Salman-a-gamer/Sahi-GST.git
git fetch salman main
git merge --ff-only salman/main
git push origin main
```

If `salman` already exists, skip the add command. If fast-forward fails because he added more commits, stop and review/merge both histories normally. Do not discard his newer commits. This chat has not pushed to the friend's repository or changed its deployment.

## Human-versus-Codex division (user preference)

**Human:** hosting dashboards, Vercel/Neon settings, account/terms/key entry, deployment button, Google Drive sharing/uploads and recording the demo. Codex provides short exact instructions and fixes errors from concise logs.

**Codex:** code, focused debugging, tests, source comparisons, docs and lean packaging. No prolonged dashboard clicking unless explicitly requested. Fetch/read only relevant changes; batch independent checks; avoid repeated full source dumps or unnecessary model/provider research.

Before stopping or approaching a usage limit: save changes, update this handoff, provide actual test results, blockers, the next bounded coding task and a work list the humans can do without Codex. Usage allowance varies; do not promise uninterrupted work or a guessed reset time.

## Completed / verified

- Responsive workspace, invoice history, local neural OCR, editable extracted fields, deterministic checks, correction drafts, JSON reports and Allauth/session plumbing.
- Friend deployed the app; live API and PostgreSQL verified.
- Live synthetic audit covered CSRF, parsing, review save, ₹1,000 discrepancy, draft and guest isolation; disposable record removed.
- Current patch invalidates confirmation after a field edit and makes it explicit that results apply to confirmed fields, not a repaired supplier original.
- After integration: backend 10-test suite passes in local SQLite smoke-test mode, root Vercel WSGI imports, frontend TypeScript passes. Earlier full PostgreSQL suite and current live PostgreSQL audit passed separately. Do not describe the latest local rerun as a PostgreSQL test.
- Production Next.js export passes after the confirmation/result-clarity patch. The patch is build-verified locally; it is not yet present on the friend's live deployment until merged/redeployed.

## What is not yet established

- Broad real-invoice parsing accuracy; current parser relies mainly on labelled lines.
- Live cloud LLM extraction (currently disabled), PDF, GSTR-2B reconciliation or active GSTIN lookup.
- Physical Android/iPhone coverage, final two-minute recording, slides and official submission.
- Verified source-to-deployment update for this session's new patch: friend must merge/redeploy it.

## Next bounded coding task

First parser improvement completed on `feature/invoice-extraction`: five synthetic OCR-text fixtures cover labels without separators, next-line values, explicit party sections, dates, rate-versus-amount and conflicting totals. Fourteen backend tests pass in SQLite smoke-test mode. This tests parsing after OCR, not real image recognition. Frontend/model/database schema did not change in this step.

Next: test 3–5 redacted/synthetic **images** with local OCR and record misreads/layout gaps. Add only reproduced failures to fixtures. In particular, ambiguous numeric dates stay null; GSTIN OCR substitutions are not silently corrected; multiple conflicting rates/totals stay unknown. Use the API guide and manual test list below.

### Delivering this feature to the shared repo

Access resolved: user accepted the collaborator invitation. Both extraction and OCR-recovery branches successfully pushed to Rayyan's repo on 10 October. The earlier 403 is historical. Shared main has not been automatically merged or redeployed by this chat.

Branches to merge in order:

1. `feature/invoice-extraction` — parser/layout changes plus previous docs/confirmation fix.
2. `feature/ocr-review-recovery` — extraction feedback and bounded/cancellable OCR; depends on the first branch.
3. `feature/ocr-image-evaluation` — three image fixtures, real OCR evaluation scripts and recorded evidence; depends on the first two branches.

On Rayyan's GitHub repo, choose **Pull requests → New pull request**, base **main**, compare **feature/invoice-extraction**. Review Files changed, add a concise description/test results, and create the PR. Rayyan reviews/merges it, verifies deployment, then repeat for the recovery and evaluation branches. For these stacked branches, a normal merge commit preserves ancestry. If an earlier PR is squash-merged, rebase/cherry-pick later features carefully so they do not repeat prior patches; ask Codex to handle that rather than force-pushing shared main.

The extraction branch includes the earlier docs/confirmation commit missing from shared main. Review that complete diff. Once merged, both teammates fetch shared main before starting the next branch. Current branch pushing does not mean the features are already merged or deployed.

## Work to do while Codex allowance recovers

New feature/multipage-ai-review builds on **pending** fix/invoice-review-completion (db26a78). Merge that PR first, then this branch; normal merge commits preserve ancestry. Adds real browser camera preview, up to 5 ordered pages/one review (3 MB total for Vercel payload safety), private additional-page storage/migration 0003, scrolling sidebar without duplicated profile, Market view with cited PIB context, schema-constrained Gemini extraction, English/Hindi/Telugu rule/AI explanations, local-voice read-aloud, GST-amount-under-review and WhatsApp share. AI key setup is owned by the user and live-provider verification is pending. Tests use mocked Gemini responses; never call them real AI accuracy evidence.

Verification for this branch: **28 backend tests in SQLite smoke-test mode, 11 frontend tests, TypeScript and production export pass**. No PostgreSQL rerun/hardware camera/live Gemini/native-speaker validation is claimed. Existing single-image `file`/`image_data` routes remain accepted; AI wording does not modify verdicts or amounts. QR/tamper evidence, supplier scoring and photo-quality classification remain deferred.

Human next steps: configure an available **unpaid** Gemini key/model, merge/redeploy both PRs, sign in, scan synthetic/redacted pages with consent, test camera allow/deny/close, page removal/viewing/reopening, sidebar at 100% zoom, voice availability and WhatsApp recipient choice. Obtain an approved interview quote before updating Market content. No public QR/tamper evidence, supplier score or photo-quality classifier has been shipped.

Review-completion fixes start from shared main 4820aaa. New branch screens OCR content before image saving, adds protected source-image retention (migration 0002), readable PDF reports with ReportLab, Finish and functional workspace actions. Older discarded images cannot be recovered. Local content screening is heuristic; manual entry without a rejected image remains available. Twenty backend tests pass in SQLite smoke-test mode; eight frontend tests, TypeScript and production build pass; PDF sample rendered/visually reviewed. A separate PostgreSQL rerun could not connect to the local server and was stopped; do not claim this new schema has been PostgreSQL-tested here. Merge/redeploy to apply the migration and dependency, then verify source-image/PDF flow against the live database. Physical-device menu/download verification remains pending.

Mobile review branch starts from shared main `a011d17`, which includes all three merged PRs. It splits file selection/camera capture, records navigation/review history so Back closes a review, cancels local OCR when review closes, and extracts upload/dialog/GSTIN/privacy/guide components. GSTIN values require explicit individual confirmation; missing values can still produce review findings. Eight frontend lifecycle/navigation tests, TypeScript and production export pass. Physical phone chooser/Back testing remains a human task after deployment. Read PRODUCT_VISION.md and OCR_ENGINE_NOTES.md before changing OCR engines.

Real image evaluation completed on feature/ocr-image-evaluation: 3 generated synthetic PNGs, 19/20 present fields correct, 2/2 expected unknowns preserved; the one misread GSTIN is flagged for review. Measured first scan 17,665 ms with loading, later scans 1,346/1,329 ms on this machine. This is not customer-invoice accuracy. Reproduction scripts, inputs and limitations are in OCR_EVALUATION.md. Next: manual phone/laptop runs and redacted unseen layouts, then final video/slides and submission checks.

Recovery stage implemented: `/api/parse/` now returns per-field hints, evidence excerpts, extracted count and total field count. The UI highlights missing/ambiguous fields without inventing model confidence. Local OCR can be cancelled and stops after 90 seconds; late results cannot overwrite fields. Sixteen backend tests, four OCR lifecycle tests, TypeScript and production build pass. No physical-device/UI browser verification or cloud deployment of this stage is claimed.

Manual checks after merging/deploying: scan a clear image and inspect field hints; cancel during OCR model loading; retry; use an ambiguous date and conflicting total; verify the image remains unchanged and only entered fields are checked. Simulated worker tests cover timeout/cancellation; do not deliberately leave the public service busy or claim an unseen-image accuracy result.

1. On the **live URL**, run a sample: ₹12,800 displayed total versus ₹11,800 arithmetic. Check finding, supplier draft and JSON export.
2. Upload 3–5 clear synthetic/redacted invoices with different layouts. Record exactly which fields OCR/parser got wrong; save minimal reproductions, not confidential documents in Git.
3. Try missing GSTIN, blank tax amount, clean total and unsupported document types. Confirm missing is not silently zero and no full-compliance promise appears.
4. After the new patch deploys: confirm fields, edit the total, and verify the checkbox resets/check button disables until reconfirmed.
5. Test on an actual phone and laptop: upload picker, scrolling, readable results, copy request and report download. Test signed-out access and account signup/login yourself.
6. Record a two-minute demo from the final build; prepare six slides from PITCH_AND_SUBMISSION.md. Use original screenshots; browse templates for layout inspiration only.
7. Log each person's actual contributions and evidence. Regenerate the latest ZIP, test extraction/setup, upload to Drive and verify signed-out sharing.
8. Stop adding features Saturday evening. Submit before Sunday 07:00 IST and save portal confirmation.

## Resume prompt (C-R-I-S-P-E)

**Context:** Continue Sahi GST from the current repository and live demo, due Sunday 11 October 09:00 IST. Read AGENTS.md, HANDOFF.md and BACKEND_API.md. **Role:** focused full-stack engineer and reviewer. **Instruction:** inspect the latest diff and complete the next documented coding task, preserving the working deployment. **Specification:** concise updates; humans handle dashboards; no paid services. **Performance:** test the changed behaviour and report exact evidence, blockers and commit. **Example:** an unextractable GSTIN stays unknown for user review; editing a confirmed total requires reconfirmation, and passing checks do not imply the original invoice was repaired.

## Latest release work — codex/auth-release-checks
Shared main 2aaa256 includes all prior feature work. Auth styling fixed at the current Allauth layout; two auth tests pass. Live session reports cloud_extraction=true and PostgreSQL on 10 October; this confirms configuration gates only, not provider success. User has no approved interview quote. Friend test set and physical two-phone checks remain pending. Commit: use git log -1 after this checkpoint.

## Release checkpoint (latest)
Branch codex/auth-release-checks: auth fix 8aa68bc, AI timeout recovery bd7d8a3; subsequent UI polish and acceptance checklist are on this branch. 32 SQLite backend tests, 11 frontend tests and production build pass. User confirms Gemini variables/redeployment; live configuration true, actual inference still unverified. Browser preview denied by security policy; no physical phone/voice verification claimed. Next: merge branch, run docs/RELEASE_ACCEPTANCE.md on two phones, provide friend cases and actual Gemini result. UI changes are build-verified, visual inspection pending. Humans: record demo/slides/contributions and submission evidence while Codex unavailable.


## Jury/demo polish — latest branch codex/demo-flow-fixes
Base shared main cb95240. AI prerequisite fix checkpoint 10a68c4: reported no-entry cursor was disabled consent/auth gating, not a reproduced provider failure. Button now gives actionable explanations; consent remains explicit. Replaced unverified default model with documented gemini-2.5-flash; explicit Vercel model still overrides it. Model access/quota must be confirmed on the unpaid account. Provider errors now distinguish key/access/model/quota without revealing payloads.

Password show/hide added. One Confirm and check action attests fields, GSTIN characters and supported scope; editing still removes the selected result. Uncertain fields remain visible, other extracted fields expand; unflagged is not claimed confidence. Phone fields are one column with a sticky confirmation action. Findings emphasize GST amount under review (not ITC at risk/loss), saffron count-up respects reduced motion. Indian number formatting, Inter/Noto script fonts with system fallbacks, status badges and neutral main surfaces added. PDF has a reference Check ID stamp and abstract ledger lines; no tamper-evidence claim.

Checks: 33 backend tests (SQLite), 11 frontend tests, production build/TypeScript passed. Two-page PDF rendered and visually checked. Physical phone/voice/live Gemini remains pending; user asked to try signed-in consent flow and report result. Browser UI review remains unavailable after earlier denied preview access. Google fonts need network; do not claim identical typography on every offline phone. Friend test cases still not supplied. Merge this branch and redeploy, then run RELEASE_ACCEPTANCE.md. No new product features planned.

## Camera OCR pipeline checkpoint — 10 October

Commit `41cf9e5` adds text-first PDF processing (`/api/parse-document/`) and a camera/scanned-image path that preserves originals, creates a temporary crop/grayscale/contrast OCR copy, scores blur/brightness/glare/page coverage, carries line confidence to parsing and returns raw text plus normalized/corrected fields. GSTIN corrections are position-aware and checksum-gated; ambiguous values stay uncorrected and need review. Server settings: `OCR_FIELD_CONFIDENCE`, `OCR_QUALITY_SCORE`, `OCR_ARITHMETIC_TOLERANCE`, `OCR_SAFE_CORRECTIONS`. Checks: 47 Django SQLite tests, 14 frontend tests, TypeScript and production export passed locally. No real camera hardware/customer-invoice benchmark or deployed verification claimed. Next human task: scan 3–5 consented/redacted poor-light, glare and skew examples on a phone; record score/warnings/corrections and adjust thresholds only from evidence.
