import os

index_path = r'C:\Users\TRANAV\Downloads\CASH FLOW SOFTWARE\aerca-landing\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

old_p = 'A one-time <b>$79</b> deposit holds your seat and locks the founding rates above for life. Fully refundable for up to 3 months after official public launch.'
new_p = "Reserve your seat free today. We'll email your <b>$79</b> deposit link when the early Beta launches. This locks your lifetime discount and is fully refundable up to 3 months after the official public launch."

old_fineprint = 'Fully refundable up to 3 months after the official public launch date. No subscription until we launch in 2026.'
new_fineprint = 'No card required today. Your $79 deposit is collected when Beta access opens. Fully refundable up to 3 months after the official public launch.'

html = html.replace(old_p, new_p)
html = html.replace(old_fineprint, new_fineprint)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated text successfully.')
