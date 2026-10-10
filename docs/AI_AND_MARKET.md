# AI relevance, market evidence and signature features

## Honest AI story

The intended primary flow is **Gemini reads the invoice pages and proposes structured fields → human confirms → deterministic rules check → AI can explain saved findings in plain language**. Local neural OCR remains an explicit backup. The app does not label rule templates as AI or claim a model decided tax validity.

Current implementation has a schema-constrained Gemini adapter, ordered multi-image inputs, invoice/other/uncertain classification, nullable fields and uncertainty hints. AI wording references saved finding IDs; unrecognized IDs, digits in narrative and certain unsupported claims are rejected. These controls are not a proof of model factual accuracy; the original rule evidence remains visible and human confirmation is required.

AI has meaningful value if it reduces transcription/correction effort on actual invoice layouts. Demonstrate that with a live free-key run and a comparison against manual/local OCR. A configured key or mocked test is not live-provider verification.

Neural OCR itself is AI. An LLM is useful here for layout-aware structured extraction and understandable wording, not simply to add an AI badge. Current language controls explain findings; the rest of the interface/PDF remains English. Hindi/Telugu wording and device voices require native-speaker/phone checks before claiming polished localization.

## Owner setup (no dashboard automation)

In Vercel's project environment, set **GEMINI_API_KEY**, **GEMINI_MODEL** to a model explicitly available on your unpaid account, and **GEMINI_FREE_TIER_CONFIRMED=1** only after checking billing/quota. Keep secrets out of chat/Git. Merge the code and redeploy, sign in to the app, choose synthetic/redacted pages, grant image-processing consent, and run AI reading. No automatic paid fallback exists. Quota/provider failure keeps the local OCR/manual paths available.

Google currently lists a free tier for selected models, with limits and different data-use terms. See [pricing](https://ai.google.dev/gemini-api/docs/pricing) and [structured outputs](https://ai.google.dev/gemini-api/docs/structured-output). Model availability/quota must be confirmed in the owner's account.

## Market evidence on the page

[PIB's 30 June 2026 release](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2279318) reports **1.65 crore GST taxpayers as of May 2026**, versus 66.5 lakh in 2017. The Market view labels this as ecosystem context, not our addressable paying market.

Entry user: GST-registered small-business buyer/bookkeeper reviewing supplier invoices. Value hypothesis: less transcription and clearer correction follow-up without switching accounting software. Payer/channel hypotheses remain unvalidated; do not claim government statistics establish willingness to pay.

No interview quote has been supplied or verified. Do not invent one. For each quote, record anonymised role, interview date, exact approved text, context and permission. Ask for a concrete correction episode, current workflow and whether the supplier message is useful. Then publish only approved evidence.

## Signature feature decisions

| Requested feature | Current decision |
|---|---|
| Rupees at risk | Implemented as **GST amount under review**, once per invoice, computed from confirmed nonnegative tax components. Not blocked ITC/loss/savings; eligibility needs separate assessment. |
| Hindi/Telugu explanations + voice | Implemented rule templates and optional AI wording. Speech selects installed local voices only; availability varies. Native-speaker and physical-phone review remain required. |
| Supplier message | Copy and user-initiated WhatsApp sharing. User chooses recipient and sends; no automatic messages. |
| Uncertainty highlighting | Existing parser hints plus Gemini uncertainty list; confirmation resets on edits. |
| Check ID + tamper-evident QR | Deferred. UUID alone is not tamper evidence; public sharing of financial data needs an explicit design. |
| Supplier reliability score | Deferred. OCR mistakes and repeated review versions could distort the score; do not imply fraud/creditworthiness. |
| Photo-quality warning | Deferred until blur/darkness thresholds are tested. Camera preview is now live; no unverified quality guarantee. |

Pitch: **“Invoice Health Check: understand the invoice, confirm the numbers, and request the right correction in your language.”** Use the actual live AI mode in the demo; label the fallback honestly.
