# Focused homepage review — 11 October 2026

Base: friend's codex/focused-fintech-home at 122b63d. Review branch: codex/focused-home-review.

## Changes in this review
- Retain friend's slim home header, two primary actions, synthetic invoice example, workspace-only stats/history, labelled unsaved demo toggle, severity-order findings and font preloads.
- Shorten pain headline to fit mobile: “One wrong digit can delay your business.” Scope-qualified upload copy and explicit supported-invoice line replace unsupported “any GST invoice” and implied credit determination.
- Compact invoice card on mobile and use two columns at 768px. Header/hero reserve viewport space; actual fit remains to be visually checked.
- Demo table is explicitly illustrative. Rows no longer all open DEMO/1042 despite showing other IDs. Actual sample remains reachable from Home.
- Ivory focus outline on navy header. No rule/extraction/API changes in this review relative to 122b63d.

## Verified
- 47 backend tests, local SQLite mode. First failure was missing pypdf in local environment; installing the dependency already declared in source restored all tests. No backend source change.
- 14 frontend tests pass.
- Next production export includes successful TypeScript validation.
- Primary text contrast ratios: navy/ivory 13.80, saffron/navy 5.59, muted/ivory 5.97, error text/pale error 7.03, amber text/pale amber 6.51, passed text/pale green 6.36. These are calculated colour-pair checks, not a full accessibility audit.
- Git-connected existing Vercel projects automatically deployed commit fcb3dab successfully. Canonical preview: https://sahi-gst-d511-b3lth9ekj-rayyan-mohiuddins-projects.vercel.app/ . Deployment success is not app-flow acceptance.
- Production before screenshots saved at 360x800 and 1280x800: review-before-360.jpg and review-before-1280.jpg.

## Blocked / not claimed
Preview shows Vercel “You Need Access” for our existing account. Owner approval requested; protection remains enabled. Local http://127.0.0.1:8011/ is denied by saved browser permissions. No alternate browser workaround attempted. User asked to allow the address if local visual checks are wanted.

Consequently after screenshots at 360/768/1280, viewport-overflow checks, Lighthouse mobile performance/accessibility, keyboard flow and preview sample/upload/camera/findings/languages/draft/PDF are PENDING. Do not claim scores, fake screenshots, live-provider success or hardware coverage. Do not merge until flow checks pass. Existing friend's after-local screenshots describe 122b63d, not this patch.

## Next bounded task once access is granted
Open canonical preview (or local address if its saved permission is changed), check 360x800, 768x1024, 1280x800; save after screenshots and measured overflow. Run the sample with explicit confirmation; inspect severity/evidence, switch Hindi/Telugu, inspect draft and download PDF. Upload a synthetic fixture and test camera permission handling. Physical capture and installed voice require the owner's real device. Run Lighthouse against accessible app URL; no credentials/bypass tokens committed. Record exact scores and failed audits.

Human owns preview approval and actual phone camera/voice verification. Branch is unmerged. Prefer reviewing against codex/focused-fintech-home so this UI review does not appear to introduce friend's pre-existing backend changes.
