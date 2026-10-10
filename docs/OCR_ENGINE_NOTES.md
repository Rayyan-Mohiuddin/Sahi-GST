# OCR accuracy, local processing and alternative-engine decision

## What is happening on the device?

The website downloads JavaScript and a WebAssembly OCR runtime plus English language data when needed. Tesseract.js runs recognition in a browser Web Worker, using the phone/laptop CPU and memory. It does not install a native app or run a cloud LLM for the default scan.

Language data is cached in IndexedDB; downloaded web resources may also be browser-cached. Later scans can reuse those assets. Clearing site data, private browsing/storage limits or browser eviction can require downloading them again. A new worker is created for each scan and terminated afterward, but cached language data can remain. The first scan is therefore often slower. Current package defaults use LSTM language data from the best-int model distribution; no better-model switch has been benchmarked here.

The default source image is processed locally. The app sends extracted text to Django for parsing, and confirmed fields/results are saved in PostgreSQL. It still needs network/server access; full offline operation is not implemented. Optional Gemini mode separately sends the image to Google only after explicit consent.

Primary sources: [Tesseract.js FAQ](https://github.com/naptha/tesseract.js/blob/master/docs/faq.md), [Tesseract.js](https://github.com/naptha/tesseract.js). Runtime/model default checked in installed package source.

## Why GSTIN errors need special treatment

Fifteen-character identifiers have little natural-language context. Z/2, O/0 and I/1 can look similar, especially with blur, small text, compression, glare or screen photographs. A format check cannot catch every wrong identifier that happens to match the format. A checksum could reject additional mistakes but still would not establish active registration or prove identity; checksum is not implemented yet.

Current mitigation: preserve OCR text, highlight suspect structure, render GSTINs in larger monospaced fields, and require separate confirmation against the original when a value is present. Edits reset acknowledgement and overall confirmation. A genuinely missing GSTIN can remain blank so the app still reports missing-field findings. Never silently replace a character merely because a guessed replacement looks plausible.

For uploads: use an original PDF/image export when available (PDF support is still pending), or a sharp straight image without glare; include enough resolution for the GSTIN characters. A clear crop can help human review. Do not claim that these tips guarantee exact recognition.

## Should we try PP-OCR/PaddleOCR?

Yes, as a comparison experiment. The remembered name sounds like the PP-OCR family, though the exact tool/version is unconfirmed.

- [PaddleOCR official project](https://github.com/PaddlePaddle/PaddleOCR) publishes recognition models and reports an official browser SDK.
- [Python OCR pipeline](https://www.paddleocr.ai/main/en/version3.x/pipeline_usage/OCR.html) documents the optional **UVDoc** image-unwarping module. This is relevant to warped document photographs; curved-text detection and exact identifier recognition are different problems.
- [Browser SDK instructions](https://github.com/PaddlePaddle/PaddleOCR/blob/main/paddleocr-js/packages/core/README.md) describe browser detection/recognition through ONNX Runtime Web/OpenCV.js, worker support, model downloads and runtime/header configuration. Browser support for the full Python unwarping pipeline has not been established in this review.

No Paddle dependency has been installed or benchmarked in the shipped app. Open-source code can be free to use while model downloads, memory and server hosting still have costs or constraints. Keep heavy Python/GPU inference out of the free Django deployment until measured and proven feasible.

## Gate before changing the engine

1. Use the same 3 existing synthetic images plus 3–5 consented/redacted failed images; label both GSTINs exactly. No confidential files in Git.
2. Compare **exact complete GSTIN match**, overall field extraction, missed text and erroneous plausible identifiers. Count manual corrections separately.
3. Measure model download size, first-scan time, subsequent time, peak memory if available, phone/browser compatibility and cancellation.
4. Confirm any coordinates are real returned evidence and that source images stay local in browser mode.
5. Switch only when observed identifier quality improves and the phone flow remains usable. Keep manual confirmation and a working fallback.

The existing 19/20 field result on three synthetic images is too small to justify a general accuracy claim or select an OCR engine without the comparison.
