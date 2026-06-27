# Wire forms → your own Google Sheet (free, unlimited)

This sends every founding application, waitlist signup, and contact message straight into a Google Sheet you own — no submission limits, no third party — and emails you on each one. ~5 minutes.

---

## Step 1 — Make the sheet
1. Go to **sheets.new** (creates a blank Google Sheet). Name it **"Aerca submissions"**.

## Step 2 — Add the script
1. In that sheet: **Extensions → Apps Script**.
2. Delete whatever is in `Code.gs`, paste the script below, and **change `NOTIFY_EMAIL`** to your inbox.
3. Click **Save** (disk icon).

> ⚠️ **Paste only the code itself — NOT the ` ```javascript ` line or the closing ` ``` `.** The first line of `Code.gs` must be `// ===== Aerca form endpoint =====`. If line 1 says `javascript`, Apps Script throws `ReferenceError: javascript is not defined` and every submission fails — delete that line and re-deploy.

```javascript
// ===== Aerca form endpoint =====
var NOTIFY_EMAIL = 'tranav50@gmail.com'; // email on every submission ('' to turn off)
var CAP = 75;                            // founding seats; overflow goes to a "Reserve" tab

function doPost(e) {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
    var ss = SpreadsheetApp.getActiveSpreadsheet();

    var raw = (e && e.parameter && e.parameter.payload) ? e.parameter.payload
            : (e && e.postData ? e.postData.contents : '{}');
    var data = JSON.parse(raw);
    data.received_at = new Date();

    // route each submission to its own tab; founding caps at CAP, overflow -> Reserve
    var name;
    if (data.type === 'contact') name = 'Contact';
    else if (data.mode === 'free') name = 'Waitlist';
    else {
      var fz = ss.getSheetByName('Founding');
      var fcount = fz ? Math.max(0, fz.getLastRow() - 1) : 0;
      if (fcount >= CAP) { name = 'Reserve'; data.status = 'reserve'; }
      else { name = 'Founding'; data.status = 'founding'; }
    }
    var sheet = ss.getSheetByName(name) || ss.insertSheet(name);

    // headers (each tab keeps its own columns)
    var lastCol = sheet.getLastColumn();
    var headers = lastCol ? sheet.getRange(1, 1, 1, lastCol).getValues()[0] : [];
    if (headers.length === 1 && headers[0] === '') headers = [];
    var changed = false;
    Object.keys(data).forEach(function (k) {
      if (headers.indexOf(k) === -1) { headers.push(k); changed = true; }
    });
    if (changed) sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

    // append the row in header order
    var row = headers.map(function (h) {
      var v = data[h];
      if (v === undefined || v === null) return '';
      if (Array.isArray(v)) return v.join(', ');
      if (typeof v === 'object') return JSON.stringify(v);
      return v;
    });
    sheet.appendRow(row);

    formatAsTable(sheet);

    if (NOTIFY_EMAIL) {
      var subject = data.type === 'contact'
        ? ('Aerca contact from ' + (data.name || ''))
        : ('Aerca ' + (data.mode || 'submission') + (data.name ? (' - ' + data.name) : ''));
      var body = Object.keys(data).map(function (k) {
        var v = data[k]; return k + ': ' + (Array.isArray(v) ? v.join(', ') : v);
      }).join('\n');
      MailApp.sendEmail(NOTIFY_EMAIL, subject, body);
    }

    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

// make each tab look like a clean table: green header, frozen, banded rows, fitted columns
function formatAsTable(sheet) {
  var lastCol = Math.max(1, sheet.getLastColumn());
  var lastRow = Math.max(1, sheet.getLastRow());
  sheet.setFrozenRows(1);
  sheet.getRange(1, 1, 1, lastCol)
       .setFontWeight('bold').setFontColor('#ffffff')
       .setBackground('#0B5C3B').setVerticalAlignment('middle');
  sheet.setRowHeight(1, 30);
  sheet.getBandings().forEach(function (b) { b.remove(); });
  if (lastRow >= 2) {
    sheet.getRange(2, 1, lastRow - 1, lastCol)
         .applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY, false, false);
  }
  sheet.autoResizeColumns(1, lastCol);
}

function doGet(e) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var f = ss.getSheetByName('Founding');
  var count = f ? Math.max(0, f.getLastRow() - 1) : 0;
  var out = JSON.stringify({ foundingCount: count, cap: CAP, full: count >= CAP });
  if (e && e.parameter && e.parameter.callback) {
    return ContentService.createTextOutput(e.parameter.callback + '(' + out + ')')
      .setMimeType(ContentService.MimeType.JAVASCRIPT);
  }
  return ContentService.createTextOutput(out).setMimeType(ContentService.MimeType.JSON);
}
```

