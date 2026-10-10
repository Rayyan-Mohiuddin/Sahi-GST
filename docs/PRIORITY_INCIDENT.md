# Priority incident: AI availability and phone warnings

10 October 2026. Both remain open until evidence confirms resolution. Pause feature/UI work.

## Verified
- Public production HTTPS GET/HEAD succeeds from this workstation; HTTP 200, HSTS, nosniff and frame protection present. Session reports PostgreSQL and AI configured. This does not prove Safe Browsing clearance or successful provider inference.
- User reports intermittent successful AI reading and generic provider-unavailable errors. Exact upstream code unknown. Do not attribute this to billing/free tier or a global Google outage.
- Shared main 1e206ed includes 2799471 but not emergency timeout commit ccaa0c0 at inspection. Merge remaining codex/demo-flow-fixes changes and redeploy.
- Provider logs now record only category/status/model/elapsed time, not key, raw error body or invoice. Targeted tests verify redaction.

## Human: one diagnostic run
1. Merge remaining branch changes and redeploy production. Keep billing disabled.
2. Vercel project -> Logs. Run one signed-in AI scan with synthetic invoice and explicit consent.
3. Filter logs for gemini_failure. Send that single line (not environment values or full logs).
4. 429: account quota/rate; wait or local OCR. 401/403: key restrictions/access. 404: model configuration. 500/503: provider service failure; retry once later/local OCR. Network category: request timeout/transport; inspect deployment timing.

## Phone warning: separate investigation
Record exact warning, full URL and browser. Do not bypass. HTTPS success is not a reputation verdict.
If Chrome says Dangerous site/Deceptive site, owner checks https://transparencyreport.google.com/safe-browsing/search and Search Console -> Security & Manual Actions -> Security Issues for this URL-prefix property. Supply affected URL/example finding so source can be investigated. Request review only after addressing findings or establishing/reporting a false positive; do not claim an unperformed cleanup. Review propagation is external, not fixed by changing CSS or creating a new domain.
If warning says connection not private, record the NET:: error, phone clock and exact hostname; troubleshoot certificate/domain/network rather than assuming Safe Browsing.
Other browsers/network filters require their specific warning/provider process. No device warning was independently reproduced here.

Sources: https://support.google.com/chrome/answer/99020 and https://support.google.com/webmasters/answer/9044101 . Public Google status/transparency pages did not yield a readable current verdict through the research tool; no outage/clearance claim.

## Supplied production evidence
User supplied /api/extract/ 502 with execution 35.14s and generic invalid-fields text. This closely matches urllib timeout=35; timeout is leading hypothesis, not proof until category log. Vercel reports firewall Allowed and bom1->iad1 routing. No outgoing requests in platform telemetry is not proof urllib made none. Added distinct timeout504/network502/invalid-fields502 and direct/wrapped timeout classification; 14 targeted tests pass. Model value still requested. Do not increase paid quota or claim provider restored.
