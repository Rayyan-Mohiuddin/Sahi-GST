# Sahi GST: final product vision and build priorities

Sahi GST is an **invoice review workspace for GST-registered small businesses**: capture a supplier document, understand what needs checking, request the right correction, and retain the review evidence. The owner should leave with a useful next action, not an unexplained compliance badge.

## The complete experience

**Capture → read → confirm → check → request → review a revision.**

- Capture through clearly separate file and camera options on a phone or desktop.
- Read using a free OCR engine, with visible loading/failure and manual recovery.
- Confirm critical identifiers against the source; preserve uncertainty rather than inventing missing values.
- Check supported arithmetic/field consistency with traceable deterministic rules.
- Request corrections using a reviewable supplier draft; record history and export evidence.
- Review a supplier-provided revision without pretending that editing the app repaired the original document.

This connected flow is our initial all-in-one workspace. Accounting, filing, payment collection and tax advice are separate products; do not fill the app with nonworking buttons for them.

## Current release priorities

1. **Core trust:** GSTIN spelling must be confirmed, unknown amounts stay unknown, checks have visible limits, original document stays unchanged.
2. **Mobile completion:** files/camera choices, Back closes review before leaving, legible critical fields and working copy/export. Validate on a physical phone after merging.
3. **Demonstration evidence:** real OCR regression inputs, known failures and manual recovery, supported live checks, two-minute video and truthful slides.

The mobile patch extracts upload, review dialog, GSTIN review, privacy and guide components. Navigation has view-specific browser history, while the review remains a responsive dialog. Overview/inbox/follow-up/report views still share the workspace host; full independent page routes are deferred until they justify a larger restructuring.

## After the core demo is stable

Benchmark an alternative OCR engine on the same failed images; improve exact GSTIN match rate and phone latency before switching. Then prioritize real revision/follow-up status, PDF support and tightly scoped user-uploaded reconciliation based on user interviews. No guaranteed ITC or automatic tax-rate classification promise.

## OCR decisions

The current browser engine is Tesseract.js. It downloads runtime/language assets and recognizes locally; parsing/checks still use Django. PP-OCR is a PaddleOCR model family, a plausible match to the user's remembered tool. PaddleOCR's Python pipeline documents UVDoc unwarping, and an official browser SDK exists. These capabilities are not proof that it reads our GSTINs more accurately, or that the browser SDK includes the whole Python unwarping pipeline.

See OCR_ENGINE_NOTES.md for sources, caching/privacy explanation and the benchmark gate. Do not replace the working engine with an untested dependency immediately before submission.
