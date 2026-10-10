# Jury response: evidence, privacy and idea evaluation

Research date: 10 October 2026. This is a prototype evaluation plan, not a legal opinion, certification or completed interview record.

## What the jury feedback means
A working prototype establishes implementation, not demand, tax correctness or permission to process client documents. Four separate questions: do buyers/bookkeepers have a repeated problem; do CAs agree with the rule scope; can users complete the flow; can we operate it responsibly and sustainably?

Until evidence arrives, say: “We have built and internally tested the prototype. Practitioner validation and customer pilots are next.” Jury feedback is not CA certification or an endorsement. No CA review or approved interview quote is recorded in this project.

## CA interview kit (human sends; not sent by Codex)
Find two practising GST CAs through existing contacts, college alumni or ICAI's CA Connect/member resources. Verify credentials through the official directory where appropriate. A CA contact is not ICAI approval.

Suggested message: “We are students building Sahi GST, a narrow supplier-invoice review prototype. Could you spare 15 minutes to critique five synthetic cases and tell us where our findings could mislead? We are not asking for endorsement or client invoices. We would publish your name/words only with separate approval.”

Interview BEFORE the demo:
1. Tell us about the last supplier-invoice correction you handled. What happened, who found it and what was the next action?
2. How often does that occur? Can you estimate from a recent period rather than guess generally?
3. Who checks incoming invoices today, with which tool? What remains manual?
4. Which mistakes need immediate action; which are harmless rounding or OCR errors?
5. Would another review step help or duplicate existing accounting/reconciliation work?
Then show clean, missing-field, wrong-total, ambiguous-GSTIN and outside-scope examples. Ask the CA to mark expected findings first, then compare our output. Ask which wording is misleading, particularly GST under review, GSTIN validity and ITC.
Finally ask for one redacted/synthetic layout they can recreate and whether they would supervise a small pilot. Do not ask for confidential client files.

Record privately: interview ID/date, role, workflow, concrete episode, observed behavior, objections, exact quote, rule changes requested, follow-up. Separate consent to participate, recording, quote use and name/firm use. Default no recording and anonymised notes. Keep names/contact details out of the public repository. For public use obtain explicit final wording/context approval; professional endorsement/publicity restrictions may apply to CAs. Never use ICAI logo or “CA certified” without a genuine permitted basis.

Safe publishable form after actual review: “Two practising GST CAs reviewed [specific rules/cases] on [date]; they identified [findings]. We changed [items]. This was feedback, not certification.” Before review: “Practitioner review pending.”

## Professional evaluation: free method, not a validation badge
Use Strategyzer's hypothesis/experiment approach, a one-page business model and Google Forms/Sheets or local CSV. AI idea scores and market-statistic websites do not prove demand. Do not pay for a score.

| Dimension | Current evidence | Next experiment | Proposed decision gate (not a result) |
|---|---|---|---|
| Desirability | Jury interest; no customer interviews | 3 bookkeepers describe last correction episode before demo | At least 2 independently report repeat pain and show a concrete workaround |
| Domain correctness | Versioned narrow rules and synthetic tests | 2 GST CAs label cases independently, resolve disagreement | No unresolved critical misleading finding; explicit exclusions accepted |
| Usability | Prototype; physical coverage incomplete | 5 people perform scan-to-draft without coaching | At least 4 finish; measure time and blockers |
| Reliability | Tiny synthetic OCR benchmark; intermittent cloud/timeouts | 20 held-out cases, 2 phones, laptop; repeat network tests | Publish counts and latency; no false claim broad accuracy |
| Viability | Payer/channel hypotheses only | Ask who approves spending; offer a defined pilot | Concrete pilot commitment, not compliments; assess support/hosting costs |
| Privacy/security | Ownership tests, optional image storage, consent | Review data map, retention, provider terms, warning incident | No real confidential data on unpaid Gemini; unresolved warning blocks broad launch |

20-case proposal: 5 correct supported, 8 supported with planted issues, 4 poor/ambiguous captures, 3 out-of-scope. CAs approve ground truth before testing; held-out cases must not be tuned on. Score exact GSTIN matches, field transcription before edits, detection after confirmation, false issue flags, abstention on ambiguity/out-of-scope, time-to-draft, P50/P95 latency and failures. Report raw numerators/denominators and small-sample limitation. Proposed pilot thresholds are team choices, not industry standards.

