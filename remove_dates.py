import os
import glob
import re

repo = r'C:\Users\TRANAV\Downloads\CASH FLOW SOFTWARE\aerca-landing'
files = glob.glob(os.path.join(repo, '*.html'))

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove any instance of the "Last updated" div
    html = re.sub(r'<div class="legal-meta">Last updated:.*?</div>', '', html)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print('Removed last updated date.')
