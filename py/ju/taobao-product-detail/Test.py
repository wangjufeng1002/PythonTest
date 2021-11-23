from requests_html import HTMLSession, AsyncHTMLSession
session = HTMLSession()

r = session.get('http://detail.tmall.com/item.htm?id=620523822174&rn=6e9c59d750b2592eef375d7c778ce71d&abbucket=11')
r.html.render()
var = r.html.search('满')['months']
print(var)