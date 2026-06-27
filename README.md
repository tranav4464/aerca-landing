# Aerca — landing page

The marketing site and founding-application flow for **Aerca**, the autonomous finance-operations system for agencies and service firms.

A static site — plain HTML/CSS/JS, no build step.

## Structure
- `index.html` — landing page + full-screen founding application / free-waitlist flow + $49 reservation
- `privacy.html`, `terms.html`, `refund.html`, `legal.css` — legal pages
- `404.html` — branded not-found page
- `og.png` — social share image (1200×630)
- `vercel.json` — static hosting config

## Run locally
```bash
python -m http.server 8000
# open http://localhost:8000
```

## Deploy
See **DEPLOY.md**. In short: `vercel --prod`, or import the folder at vercel.com.

## Forms
Submissions post to a Google Apps Script → your own Google Sheet (Founding / Waitlist / Contact tabs). Setup in **GOOGLE-SHEET-SETUP.md**.

## Go-live checklist
Paste-ins in `index.html`: the Apps Script URL (`APPLY_ENDPOINT`), GA4 Measurement ID, and your domain. Full list in **DEPLOY.md**.

---
© 2026 Aerca. Built for agencies.
