with open('Files/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<div id="main-panel-config"')
print(text[idx-300:idx])
