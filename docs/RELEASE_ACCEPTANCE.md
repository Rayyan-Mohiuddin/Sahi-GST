# Release acceptance record — 10 October 2026

Deadline: 11 October 09:00 IST; submit by 07:00. Do not claim a fully tested release until the pending device checks below have evidence.

## Verified in this release
- 32 Django tests pass using SQLite: authentication, ownership, images/pages, PDF, rules, mock AI and no-key API flow.
- 11 frontend tests pass; production export and TypeScript pass.
- Live session endpoint reports PostgreSQL and cloud_extraction=true. User confirms environment configuration/redeployment. This is not proof of successful Gemini inference.
- Login template now overrides current Allauth layout. Responsive account styles, focus states and checkbox sizing are included.
- UI polish covers shared cards, navigation, typography, touch targets and mobile input sizing. Browser access to local preview was denied by security policy; visual QA pending.

## Phone test: repeat on two real devices
Record device/OS/browser, deployment commit, date, network, result and observed error for each step. Turn Wi-Fi OFF and confirm mobile data works. Use synthetic/redacted invoices.

| Step | Expected | Phone A | Phone B |
|---|---|---|---|
| Login/signup/logout | Styled, usable form; correct session | Pending | Pending |
| Camera allow/deny/close | Live preview; capture; useful denied message; camera stops | Pending | Pending |
| Choose files | Files chooser separate from camera | Pending | Pending |
| Add 2–5 pages of ONE invoice | Correct order and previews; remove works; total under 3 MB | Pending | Pending |
| Gemini extraction with consent | Fields + honest uncertainty; compare every GSTIN character | Pending | Pending |
| Confirm/edit/check | Edit resets confirmation; planted discrepancy caught | Pending | Pending |
| Hindi/Telugu | Text appears; fluent speaker checks meaning | Pending | Pending |
| Read aloud both languages | Audible correct language OR honest missing-local-voice message | Pending | Pending |
| WhatsApp draft | Correct draft; recipient chooser; user chooses whether to send | Pending | Pending |
| PDF download | Opens, readable fields/findings, no clipping | Pending | Pending |
| Finish/recent invoices/Back | Close review; saved pages reopen; Back closes review before exiting | Pending | Pending |
| Sidebar at 100% zoom | All actions reachable without zooming out | Pending | Pending |

## No-key fallback
Use a preview/test deployment, not the only live demo: remove GEMINI_API_KEY there and redeploy, leaving production unchanged. Confirm session cloud_extraction=false. Upload a redacted invoice, explicitly choose local OCR, compare/edit fields, confirm, save, switch languages and download PDF. Record actual image OCR output. The automated test covers the downstream API flow from OCR text, not camera/network/recognition on a phone. Restore preview settings afterward if desired. Local OCR needs model assets on its first run; this is not a fully offline app.

## Friend's accuracy test set — awaiting input
No cases or expected planted errors were supplied. Do not invent results or call previous synthetic fixtures the friend's set.

For each case record: case ID, expected printed fields, planted errors, extracted fields before edits, detected rule IDs, missed errors and false alarms. Score extraction before correction separately from rule detection after confirmation.

- Detection recall = caught planted errors / all planted errors.
- Precision = correct issue flags / all issue flags; report N/A if none.
- False-positive rate = incorrect issue flags / evaluated negative opportunities; define those opportunities first.
- Also publish raw counts, sample size and unsupported cases. Unknown/review warnings are separate from incorrect confirmed-error flags.

## Submission gate
Merge codex/auth-release-checks into shared main and verify deployment. Complete phone evidence, real Gemini scan and friend fixtures. Record contributions. Rehearse the two-minute demo, finish slides/video, generate source ZIP <=10 MB, upload with view access and submit before 07:00 IST. No approved interview quote exists; keep it pending.
