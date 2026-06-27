// ===== Aerca form backend (Google Apps Script, bound to the submissions Sheet) =====
//
// Setup once:
//   1. In the Google Sheet: Extensions > Apps Script. Paste this whole file into Code.gs.
//   2. Set NOTIFY_EMAIL below.
//   3. Deploy > New deployment > Web app > Execute as: Me, Who has access: Anyone > Deploy.
//   4. Copy the /exec URL and paste it into APPLY_ENDPOINT near the bottom of index.html.
//   After any edit: Deploy > Manage deployments > Edit (pencil) > Version: New version > Deploy
//   (this keeps the same /exec URL).
//
// Behaviour: submissions split into Founding / Waitlist / Contact tabs. Founding caps at CAP (75);
// once full, new founding applicants go to a Reserve tab. doGet reports the live count to the site.

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

// returns the live founding count (JSONP if ?callback= is passed) for the site's cap check
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
