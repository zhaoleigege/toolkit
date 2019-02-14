# -*- coding: UTF-8 -*-
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

req = Request('https://git-scm.com/book/zh/v2', headers={'User-Agent': 'Mozilla/5.0'})
bs = BeautifulSoup(urlopen(req).read(), 'html.parser')

content = str(bs.find(id='content'))

bs.find(id='documentation').clear()
bs.find(id='content').decompose()
bs.footer.decompose()

bs.body.append(BeautifulSoup(content, 'html.parser'))

f = open('./1.html', 'w')
f.write(str(bs))
f.close()