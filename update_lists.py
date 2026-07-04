import os

index_path = r'C:\Users\TRANAV\Downloads\CASH FLOW SOFTWARE\aerca-landing\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

old_founding = """<ul class="path-perks">
          <li>The lifetime founding discount ladder above</li>
          <li>First access the day we launch</li>
          <li>A direct hand in the roadmap</li>
          <li>Your free Agency Cash-Flow Teardown</li>
        </ul>"""

new_founding = """<ul class="path-perks">
          <li>Bespoke platform integration for your workflows</li>
          <li>Priority access to the early Beta & future updates</li>
          <li>Lifetime preferred pricing discount on V1</li>
          <li>Strategic roadmap partnership (Design Partner)</li>
        </ul>"""

old_waitlist = """<ul class="path-perks" style="margin:18px 0 22px">
          <li>Early access at launch, ahead of the public</li>
          <li>An exclusive launch-day offer</li>
          <li>Your free Agency Cash-Flow Teardown</li>
        </ul>"""

new_waitlist = """<ul class="path-perks" style="margin:18px 0 22px">
          <li>Early access to the V1 public launch</li>
          <li>An exclusive launch-day pricing offer</li>
          <li>Your free Agency Cash-Flow Teardown</li>
        </ul>"""

html = html.replace(old_founding, new_founding)
html = html.replace(old_waitlist, new_waitlist)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated lists.")
