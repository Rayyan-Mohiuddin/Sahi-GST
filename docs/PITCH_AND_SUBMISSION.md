# Pitch, visual direction and submission

All scripts describe the intended MVP. Before using them, remove any feature that is not live. No user validation, accuracy, speed or saved-money results exist yet.

## Opening lines

**Recommended interactive opening:** “This invoice looks ordinary. Its total is ₹1,000 too high. Would you spot it before forwarding it to your accountant?” Show the synthetic invoice immediately.

**Owner-focused alternative:** “The difficult part is not seeing that an invoice has a problem. It is knowing exactly what to ask the supplier to fix.”

**Trust-focused alternative:** “A green tick cannot tell you everything about GST. We show what we checked, what we found, and what still needs a person.”

Do not say all of India checks invoices only at filing time, or imply every error causes permanent ITC loss.

## Elevator speech — about 30 seconds

“Small businesses receive supplier invoices in different formats. When something is missing or the numbers do not match, the owner has to work out what to ask the supplier to fix. Sahi GST turns an invoice photo into a clear correction request. AI reads the fields, the owner confirms them, and tested rules show the mismatch and its evidence. It works through a phone browser, with no accounting-software migration. We start with ordinary B2B invoices and clearly flag what we cannot verify.”

## Ten-second version

“Sahi GST checks a supplier invoice, shows the evidence behind a mismatch, and helps a small-business owner request the right correction.”

## Two-minute demo/video

| Time | On screen | Spoken point |
|---|---|---|
| 0–12 sec | Synthetic invoice with ordinary appearance | Opening: the ₹1,000 total mismatch |
| 12–25 sec | Phone uploads image to live app | Name primary user and supported scope |
| 25–45 sec | Extraction review beside source | AI reduces typing; critical fields remain reviewable |
| 45–70 sec | Mismatch card showing observed/expected values | Deterministic arithmetic; precise evidence |
| 70–90 sec | Copyable supplier request | User leaves with a useful action; original remains unchanged |
| 90–105 sec | Corrected supplier sample/recheck, if implemented; otherwise clean case | Named checks pass, unverified areas stay visible |
| 105–120 sec | Live URL/QR and measured evidence, then roadmap | State actual performance and narrow future scope |

Prepare three tiny synthetic files: clean invoice, seeded arithmetic/missing-field invoice and unreadable/unsupported case. Also test a fresh supported image beyond the rehearsed example. A visible fixture is fine; hidden fake extraction is not.

If the network fails, say so, show the labelled manual-entry fallback and use the recorded successful run as backup evidence. Do not present playback as a live action. Keep video duration at or below 2:00; test narration at normal speed.

## Presentation: six slides

1. **Problem:** one person, one invoice, one unnecessary correction chase.
2. **Product:** source → finding → correction request, with real screenshots.
3. **Trust architecture:** AI extraction, confirmation, deterministic checks, visible limits.
4. **Evidence:** measured dataset size/accuracy/latency and user feedback, or explicitly “pilot pending.”
5. **Market and differentiation:** entry segment, current alternative, distribution experiment and payer hypothesis.
6. **Working result and next step:** live QR/link, shipped scope, team contributions, next integration.

Spend most time in the product. No fabricated traction, gigantic TAM number or “first AI GST platform” claim.

## Visual direction

Working brand: Sahi GST. Tagline: **“From invoice doubt to a clear next step.”** Avoid spending core-build time naming.

Use warm off-white canvas, deep ink text and one restrained teal accent. Use red/amber/green only for labelled findings. Dark ink title slides can contrast with the light invoice workspace. The invoice and its numbers are the hero; avoid 3D coin animations and irrelevant dashboards.

Proposed palette: background #F7F5EF, text #12232E, action #006B5E, issue #B42318, review #8A4B08. Verify actual contrast for each usage. Use system/locally available fonts, readable numeral alignment, generous spacing and 44px-ish touch targets. Do not rely on colour alone. Respect reduced motion.

Signature interaction: selecting a mismatch reveals the source field and the arithmetic explanation; “Copy supplier request” then gives a clean actionable message. Green can mean one check passed; it must not erase unresolved checks or supplier correction status. A short state transition is sufficient for polish.

Landing headline: **“Know what needs correcting.”** Subtext: “Review supplier invoices, understand mismatches, and prepare a clear correction request.” Primary CTA: “Check an invoice.” Secondary: “Try a sample.” Put the product above the fold rather than forcing judges through a marketing tour.

Do not add a generic chatbot unless a real task requires conversation. Structured findings are easier to scan in a short jury visit.

## Rubric strategy

