# Sahi GST — GST invoice checks with a clear next action

Updated: 10 October 2026, Asia/Kolkata. Product name: **Sahi GST**. Repository: [Salman-a-gamer/Sahi-GST](https://github.com/Salman-a-gamer/Sahi-GST). Brand availability has not been checked.

**Submission deadline: Sunday, 11 October 2026, 09:00 IST. Internal submission target: 07:00 IST.**

## What we are building

Sahi GST helps a GST-registered small-business owner or bookkeeper review incoming supplier invoices: upload a supported invoice, confirm the extracted fields, see evidence-backed missing-field and arithmetic checks, and copy a precise supplier correction request.

**Promise:** “Know what needs correcting before an invoice becomes a month-end chase.”

The initial user is a small Indian trading business receiving ordinary domestic B2B goods invoices. This is a recommended starting segment, pending interviews. An everyday consumer is not the same customer: consumer bill checking generally does not involve a business ITC claim.

## Current status

- Working local MVP: responsive overview, invoice inbox, image OCR, field confirmation, deterministic checks, correction drafts, saved reviews and JSON reports.
- Django Allauth account flow and session-isolated guest workspace implemented. PostgreSQL migrations and 10 backend tests pass; Next.js production export passes.
- Real local OCR and the invoice-to-request flow have been exercised in the browser. OCR can misread identifiers; human confirmation remains essential.
- On `feature/invoice-extraction`, OCR-text parsing now handles five additional synthetic layout patterns; 14 backend tests pass. Regression-set present fields improve from 7/22 to 22/22, and expected unknowns from 4/10 to 10/10. These are synthetic parser results, not real-image accuracy.
- Optional Gemini adapter is implemented but not live-key verified. The baseline has no API fee and does not need a key.
- Friend's live demo: [sahi-gst-d511.vercel.app](https://sahi-gst-d511.vercel.app/). Health/session and a synthetic invoice API flow verified on 10 October; PostgreSQL reports ready and cloud extraction is disabled. Current local confirmation/UI fixes require merge into the friend's deployed repo. No user interviews, real-world accuracy benchmark or legal certification is claimed.
- Twenty combined person-hours is the conservative planning budget. User said a minimum of about 20 hours; per-person availability remains unconfirmed.
- Core stack is locked: React via Next.js, Django, PostgreSQL, Django Allauth.
- No extra plugin was necessary for planning. No plugin installation is claimed.
- Contribution reminder's deadline/name were updated; its existing PAUSED state was preserved.

## Read in this order

1. [Strategy, problem and competition](docs/STRATEGY.md)
2. [MVP, rules and architecture](docs/MVP_SPEC.md)
3. [Two-person execution plan and Codex prompts](docs/BUILD_PLAN.md)
4. [Pitch, demo and submission checklist](docs/PITCH_AND_SUBMISSION.md)
5. [Research sources and unresolved verification](docs/RESEARCH.md)
6. [Difficulties and decisions](docs/DIFFICULTIES.md)
7. [Team contributions](docs/TEAM_CONTRIBUTIONS.md)
8. [Free AI and Vercel deployment](docs/FREE_DEPLOYMENT.md)
9. [Actual backend/API guide](docs/BACKEND_API.md)
10. [Continuation, collaboration and manual test work](docs/HANDOFF.md)

The user's operating preference is recorded in AGENTS.md: humans handle hosting dashboards and uploads; Codex spends usage on focused code/debugging. HANDOFF.md carries resume context and work to do during usage resets.

## Product boundary

Free browser OCR reads image text; a conservative label parser proposes fields. An optional Gemini adapter can provide structured extraction. The user confirms critical fields. Tested deterministic code checks arithmetic and supported rules. The original document remains unchanged.

Result categories are **Issue found**, **Needs review**, **Checked**, and **Not checked**. “Checked” means only that the named check passed. It does not establish active GST registration, authenticity, correct HSN classification, supplier filing, or input-tax-credit eligibility.

First supported format: clear JPEG/PNG image of one ordinary domestic B2B goods tax invoice. Restrict baseline tax-jurisdiction examples to supported Indian states and explicit, user-confirmed place of supply. Add single-page PDFs only after the image loop works. Unsupported scenarios get an honest scope message.

## The core journey

Upload → AI extraction → confirm uncertain/critical fields → rule findings with evidence → correction request → recheck a supplier-provided revision.

Editing an extraction fixes the app's transcription. A buyer does not repair a supplier-issued document by editing the app. Supplier correction remains pending until an actual revised document is reviewed.

## Repository structure

```text
frontend/             Next.js responsive UI
backend/              Django API, Allauth and deterministic checks
scripts/              Build and source packaging helpers
backend/invoices/tests.py  Synthetic rule and API tests
docs/                 Planning, evidence and submission material
```

## Run locally

Requires Node.js 22+ and Python 3.12/3.13, plus PostgreSQL. Docker users can run `docker compose up -d db` for the included local database. Use a UTF-8 database (required for rupee signs and Indian text).

PowerShell, from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
npm.cmd ci --prefix frontend
npm.cmd run build --prefix frontend
$env:DEBUG='1'
$env:DATABASE_URL='postgresql://sahi:sahi@localhost:5432/sahi_gst'
.\.venv\Scripts\python.exe backend/manage.py migrate --noinput
.\.venv\Scripts\python.exe backend/manage.py collectstatic --noinput
.\.venv\Scripts\python.exe backend/manage.py runserver 127.0.0.1:8000
```

Open http://127.0.0.1:8000. For frontend hot reload, start `npm.cmd run dev --prefix frontend` in another terminal and open its port 3000; it proxies API/account requests to Django on port 8000.

Environment files are examples only, not auto-loaded. Set variables in the shell or hosting dashboard. Production requires SECRET_KEY, DATABASE_URL, the exact allowed host and HTTPS CSRF origin; DEBUG must be 0. The optional DEV_SQLITE=1 switch is for a local smoke test only, not the production stack.

```powershell
.\.venv\Scripts\python.exe backend/manage.py test invoices
npm.cmd run typecheck --prefix frontend
python scripts/package_source.py
```

The package script uses tracked source files and fails at 10 MB. Dependency folders, database files, credentials and generated output are excluded from Git and the ZIP.

## Free platform scope

The connected workspace includes invoice history, review findings, supplier-request drafts and downloadable evidence. It is not a filing/accounting suite. No fake GSTN integration, automated supplier sending or payment system is presented as complete. Free OCR is neural OCR, not an LLM. First use downloads model assets; network is needed for the app's server checks.

Guest records are scoped to the session and visible for 24 hours; expired guest records are removed when the session endpoint next runs. Account records persist until deleted. Original image bytes are not saved by the app. Gemini, when enabled, has its own processing policy and requires explicit consent. Do not upload confidential invoices to an unpaid cloud tier without evaluating those terms.

## Success criteria

- A fresh supported image completes the live flow on a phone and a laptop.
- User can correct a misread field and see deterministic results update.
- Findings show observed value, expected relationship, explanation and next action.
- AI/network failure offers retry and a clearly labelled manual-entry fallback.
- At least one clean, one erroneous and one unreadable/unsupported example are demonstrated honestly.
- Source ZIP is below 10,000,000 bytes, reproducible, and free of dependencies, secrets and customer invoices.
- Source, ZIP link, slides, two-minute video, live link and individual contributions are submitted before the portal closes.

## Log maintenance

After every completed work block, record actual work and evidence in TEAM_CONTRIBUTIONS.md. Add encountered blockers, attempted fixes and verified outcomes to DIFFICULTIES.md. Keep anticipated risks separate from incidents. Update current status and setup instructions after each milestone.
