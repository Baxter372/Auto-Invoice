try:
    from bs4 import BeautifulSoup
    with open('Files/index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    cfg = soup.find(id='main-panel-config')
    if cfg:
        parent = cfg.parent
        if parent.has_attr('id'):
            print("Parent ID:", parent['id'])
        else:
            print("Parent classes:", parent.get('class'))
            print("Parent style:", parent.get('style'))
            grandparent = parent.parent
            if grandparent and grandparent.has_attr('id'):
                print("Grandparent ID:", grandparent['id'])
            
except Exception as e:
    print(e)
