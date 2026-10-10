# How the backend and API work

Verified against friend's commit `3c349a8` plus the confirmation/UI patch developed on 10 October 2026. Live API tested at https://sahi-gst-d511.vercel.app. Backend/API behaviour below is actual implemented behaviour, not the larger planning roadmap.

## One request journey

```mermaid
flowchart LR
  A[Image in browser] --> B[Tesseract.js neural OCR]
  B --> C[POST /api/parse/]
  C --> D[Human confirms fields and scope]
  D --> E[POST /api/reviews/]
  E --> F[Python Decimal checks]
  F --> G[(PostgreSQL review record)]
  G --> H[Findings and supplier draft]
```

1. The browser accepts a JPEG/PNG under 5 MB and at most 20 megapixels. Tesseract.js reads it locally. First use downloads OCR assets; this is not an offline guarantee.
2. OCR text goes to Django's `/api/parse/`. A regex label parser proposes fields. Missing labels remain null. It does not infer a product's legal tax rate or fill missing taxes with zero.

Parser update on `feature/invoice-extraction`: labels can be colon-separated or whitespace-separated, values may follow on the next line, currency prefixes/grouping are normalized, and tax percentages are kept distinct from monetary amounts. Explicit supplier/buyer headings can assign a bare GSTIN; a bare unscoped GSTIN stays unknown. ISO/named-month dates normalize to YYYY-MM-DD; ambiguous numeric dates stay null. Repeated conflicting values stay null. Five synthetic OCR-text layouts and additional safety regressions pass; no real-world OCR accuracy figure is claimed.
3. The person confirms fields against the original and confirms the limited invoice scope. After an edit, the updated frontend requires fresh confirmation.
4. `/api/reviews/` runs deterministic checks, stores a review and returns findings plus a correction draft. Each run is a new record; it does not overwrite the original review.
5. The frontend displays saved history, drafts and JSON exports. Copying a draft does not send it or mark an invoice resolved.

## Tools/libraries and their jobs

| Component | Tool | Job |
|---|---|---|
| Interface | Next.js 16 / React 19 / TypeScript | Responsive workspace; static production export |
| Icons | Lucide React | UI icons |
| Free extraction | Tesseract.js | Browser neural OCR, no LLM API required |
| API and web app | Django 5.2 | URLs, sessions, CSRF, requests, persistence |
| Authentication | Django Allauth | Username/password signup, login and logout; email verification currently disabled |
| Database | PostgreSQL / psycopg / dj-database-url | Durable users, sessions and JSON review records |
| Exact arithmetic | Python Decimal | Money/rate checks without binary float errors |
| Optional cloud image reading | Gemini REST API via urllib | Image-to-fields extraction, only if configured and explicitly consented |
| Image validation | Pillow | Verify cloud-upload bytes/type/dimensions |
| Static assets | WhiteNoise | Django assets locally; Vercel serves collected assets in its deployment flow |
| Deployment | Vercel Python/Django support | Root WSGI entrypoint with Next.js export included |
| Alternative server packaging | Docker / Gunicorn | Optional single-container deployment; not required for the live Vercel demo |
| Development | Codex, Git and GitHub | Implementation, focused tests, version control and collaboration |

Neon was the planned free PostgreSQL provider. The live API confirms PostgreSQL, but it does not expose the provider; confirm the actual database provider in the owner's dashboard rather than assuming it.

## Actual endpoints

All routes have a trailing slash. POST/DELETE requests require Django CSRF handling. The frontend first calls `/api/session/`, then sends the `csrftoken` cookie value in `X-CSRFToken`; cookies maintain the session.

