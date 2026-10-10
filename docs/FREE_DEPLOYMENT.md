# Zero-cost deployment and AI

Updated 10 October 2026. Deadline: Sunday 11 October 09:00 IST; submit by 07:00 IST.

## Zero-cost core

The running baseline needs no LLM API key. Tesseract.js runs a neural OCR engine in the browser. This is machine-learning OCR, **not an LLM**. The image is read locally; extracted text goes to Django's conservative label parser; a person confirms fields; deterministic Python checks run on the confirmed values. First use downloads OCR engine/language assets from third-party CDNs. Offline use is not promised.

The observed synthetic-image test misread GSTIN characters. Human review is necessary. Do not pitch OCR as perfect structured extraction. The optional Gemini adapter can improve extraction, but has not been tested with a live key in this session.

## Optional free LLM

[Google's pricing page](https://ai.google.dev/gemini-api/docs/pricing) lists free-tier access to selected models with quotas and product-improvement data use. Create/use an unpaid API project, select a model explicitly listed with a free tier, and confirm its actual quota. Do not attach billing, enable paid fallback, or upgrade to solve a quota error.

Set GEMINI_API_KEY only in server environment settings, GEMINI_MODEL to an available free-tier model and GEMINI_FREE_TIER_CONFIRMED=1 only after checking the account. The adapter defaults to gemini-3.8-flash based on the pricing page read during this session; model availability must still be checked in the account. No client-side key or key committed to Git.

Cloud scans require sign-in and per-upload consent. Use synthetic or suitably redacted invoices on unpaid cloud processing; do not send confidential financial documents into a free-tier product-improvement pipeline. Quota exhaustion returns an error and the local OCR option; there is no automatic paid provider.

## Existing Vercel account: preferred route

Vercel currently documents Django support. This repository has a root manage.py, requirements.txt and vercel.json. The build script exports the Next.js client, migrates PostgreSQL, and Django serves the UI and API on one origin. The frontend remains Next.js/React; the backend remains Django/Allauth. [Vercel Django documentation](https://vercel.com/docs/frameworks/full-stack/django)

Steps requiring the owner's account:

1. Sign in to Vercel and import Salman-a-gamer/Sahi-GST. Use the repository root and the Django framework preset.
2. Add **Neon Free** through Storage/Marketplace, inspecting the selected plan before creation. Do not choose paid compute, a trial requiring later payment, or upgrades. Connect it to this project so DATABASE_URL is supplied. [Neon integration](https://vercel.com/marketplace/neon)
3. Add a random SECRET_KEY. Set DEBUG=0. Add the exact live hostname to ALLOWED_HOSTS if not covered by Vercel's project environment variables. Set CSRF_TRUSTED_ORIGINS to the exact HTTPS live origin.
4. Keep Gemini variables unset for the free local-OCR baseline.
5. Deploy. The build runs migrations. Test /api/health/, a fresh guest session, signup/login, an OCR image and correction export.
6. Test the live URL signed out. If Vercel deployment protection blocks judges, adjust the intended public demo's access deliberately; keep the GitHub repo private unless a public repo is desired or required.

Vercel Hobby has eligibility and usage limits, including personal/noncommercial restrictions. Verify that the hackathon demo fits the current plan. Free quota is not unlimited uptime or production capacity. No paid service has been authorized.

## Alternative if Vercel deployment is unsuitable

Dockerfile and render.yaml package the Next.js export and Django into one free Render web service with an external free PostgreSQL database. [Render free limits](https://render.com/docs/free) include sleeping and monthly runtime limits. Render's own free PostgreSQL expires after 30 days; do not describe it as permanent free storage.

## Current verification boundary

Friend's deployment https://sahi-gst-d511.vercel.app now responds successfully; live health/session and a synthetic API flow verified on 10 October. It reports PostgreSQL and cloud extraction disabled. The friend fixed Vercel entrypoint discovery using root config/wsgi.py and pyproject.toml; preserve those files. Backend/API details and remaining verification are in BACKEND_API.md and HANDOFF.md.

The user handles dashboards/deployments from now on. Merge new code into the deployed repository and let the owner redeploy; ask for concise build errors only when needed. Avoid continuing the earlier duplicate dashboard setup.