## Step 3 — Deploy it as a Web App
1. Top-right: **Deploy → New deployment**.
2. Click the gear ⚙ next to "Select type" → **Web app**.
3. Set:
   - **Description:** Aerca
   - **Execute as:** **Me**
   - **Who has access:** **Anyone**  ← important (the public site must be able to post)
4. **Deploy** → it asks you to **Authorize access** → pick your Google account → if it warns "Google hasn't verified this app", click **Advanced → Go to (project) → Allow**. (It's your own script, this is normal.)
5. Copy the **Web app URL** — it ends in **`/exec`**, like `https://script.google.com/macros/s/AKfy.../exec`.

## Step 4 — Put the URL in the site
1. Open `index.html`, find `const APPLY_ENDPOINT = ''` (near the bottom of the script).
2. Paste your URL: `const APPLY_ENDPOINT = 'https://script.google.com/macros/s/AKfy.../exec';`
3. Save. Done.

## Step 5 — Test
1. Open the site, run the founding application or contact form, finish it.
2. Within a few seconds a new row appears in your sheet, and you get an email. 🎉

---

## Good to know
- **First field run:** the first submission of each kind adds its columns automatically; later ones fill the same columns and add any new ones. Applications, waitlist, and contact all live in one tab, distinguishable by the `mode` / `type` columns.
- **If you edit the script later:** use **Deploy → Manage deployments → ✏️ Edit → Version: New version → Deploy** so the URL stays the same. (A brand-new deployment makes a new URL you'd have to re-paste.)
- **Email quota:** Gmail Apps Script sends up to ~100 emails/day free — far more than you'll need early. Set `NOTIFY_EMAIL = ''` to turn notifications off and rely on the sheet only.
## Nothing showing up? Work through these in order
1. **Re-paste the updated script** (the one above with the `var raw = ...` line) into Apps Script, then **Deploy → Manage deployments → ✏️ Edit → Version: New version → Deploy** (keeps the same URL). The new line lets it accept the data whichever way the browser sends it.
2. **Check access:** open your `…/exec` URL directly in a browser tab. It must show **JSON** like `{"foundingCount":0,"cap":75,"full":false}`. If it shows a Google login/permission page instead, your deployment's **Who has access** isn't **Anyone** — redeploy with that set.

> **Founding cap:** submissions now split into **Founding / Waitlist / Contact** tabs, and once **75** founding rows exist, new founding applicants automatically go to a **Reserve** tab (and the site shows them the reserve-list flow). After pasting this updated script, **Deploy → Manage deployments → Edit → New version → Deploy** to apply it.
3. **Check the run log:** Apps Script editor → left sidebar **Executions** (clock icon). Submit the form, refresh Executions:
   - A `doPost` row appears = the data reached the script. If it's red/failed, open it to see the error.
   - No row at all = the request isn't leaving the browser. This is almost always because you're testing the **local `file://` page** — see #4.
4. **Test on a real URL, not `file://`.** Browsers restrict requests from local files. The reliable test is the **deployed site** (`vercel --prod`) — or run a quick local server: in the `aerca-landing` folder run `python -m http.server 8000` and open `http://localhost:8000`. Submitting from an `http(s)` page writes to the sheet every time.
