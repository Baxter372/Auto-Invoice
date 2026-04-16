with open('Files/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

config_idx = text.find('id="main-panel-config"')
before_text = text[:config_idx]

div_opens = before_text.count('<div')
div_closes = before_text.count('</div')

print('Opens:', div_opens)
print('Closes:', div_closes)
print('Unclosed divs at config_idx:', div_opens - div_closes)
