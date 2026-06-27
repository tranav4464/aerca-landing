# Aerca — go-live setup

The two flows (Founding Application + Free Waitlist) are now **built into the page** — full-screen, custom, on the Aerca brand. You don't build them anywhere else. You only need to (1) point them at a place to store answers, and (2) paste a few keys.

---

## How the flows work (already built)

- **"Become a founding member"** → opens the **15-step Founding Application** (full-screen, progress bar, one question per screen, "Other → tell us" on every choice) → ends in the **"Secure your place"** 4-step reservation ($0 today, honest WTP capture, fires `reserve_intent`).
- **"Join the free waitlist"** → opens the **6-step light waitlist** (type, team, revenue, pain, leakage, email) → "You're on the list."
- Every submission POSTs to **Formspree** (Step 1). The email is captured before the reservation, so you keep the lead even if someone doesn't finish.

---

## STEP 1 — Connect Formspree (where answers land)  ·  ~3 min

1. Go to **formspree.io** → sign up (free) → **+ New form** → name it "Aerca applications". Copy its endpoint, e.g. `https://formspree.io/f/abcdwxyz`.
2. Open `index.html`, find **`const APPLY_ENDPOINT = ''`** (near the bottom) and paste the endpoint between the quotes.
3. Done. Every Founding Application **and** Free Waitlist submission now lands in your Formspree dashboard (with all answers + UTM), and Formspree emails you on each one.

**Export to Excel/Sheets:** Formspree → your form → **Submissions → Export CSV** (open in Excel). Free plan keeps your latest submissions; paid plans add a live Google Sheets sync if you want it automatic.

> Want submissions to flow straight into a Google Sheet for free instead? Say the word and I'll swap `APPLY_ENDPOINT` for a Google Apps Script web app that writes to your own sheet.

---

## STEP 2 — Contact form (footer)  ·  ~5 min

Still on **Tally** (separate, tiny): create a Tally form (Name, Email, Message), set its **Notifications** email to **tranav50@gmail.com**, and replace **`CONTACT_TALLY_ID`** in `index.html`. Your address never appears in the page source.

---

## STEP 3 — Analytics, calls, deploy

- **GA4:** create a property, paste the Measurement ID over `G-XXXXXXXXXX` (two spots, top of file). This powers the funnel below — set it up first.
- **Calendly:** replace `YOUR_HANDLE` in the book-a-call script.
- **Deploy:**
  ```bash
  npm i -g vercel
  cd "aerca-landing"
  vercel --prod
  ```
- **Domain:** Vercel → Settings → Domains → add `aerca.ai`, then update `og:url` in `index.html`.
- **Legal:** have a lawyer skim Privacy/Terms/Refund before relying on them.

---

## The funnel you'll see in GA4
- `apply_start` / `waitlist_start` — opened a flow
- `apply_complete` / `generate_lead` — finished the questions (lead captured)
- `reserve_view` → `reserve_intent` — reached the reservation → **clicked Confirm (your willingness-to-pay number)**

**`reserve_intent` ÷ visitors = your validation metric.** And remember: the open-text answers (what they'd do with recovered cash, what's held them back, why now) are customer-discovery gold — email every founding applicant personally.