| Method and path | Input | Output / purpose |
|---|---|---|
| GET `/api/health/` | None | Database `SELECT 1`; 200 when ready, 503 if unavailable |
| GET `/api/session/` | Session cookies | Auth state, username, cloud configuration and database type; creates guest session and clears expired guest reviews |
| POST `/api/parse/` | JSON `text`, up to 30,000 characters | `fields`, `review_fields`, `extracted_count`, `field_count`, source `local_ocr` and review warning |
| GET `/api/reviews/` | Session/account | Up to 100 newest reviews belonging to that user/session |
| POST `/api/reviews/` | JSON `fields`, `source`, `scope_confirmed: true`, optional `original_id` | 201 with a newly saved review, deterministic result and draft |
| GET `/api/reviews/{uuid}/` | Session/account | Owned review and draft; another session receives 404 |
| GET `/api/reviews/{uuid}/image/` | Session/account | Saved original image; owner/session checks and private no-store cache policy |
| GET `/api/reviews/{uuid}/report/` | Session/account | Downloadable readable PDF; owner/session checks |
| GET `/api/reviews/report/` | Session/account | PDF of up to 100 owned review records |
| DELETE `/api/reviews/{uuid}/` | CSRF + ownership | Deletes the owned review; does not delete other users' reviews |
| POST `/api/extract/` | Multipart `file`, `consent=true` | Optional Gemini structured fields; requires signed-in user and configured free-tier consent flag |
| `/accounts/…` | Allauth forms | Signup/login/logout with sessions and CSRF |

The old `/api/invoices/` endpoints in MVP_SPEC.md are proposed design names. They are **not implemented routes**; use this table for actual integration.

## Confirmed field schema

Text/date fields: `supplier_name`, `supplier_gstin`, `buyer_name`, `buyer_gstin`, `invoice_number`, `invoice_date` (YYYY-MM-DD), `place_of_supply`, `description`.

Numeric fields represented as strings or null: `taxable_value`, `tax_rate`, `cgst`, `sgst`, `igst`, `round_off`, `total`. Maximum field length is 500 characters. GSTIN text is uppercased and spaces removed; that normalization is not identity verification.

Example request:

```json
{
  "fields": {
    "supplier_name": "Synthetic supplier",
    "buyer_name": "Synthetic buyer",
    "invoice_number": "DEMO/001",
    "taxable_value": "10000",
    "tax_rate": "18",
    "cgst": "900",
    "sgst": "900",
    "igst": "0",
    "round_off": "0",
    "total": "12800"
  },
  "source": "sample",
  "scope_confirmed": true
}
```

Identifiers/date/description omitted above produce review findings; the total check still finds arithmetic expected `11800.00`. This is a synthetic arithmetic example, not a product-rate recommendation.

Response contains `id`, `fields`, `result`, `source`, `status`, `created_at`, `original_id`, `draft`. Result contains rule version, findings, counts, unchecked areas and overall status. Findings contain `rule_id`, field, status, title, message and observed/expected values where applicable.

Parser hints (separate from validation findings) include `field`, `reason`, `message`, and optional observed-line `evidence`. Reasons are `not_extracted`, `uncertain_value`, `conflicting_values`, and `identifier_structure`. Extracted count is only how many non-null values were proposed; it is not accuracy or calibrated AI confidence. Evidence is a text excerpt, not an invented image bounding box. The frontend clears a hint when the user edits its field and still requires full field confirmation.

`frontend/lib/ocr.ts` bounds a local scan to 90 seconds and handles cancellation while the worker loads or recognizes. It terminates workers, including workers that arrive after cancellation, and does not publish late output. This is browser-side OCR recovery; optional cloud processing keeps its existing server timeout. `npm run test --prefix frontend` exercises worker lifecycle with simulated workers using a current Node 22/24 runtime.

## Rules and boundaries

- **F01:** named fields present; absent/unreadable fields need confirmation.
- **I01:** GSTIN character pattern only. Checksum, active registration and authenticity are not checked.
- **I02:** invoice-number character/length review within the supported context.
- **I03:** parse date and flag implausible future dates for review.
- **M00:** missing/invalid/negative numeric inputs need review; unknown is not zero.
- **M04:** taxable value + CGST + SGST + IGST + explicit round-off compared with printed total using Decimal/paise rounding.
- **M02:** single printed rate × taxable base compared with aggregate tax; different rounding or multiple rates need human review.
- **M03:** mixed IGST and CGST/SGST prompt review; no jurisdiction inference is made.