Counterbalance manual-first/app-first order when comparing task time; identical practice exposure. Never count developer correction as AI accuracy. A missing/uncertain warning is different from a false confirmed-error flag.

## Publishability and privacy
A public synthetic demo is different from a production service for client financial documents. Present named checks and limitations; do not promise tax savings, ITC approval, authentic GST registration or whole-invoice legal compliance. CA input does not replace privacy/security/legal assessment.

Critical current provider constraint: Gemini unpaid terms permit product/model improvement and human review, and tell users not to submit sensitive, confidential or personal information. Consent does not override that restriction. For this zero-cost prototype use SYNTHETIC invoices for cloud AI. Blacking out a name alone does not make a real invoice safe: GSTIN/PAN-derived identifiers, addresses, signatures, bank/UPI/QR codes, line items and commercial terms may remain identifiable/confidential. A future real-client service needs a permitted processing arrangement or validated local/self-hosted pipeline; no paid service is being enabled.

Data map:
- Browser local OCR: image recognition runs on device. OCR text/confirmed fields still go to Django; this is NOT fully offline.
- Cloud extraction: selected images go through Django to Google after consent.
- Database: confirmed fields/results; optional source images; account/session linkage.
- Guest expiry: 24-hour query restriction and cleanup on session access, NOT a guaranteed deletion scheduler.
- Logged-in records: kept until deletion. Backups/log retention need explicit verification.
- Draft/PDF/WhatsApp: user-initiated export may leave app control; tell users before sharing.
- Hosting: user logs show US function region iad1; do not claim India-only data residency. Database/provider locations and subprocessors need checking.

Before a real-data pilot: clear purpose/field/provider notice; authorised upload; data minimisation; source retention off by default where feasible; documented retention/withdrawal/deletion covering backups; auth/ownership tests; rate limits; secrets handling; no invoice content in telemetry; incident response/contact; subprocessor and cross-border review; language accessibility; independent security and domain review. These are recommended release gates, not all implemented controls.

DPDP: final rules notified in November 2025 have phased commencement (immediate, one year, eighteen months). As of this research date do not claim all provisions are already effective or that the app is DPDP compliant. Applicable Act provisions, existing IT/confidentiality duties and the actual launch date require qualified review. The phase-in is not permission to misuse data.

## Pitch and design brief
Story: observed problem hypothesis -> synthetic INR1,000 mismatch -> focused user -> working correction flow -> engineering -> evidence/limits -> CA pilot -> privacy -> business hypothesis -> ask. Open with “Your invoice looks fine. Your totals might disagree.” Keep humour here, never in privacy or tax conclusions.
Visual direction: ink navy, warm ivory, restrained saffron, large editorial typography, abstract invoice/ledger art, consistent margins, one argument per slide. Do not copy another company's deck or fabricate customer photos/interviews. Inspired by Sequoia's problem/solution/market/competition/business structure and YC's plain-language user journey. Separate presenter narrative and source notes from on-slide copy. Use a live screenshot only if it is genuine and redacted/synthetic; illustration is labelled illustrative.

Market context: PIB reports 1.65 crore GST taxpayers in May 2026. This is ecosystem scale, NOT our TAM, unique paying businesses or evidence of willingness to pay. Build a bottom-up reachable pilot segment before revenue projections.

## Primary sources
- Google unpaid data terms: https://ai.google.dev/gemini-api/terms
- MeitY final Rules, commencement: https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf
- Strategyzer experiments: https://www.strategyzer.com/library/roadmap-to-test-your-value-proposition
- YC pitching: https://www.ycombinator.com/blog/how-to-pitch-your-company/
- Sequoia structure: https://sequoiacap.com/article/writing-a-business-plan
- ICAI members: https://www.icai.org/post/list-of-members
- ICAI professional publicity context: https://cajournal.icai.org/article-details/listing-of-members-and-firms-ethical-issues-and-ca-connect-portal
- PIB market context: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2279318
