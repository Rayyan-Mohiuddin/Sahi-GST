# Sahi GST continuation and efficient collaboration

Updated 10 October 2026. Deadline: **Sunday 11 October, 09:00 IST**; submission target **07:00 IST**.

## Current source/deployment

- Original repo: https://github.com/Salman-a-gamer/Sahi-GST
- Friend's repo and current deployed source: https://github.com/Rayyan-Mohiuddin/Sahi-GST
- Live demo: https://sahi-gst-d511.vercel.app/
- Imported friend's latest checked commit: `3c349a8`; four deployment fixes atop our baseline.
- This checkout preserves those fixes and adds docs plus field-confirmation/result-clarity corrections. Exact final commit: use `git log -1 --oneline` after this work is committed.
- User confirmed the intended workflow: one shared project, separate feature branches, pull-request review/merge, then teammate continues. Use the friend's deployed repo as shared integration target; the current authenticated Salman account has read-only access there. Rayyan must add Salman-a-gamer as collaborator for direct feature-branch pushes/PRs. Local origin still points to Salman's repo; teammate points to Rayyan's. No force-push or remote replacement is needed.

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

Latest access check: the attempted `git push teammate feature/invoice-extraction` returned 403, and GitHub still reports `push: false` for the authenticated Salman account. Verify Rayyan invited **Salman-a-gamer**, then accept the invitation. Invitation sent is not the same as accepted write access. Do not repeatedly retry pushes until access changes.

Branches to merge in order:

1. `feature/invoice-extraction` — parser/layout changes plus previous docs/confirmation fix.
2. `feature/ocr-review-recovery` — extraction feedback and bounded/cancellable OCR; depends on the first branch.

Both are saved in Salman's repository while teammate access is blocked. Once access works, push them to teammate. On Rayyan's GitHub repo, choose **Pull requests → New pull request**, base **main**, compare **feature/invoice-extraction**. Review Files changed, add a concise description/test results, and create the PR. Rayyan reviews/merges it, verifies deployment, then repeat for the recovery branch. If the first PR is squash-merged, rebase/cherry-pick the second feature carefully so its PR does not repeat the first patch; ask Codex to handle that rather than force-pushing shared main.

After Rayyan grants collaborator access, push this branch to `teammate` and open a PR targeting Rayyan's `main`. The branch includes the earlier docs/confirmation commit missing from his main. Review that complete diff. Once merged, both teammates pull shared main before starting the next branch.

Until then, the branch is pushed to Salman's repo. Rayyan can fetch the exact branch using a `salman` remote, run `git merge --ff-only salman/feature/invoice-extraction` from a clean up-to-date main, and push to his origin. If he has newer work and fast-forward fails, review a normal merge. This is a Git merge handoff, not a GitHub pull request across unrelated repositories. Do not present it as already merged/deployed.

## Work to do while Codex allowance recovers

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
