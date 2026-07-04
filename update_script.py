import os

# Update index.html
index_path = r'C:\Users\TRANAV\Downloads\CASH FLOW SOFTWARE\aerca-landing\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the partial replacements first
html = html.replace('Reserve a founding seat for $49 and lock a rate no one will ever be offered again', 'Reserve a founding seat with a $79 deposit and lock a rate no one will ever be offered again')
html = html.replace('A one-time <b>$49</b> holds your seat and locks the founding rates above for life. Fully refundable, with no subscription until we launch.', 'A one-time <b>$79</b> deposit holds your seat and locks the founding rates above for life. Fully refundable for up to 3 months after V1 launch.')
html = html.replace('When we open at launch, we email you a secure link to complete the one-time $49 and lock your rate for life.', 'When our early Beta launches, we email you a secure link for the $79 deposit. This gets you into the Beta 15 days before the public V1 launch, and locks your discount for life.')

html = html.replace('$49', '$79')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

# Update privacy.html
privacy_path = r'C:\Users\TRANAV\Downloads\CASH FLOW SOFTWARE\aerca-landing\privacy.html'
with open(privacy_path, 'r', encoding='utf-8') as f:
    html2 = f.read()

html2 = html2.replace('$49', '$79 deposit')

with open(privacy_path, 'w', encoding='utf-8') as f:
    f.write(html2)

# Update refund.html
refund_path = r'C:\Users\TRANAV\Downloads\CASH FLOW SOFTWARE\aerca-landing\refund.html'
with open(refund_path, 'r', encoding='utf-8') as f:
    html3 = f.read()

html3 = html3.replace('$49', '$79')
html3 = html3.replace('Short version: your $79 founding reservation is fully refundable, any time before launch, no questions asked.', 'Short version: your $79 founding deposit is fully refundable up to 3 months after you start using V1, no questions asked.')
html3 = html3.replace('If you later complete the one-time $79 to confirm your seat (we email a secure link when reservations open around launch), that $79 is <strong>100% refundable at any time before the product launches</strong>.', 'If you later complete the $79 deposit to confirm your seat (we email a secure link when our early Beta launches), that $79 is a deposit for Beta access. It is <strong>100% refundable for up to 3 months after you start using V1</strong>. If you refund, your founding seat and lifetime discount are forfeited.')

with open(refund_path, 'w', encoding='utf-8') as f:
    f.write(html3)
print('Done updating.')