| Criterion | Weight | What to prove | Evidence to prepare |
|---|---:|---|---|
| Working MVP | 30% | Core flow works on a fresh supported input | Hosted journey, error handling and repeat-run record |
| AI/SaaS relevance | 20% | AI reduces manual transcription in a repeatable workflow | Real extraction, schema review, measured quality and time comparison |
| UI/UX | 15% | User sees issue, evidence and next step without coaching | Phone demo, readable statuses and short user test |
| Market potential | 15% | User/payer/channel are credible | Specific interviews or clearly labelled hypotheses |
| Innovation | 10% | Distinctive execution, not a generic upload/chat wrapper | Evidence-led correction journey and honest abstention |
| Demo/pitch | 10% | Problem and working value are clear in two minutes | Rehearsed story, backup recording, working links |

The first three categories total 65%. This is a prioritization guide, not a reason to neglect submission quality or claim the rubric is only visual polish.

## Questions judges will likely ask

| Question | Answer to prepare |
|---|---|
| Why another GST tool? | Established tools are capable. We test a focused intake-to-correction flow for owners handling external invoices; no migration required. We must validate whether the added step is useful. |
| Why not ChatGPT? | This workflow persists confirmed fields, runs versioned deterministic checks and generates traceable findings. AI handles extraction; it does not decide the tax answer. |
| What is original? | Our implemented review/uncertainty/correction flow, rule integration, fixtures and evaluation. Disclose libraries, model and AI coding assistance per event policy. |
| What if OCR is wrong? | The source remains visible, critical fields are confirmable, and unknowns stay unknown. Wrong transcription can otherwise cause false findings. |
| Is this legally compliant? | It performs named checks within a narrow scope. It does not certify GST compliance, authentic registration or ITC eligibility. |
| How accurate? | Report measured field/finding metrics with sample count, held-out cases and failure rate. We have no accuracy figure before testing. |
| Can you verify a GSTIN is active? | P0 structure checks cannot. Live authoritative verification is a future integration with access and terms checked first. |
| Can it fix invoices? | It can fix extracted transcription and draft requests. A supplier must correct its issued document through the appropriate process. |
| Does it save tax? | We measure time and correction usefulness. An amount mismatch is not tax saved, and credit depends on more than invoice fields. |
| What if rules change? | Versioned applicability/source records and code tests; changes reviewed before release. The model does not improvise rules. |
| How do you make money? | Test business/bookkeeper plans after validating repeat use and unit costs. No paid-demand claim yet. |
| What happens without internet? | Real extraction requires network; app shows failure and a labelled manual-entry path. No offline-AI claim. |
| Is customer data safe? | Describe implemented ownership, deletion and retention controls and the chosen provider's actual processing policy; no absolute privacy promises. |
| What is live versus sample? | Sample invoices are synthetic. Identify which processing is real, what is manual fallback and which features are roadmap. |
| Why Django with Next.js? | It matches our team's skills; Django holds rules/auth/data, Next.js delivers the responsive review UI. |

## Submission checklist — complete by Sunday 07:00 IST

- [ ] Verify the official event instructions and time zone; current deadline is user-provided 11 October 09:00 IST.
- [ ] Source repository contains code, README setup, lockfiles, migrations, license/attributions and small synthetic fixtures.
- [ ] Record shipped versus unimplemented features accurately.
- [ ] ZIP below **10,000,000 bytes** for a conservative interpretation of 10 MB.
- [ ] Exclude node_modules, .next, dist, build outputs, virtual environments, caches, .git, logs, environment secrets, real invoices and large recordings.
- [ ] Keep necessary source, dependency manifests/lockfiles, migrations, .env.example placeholders and reproducibility instructions.
- [ ] Extract ZIP into a fresh folder and follow README; verify essential assets are present.
- [ ] Upload ZIP to Google Drive, set anyone with link can view, and verify download while signed out.
- [ ] Presentation export opens correctly and matches shipped functionality.
- [ ] Two-minute video plays from its share link without requesting access; audio and text are clear.
- [ ] Live product opens over HTTPS on a phone and a signed-out desktop browser; provide a safe demo-access path if login is required.
- [ ] Public demo contains only synthetic data and does not expose account secrets.
- [ ] Recheck extraction service quota, backend/database health and demo reset procedure.
- [ ] Both teammates' contributions are specific, accurate and backed by artifacts/commits.
- [ ] Confirm event policy on AI assistance and reuse; originality is not copying a competitor's code, branding, copy or full design.
- [ ] Submit all fields by **07:00 IST**, save confirmation and reopen links once.

Keep video and large slide exports outside the source ZIP unless the event explicitly requires them there. A 10 MB limit is not a reason to remove source files needed to rebuild.


## Walk-up jury pitch (30 seconds)
“Sahi GST turns an invoice into a clear next action. AI reads it, the user confirms uncertain details, and transparent rules catch missing fields and mismatched totals. We explain the findings in Hindi or Telugu and prepare a supplier correction message—so small businesses spend less time chasing invoice mistakes.”

Stay signed in. Show a labelled synthetic invoice, the planted total mismatch, its explanation, then supplier draft. Say “GST under review,” not “credit lost.” If live AI fails, disclose the failure and use local OCR or the labelled sample. AI proposes fields/wording; deterministic rules calculate findings. Do not claim live AI, physical phone coverage or interviews not evidenced.