Statuses: `issue`, `review`, `pass`, `not_checked`. A review becomes `checked` when the supported checks have no issue/review findings; it is not complete GST compliance. HSN classification, legal rate, place-of-supply applicability, GSTR-2B matching, filing and ITC eligibility stay explicitly unchecked.

## Storage, ownership and revisions

`Review` stores a UUID, nullable account owner, guest session key, confirmed fields JSON, result JSON, extraction source, status, optional original-review UUID and timestamps. Users and sessions use Django/Allauth tables.

Logged-in queries filter by owner. Guest queries filter by session and a 24-hour window. Expired guest records are deleted on the next session-endpoint request, not by a precisely timed background scheduler. Account reviews persist until deleted. Guest and account histories are separate.

Image retention is now optional and explicit. POST reviews can include `save_image: true` plus base64 `image_data`. Django verifies the actual JPEG/PNG bytes, 5 MB and 20-megapixel limits, then stores original bytes/mime privately in the review row. Metadata responses include protected `image_url` and `report_url`; list queries do not load image blobs. With no new image, a selected saved image can be inherited from the owned original review. Deleting/expiring the review deletes its image. Older images that were never stored remain unavailable. `original_id` links review runs but does not prove supplier correction or resolve older drafts.

`/api/parse/` also returns `document_check`, screening OCR text for independent invoice/reference/amount/party cues. Local-OCR review creation requires invoice-like OCR text (`ocr_text`); unrelated or unrecognized text gets 422. This is a content heuristic with possible false positives/negatives, not authenticity or tax-document classification. Manual entry without the rejected image remains available.

PDF reports use the free ReportLab library with bundled fonts, wrapped tables/findings, rule version, unchecked areas and supplier draft. They use INR labels and IST timestamps. JSON remains optional developer data. The frontend Finish action closes the already saved review; it does not mark supplier issues resolved. Workspace dropdown actions open the inbox/privacy view or sign-in/sign-out; multiple organization workspaces are not implemented.

## Optional LLM and zero-cost operation

The checked live deployment returned `cloud_extraction: false`. Its working baseline is neural OCR plus rules, not a currently running LLM.

Gemini requires server-side `GEMINI_API_KEY`, a model available to the account and `GEMINI_FREE_TIER_CONFIRMED=1`. The adapter requires login, explicit image consent, a 20-second session scan interval, file verification and a 35-second provider timeout. Failure returns an error; no paid provider is automatically selected. Model/account free quota and data terms still need owner verification before enabling it.

## Deployment fixes from the friend

Four commits (`739186f` → `3c349a8`) flattened root requirements, added pyproject metadata/entrypoint, changed vercel.json to `config/wsgi.py`, and added a root config package/WSGI shim that loads backend modules. This fixed Vercel discovery while preserving the Django implementation. `scripts/vercel_build.py` installs/builds Next.js and runs migrations.

Configuration values belong in the hosting environment: production SECRET_KEY, PostgreSQL DATABASE_URL, allowed host and HTTPS CSRF origin; DEBUG=0. Do not commit database passwords or API keys. See FREE_DEPLOYMENT.md for the original route; use the actual deployed root configuration now.

## Verification on 10 October

### Multi-page / AI additions

`ReviewPage` (migration 0003) stores additional ordered page images with cascade deletion; the existing first-image fields/routes remain compatible. Responses add `image_urls`; `/api/reviews/{uuid}/pages/{page_id}/` enforces review ownership. Up to 5 pages, **3 MB total**, keep base64-encoded saving under Vercel's 4.5 MB request limit. Local OCR reads pages sequentially, then parses combined text; it does not add invoice totals across pages. Different/conflicting values remain reviewable.

