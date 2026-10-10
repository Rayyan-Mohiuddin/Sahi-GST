# Real OCR regression evidence

10 October 2026. Dataset: three generated, clearly labelled synthetic invoice images. This is a small controlled regression run, not a representative invoice accuracy benchmark.

## Observed results

- Correct present fields: **19/20** (money compared numerically; other fields exactly).
- Expected unknown fields correctly left blank: **2/2**.
- Misread: buyer GSTIN printed `27PQRST5678L1Z2`, OCR returned `27PQRST5678L122`. Parser preserved observed text; the identifier-structure hint flagged it for human review. No automatic GSTIN repair.
- First scan: **17,665 ms**, including worker/model loading. Next scans: **1,346 ms** and **1,329 ms** with cached language assets, on this Windows development machine.
- Three OCR calls completed; no cloud LLM or paid API was used.

The denominator covers only fields explicitly labelled in the manifest. It does not imply all 15 fields were present in every image. Plain-text parser fixtures previously reached 22/22 present fields; the image run is distinct and exposes an OCR error the text tests cannot reveal.

## Reproduce from repository root

Install the existing Python/frontend dependencies first. Use a current Node 22/24 runtime with TypeScript stripping support.

```powershell
# Images and manifest are already committed. Optional regeneration uses available fonts.
.\.venv\Scripts\python.exe scripts/generate_ocr_fixtures.py
node --experimental-strip-types frontend/scripts/evaluate-ocr.mjs
.\.venv\Scripts\python.exe scripts/evaluate_ocr_fields.py
```

The runner uses the same readInvoice lifecycle helper and Tesseract.js engine as the app, then sends the OCR text through the Python parser offline. It does **not** test browser upload, deployed HTTP/session handling, camera capture or physical-device performance. First use may download the free English model; results and cache go into ignored `.local/ocr-evaluation/`. No customer document is uploaded to a third-party API.

Committed inputs: `tests/ocr_images/layout-1.png` (currency/rates), `layout-2.png` (next-line values), `layout-3.png` (party sections and combined number/date), plus `manifest.json`. The selected fonts/machine may affect recognition; retain the committed images when comparing releases rather than silently regenerating them.

## Manual test after PRs merge

Upload each PNG to the live app and click **Read with free local OCR**. Compare with manifest values; confirm the GSTIN hint if the same character misread occurs. Add 3–5 consented/redacted invoice layouts, or synthetic replicas of those layouts. Record expected/observed values, image quality, failure messages and device/browser. Test cancel/retry separately.

Do not quote “95% accurate” as general product accuracy from 20 labelled values. A pitch-safe claim is: “We tested the real OCR flow on three synthetic layouts, recorded an identifier error, and surfaced it for human confirmation.”

## Next build priority

Use actual failed layouts to improve recognition/label parsing. If the core live loop is stable, prepare the final demo video/slides and signed-out link tests. Avoid adding filing, broad tax-rate inference or reconciliation immediately before submission.
