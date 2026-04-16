import re

path = 'Files/index.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# The config panel section we need to move
config_pattern = r'<div id="main-panel-config" style="display:none; padding:20px 0;">.*?<!-- closes main-left-col -->'

# Let's extract from <div id="main-panel-config... to the end of main-panel-config.
# Wait, the comment "<!-- closes main-left-col -->" is right AFTER main-panel-config currently!
# Oh yes! The text was injected before "</div> <!-- closes main-left-col -->" !
# BUT if "</div> <!-- closes main-left-col -->" was actually closing the page-body... wait!
# Let me just cleanly find `main-panel-config` bounds.
# `main-panel-config` starts at <div id="main-panel-config" and ends with multiple </div> before <!-- closes main-left-col --> or something.