`POST /api/extract/` accepts repeated `files` (legacy `file` still supported), requires login/consent/free-tier configuration, verifies all image bytes, and sends ordered images to schema-constrained Gemini. It returns classification, nullable fields and uncertainty hints. `POST /api/reviews/{uuid}/explanations/` accepts `language` en/hi/te and optional `use_ai:true`; default returns labelled rule templates. AI mode is owner-protected and login/quota/configuration-gated, with validated finding IDs; it never changes saved findings or calculations.

Rule results add `tax_context`, summing confirmed tax components with Decimal once per invoice. This is invoice GST information, not an ITC eligibility or loss estimate. Missing/invalid amounts yield null. No source image is sent to Google automatically; consent resets when pages change. Local speech uses installed local voices; text stays available without one.

- Live health and session endpoints: 200; database reports PostgreSQL; cloud extraction disabled.
- Live synthetic API test: CSRF/session, parsing, review creation, expected arithmetic, draft and guest isolation passed; test record removed.
- Earlier local PostgreSQL suite: 10 tests passed. After importing deployment fixes, local SQLite smoke-test suite (10 tests), root WSGI import, TypeScript and production Next.js export passed. Current live PostgreSQL behaviour was checked separately.
- Browser local OCR was tested earlier. Real-world extraction accuracy and physical-device coverage remain unmeasured; use the manual testing list in HANDOFF.md.

## Release update
Live session now reports cloud_extraction=true (10 October, user configured/redeployed); this supersedes earlier disabled snapshots, but real inference remains pending. Explanation endpoint catches timeout/network/malformed-response errors with JSON 502 and preserves rule wording. Authentication uses backend/templates/allauth/layouts/base.html; account/base.html is a compatibility wrapper. Current image limits are 5 pages and 3 MB combined, superseding the old single-image 5 MB description. See RELEASE_ACCEPTANCE.md for verification scope.

### Demo release changes
AI adapter now defaults to gemini-2.5-flash, normalizes whitespace/models prefix and returns safe HTTP-category guidance. For supported 2.5 Flash models thinkingBudget=0 avoids using the limited output budget on reasoning. No retries to paid providers. User reported button-disabled prerequisite friction; no actual live provider error reproduced yet. The UI combined confirmation still submits scope_confirmed=true only on explicit Confirm and check. PDF ID is a record reference, not signature/tamper verification.

### AI failure diagnostics (local patch, pending deployment)

`/api/extract/` provider failures now include `reference`, `error_code`, `provider_http_status` (nullable) and `provider_status` (nullable, allowlisted Google status). `error` remains the frontend-readable message and includes the reference and upstream HTTP status when available. The app still returns HTTP 429 for upstream quota errors and 502 for other provider failures. Vercel logs contain `gemini_failure` with the matching reference, operation, safe model name, category and upstream status; provider payloads/messages, keys and invoice data are never logged. Categories distinguish HTTP, connection, timeout, invalid-response and internal errors.

Transport retries HTTP 500/502/503/504 once on the same model after 1–1.5 seconds. Each socket timeout is at most 35 seconds and reduced against a shared 45-second budget; retries are skipped if fewer than five seconds would remain after the delay. This is a socket/request retry budget, not a hard wall-clock cancellation guarantee for urllib. Other HTTP errors, network failures and invalid output are not automatically retried. The existing 20-second session rate limit and consent/login gates still apply. This shared transport also serves explanation requests; their existing rule-fallback error messages remain unchanged.

The user identified their model as Gemini 3.8 Flash. The default/example now use exact API ID `gemini-3.8-flash`; explicit environment values still override the default. For this model the adapter omits deprecated sampling parameters and uses `thinkingConfig: {thinkingLevel: "low"}`, consistent with Google's [3.8 generateContent guide](https://ai.google.dev/gemini-api/docs/generate-content/latest-model). It retains structured output and ordered inline images. Explicit 2.5 Flash models retain `temperature: 0` and `thinkingBudget: 0`. Request-payload regressions pass, but live 3.8 inference has not been verified.
