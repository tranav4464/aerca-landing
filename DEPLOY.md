# Aerca — go-live punch list

Static site: `index.html` + `privacy.html` + `terms.html` + `refund.html` + `legal.css` + `vercel.json`. No build step. Everything below is a copy-paste into `index.html` (or a one-time account setup). Items are ordered by what's blocking you.

---

## 🔴 CRITICAL — without this, nothing is captured

### 1. Form storage — fixes "forms don't store data" AND "contact gets no email"
**Both problems have the same single cause:** `const APPLY_ENDPOINT = ''` is empty. The application, the free waitlist, AND the contact form all POST to this one URL. Until it's set, submissions only print to the browser console (open DevTools → Console to see them while testing) — nothing is saved or emailed.

**Fix — Google Sheet via Apps Script (unlimited, free, your own data).** Full step-by-step + the script are in **`GOOGLE-SHEET-SETUP.md`**. In short:
1. Make a Google Sheet → **Extensions → Apps Script** → paste the script (set your notify email).
2. **Deploy → Web app → Execute as: Me → Who has access: Anyone** → authorize → copy the URL ending in `/exec`.
3. Paste it into `const APPLY_ENDPOINT = ''` in `index.html`.
4. Done. Every application, waitlist signup, **and contact message** appends to your sheet and emails you (contact rows tagged `type: contact`; applications carry every answer). No 50/month cap, no third party.

---

## 🟠 NEEDED for full functionality

### 2. Book a call — fixes "booking not available"
There's a **"Book a 15-minute call"** button. It currently shows an alert because the Calendly link is a placeholder.
- Make a free **calendly.com** event (e.g. 15-min intro), copy your link `https://calendly.com/your-handle/15min`.
- In `index.html` find `YOUR_HANDLE` and replace the whole URL with yours. Done — the button opens your real booking page.

### 3. Analytics — fixes "no visitor / conversion data"
- Create a free **GA4** property, copy the Measurement ID `G-XXXXXXXXXX`.
- Replace it in the **two** spots at the very top of `index.html`.
- You'll then see the funnel: `apply_start` → `apply_complete` → `reserve_view` → **`reserve_intent`** (your willingness-to-pay number), plus `waitlist_start`, `contact_open`, `book_call`.

---

## 🟡 BEFORE you go public

### 4. Domain
Vercel → Project → Settings → Domains → add `aerca.ai`, point DNS as shown, then update `og:url` in `index.html`.

### 5. Legal review
Privacy / Terms / Refund are solid, good-faith templates (updated to reflect: $0 taken at reservation, $49 only at launch, fully refundable). Have a lawyer skim them and set your real company entity + jurisdiction before relying on them.

### 6. Real $49 payment (only when you're ready to take money)
Today the $49 is an honest reservation — **$0 is charged**, it just records willingness to pay. When the WTP numbers justify it: make a Stripe **Payment Link** ($49, one-time) and email it to confirmed founders (or wire it into the confirm step — the spot is marked in the code). No Stripe needed before then.

### 7. (Optional) Social share image
Add `og.png` (1200×630) + `<meta property="og:image" content="/og.png" />` in `<head>` so shared links show a branded card.

---

## Deploy
```bash
npm i -g vercel
cd "aerca-landing"
vercel --prod
```
Or vercel.com → Add New → Project → drag in the `aerca-landing` folder. Policy pages serve automatically at `/privacy`, `/terms`, `/refund`.

---

## Quick status
| Thing | State | Action |
|---|---|---|
| Founding application + waitlist | ✅ built | paste `APPLY_ENDPOINT` (#1) |
| Contact form | ✅ built (no more Tally) | same `APPLY_ENDPOINT` (#1) |
| $49 reservation (WTP) | ✅ works ($0 charged) | nothing — real Stripe later (#6) |
| Book a call | ⚠️ placeholder | paste Calendly (#2) |
| Analytics | ⚠️ placeholder | paste GA4 ID (#3) |
| Legal pages | ✅ updated | lawyer review (#5) |
| Domain | ⬜ | add in Vercel (#4) |

**Do #1 first** — it switches on lead capture, contact email, and your validation data in one paste.
