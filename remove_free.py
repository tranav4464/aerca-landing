import os

index_path = r'C:\Users\TRANAV\Downloads\CASH FLOW SOFTWARE\aerca-landing\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

old_p = "Reserve your seat free today. We'll email your <b>$79</b> deposit link"
new_p = "Reserve your seat today. We'll email your <b>$79</b> deposit link"

html = html.replace(old_p, new_p)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Removed the word "free" successfully.')
