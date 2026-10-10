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

### Camera, pages and AI relevance

- **Laptop capture opened a file picker:** capture attribute only hints to mobile pickers. Replaced it with live getUserMedia video preview, explicit capture, permission errors and stopped tracks on close/unmount. Hardware/browser permission verification remains manual.
- **Multiple pages:** added ordered page inputs, sequential local OCR or one multi-image Gemini request, preserved additional private pages and retained legacy first-image routes. Migration 0003 is required.
- **Hosting payload cap:** Vercel documents a 4.5 MB function request/response limit. Capped raw invoice pages at 3 MB combined to leave base64/JSON overhead; did not introduce new paid storage. Source: https://vercel.com/docs/functions/limitations.
- **Repeated/hidden sidebar controls:** removed duplicate profile, relabelled account menu, made navigation scroll inside viewport and hid decorative note on short screens.
- **AI gap:** built actual structured extraction and finding-ID-grounded explanation adapters, with local backup/templates explicitly labelled. Mock tests pass; owner's live free key and a live run are still required.
- **Unsupported financial promise:** changed requested risk meter to known GST amount under review. Invoice-only checks cannot calculate blocked ITC or guaranteed savings.
- **Market proof:** added cited 1.65 crore ecosystem statistic and marked payer/interview claims unvalidated. No fabricated quotes.

### Review completion fixes

- **Non-invoice uploads:** file type/size checks alone did not distinguish content. Added invoice-like OCR-text screening and local-OCR save gate; rejected/unreadable images offer retry/manual entry without that image. Not an authenticity classifier.
- **JSON reports:** added owner-protected PDF downloads, ReportLab dependency and wrapped report sections; JSON stays optional. Rendered a synthetic sample to inspect both pages and corrected a split checklist heading.
- **No Finish:** added a Finish action after the supplier draft, closing the saved review without claiming issues are resolved.
- **Missing recent image:** earlier design deliberately discarded sources. Added optional private original bytes/mime to PostgreSQL with migration, owned retrieval, no-store headers and deletion/expiry. Old discarded images cannot be reconstructed.
- **Inactive workspace control:** replaced decorative dropdown with inbox/privacy/account actions. Does not pretend to provide multi-organization switching.
- **Checks:** 20 backend tests verify screening, image validation/opt-out, ownership, PDF access and deletion; 8 existing frontend tests and typecheck pass. Device/browser flow validation remains to do after merge.
- **Local PostgreSQL unavailable:** separate rerun hung on connection establishment; a five-second connection probe confirmed timeout. Stopped the run. SQLite tests, migration generation, production build and PDF visual QA pass; live PostgreSQL verification is required after deployment.

### Mobile capture, navigation and GSTIN trust

- **Camera opened from generic upload:** original single file input had capture=environment. Replaced it with separate file input without capture and camera input with capture, exposed as two clear actions. OS/browser picker details still vary; physical-device test pending.
- **Back left the website from a review:** review state lacked a history entry. Added workspace navigation controller/hook with dialog entries, popstate handling and balanced close; four history tests pass. Closing the review aborts local scanning.
- **Monolithic UI:** extracted upload, review dialog, GSTIN review, privacy and guide components, plus shared types and navigation hook. Other workspace views remain in the host rather than requiring a risky full routing rewrite.
- **Exact GSTIN uncertainty:** even a pattern-valid identifier can be OCR-misread. Added prominent character review and per-identifier acknowledgement; never silently replaces characters. This improves verification, not raw recognition accuracy.
- **Alternative engine research:** user remembers a PP-OCR-like name. Official PaddleOCR sources confirm an unwarping Python pipeline and browser SDK. Actual GSTIN/phone benchmarking is still pending; engine not replaced on speculation.

### Real-image OCR evaluation

- **Collaborator access resolved:** after invitation acceptance, both tested branches pushed successfully to Rayyan's repository. PR review/merge remains a human task; shared main was not changed.
- **Text tests could not measure OCR:** rendered three synthetic invoice layouts as PNGs and ran the actual free OCR engine, followed by the parser. Got 19/20 present fields correct and 2/2 expected unknowns preserved.
- **Observed identifier misread:** OCR read buyer GSTIN's Z as 2. Preserved observed text and confirmed the structural hint marks it for human review; no checksum/authenticity or silent auto-correction claim.
- **Cold-load latency:** initial model/worker loading took about 18 seconds, versus about 1.3 seconds on later scans. Recorded raw timings and a repeatable local evaluation; no universal speed promise.

### OCR feedback/recovery stage

- **Shared push denied:** collaborator invitation was reported by the user, but git push to Rayyan's repo returned 403 and GitHub still reports read-only access. Work remains on saved feature branches in Salman's repo. Invitation acceptance/account check is the human's next step.
- **Invisible extraction gaps:** added parser hints distinguishing absent, uncertain, conflicting and structurally suspicious fields, with actual OCR-line evidence. UI presents field coverage instead of false confidence percentages.
- **Potential stuck scans and stale results:** added a 90-second limit and cancellation. Late-created workers are terminated; late recognition results cannot overwrite fields. Controls prevent field/file edits during scanning.
- **Verification:** 16 backend tests, 4 simulated-worker lifecycle tests, TypeScript and production export pass. Manual phone/laptop scan-and-cancel verification remains pending.

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

### Auth layout fix — 10 October
Allauth entrance pages bypassed account/base.html, leaving login unstyled. Added the current allauth/layouts/base.html override, responsive form styles and checkbox/focus treatment. Two regression tests verify branded forms and signup/login/logout/session behavior (SQLite).

### AI explanation resilience
Provider timeouts/network errors were not caught by the explanation endpoint. It now returns a recoverable JSON error; rule explanations remain usable. A regression verifies timeout recovery. A key-disabled API flow verifies parsing OCR text, review, Hindi/Telugu and PDF without provider calls; this does not replace real phone OCR testing.

### Visual verification blocked
Local browser preview was rejected by browser security policy (permission denied). No alternate browser workaround attempted. Production build passes; visual/physical-device QA explicitly remains pending in RELEASE_ACCEPTANCE.md.

### Disabled AI button (user reproduced)
User reported a prohibited cursor, not a provider error. Consent/auth gating disabled the button without an actionable explanation. The button now explains missing consent/auth, focuses consent and offers a sign-in link. Explicit consent remains required. Separately replaced unverified model default with documented gemini-2.5-flash and added safe provider error categories; live inference still pending.
