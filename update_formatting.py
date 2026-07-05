import os

index_path = r'C:\Users\TRANAV\Downloads\CASH FLOW SOFTWARE\aerca-landing\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Make header green and bold
old_h = '<div class="cta-h">Reserve your founding seat</div>'
new_h = '<div class="cta-h" style="color: var(--accent); font-weight: 800;">Reserve your founding seat</div>'
html = html.replace(old_h, new_h)

# 2. Highlight 'lifetime discount' and '3 months' in the paragraph
old_p = "Reserve your seat free today. We'll email your <b>$79</b> deposit link when the early Beta launches. This locks your lifetime discount and is fully refundable up to 3 months after the official public launch."
new_p = "Reserve your seat free today. We'll email your <b>$79</b> deposit link when the early Beta launches. This locks your <b>lifetime discount</b> and is fully refundable up to <b>3 months</b> after the official public launch."
html = html.replace(old_p, new_p)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated text formatting successfully.')
