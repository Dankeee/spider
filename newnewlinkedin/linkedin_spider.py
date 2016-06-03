
import requests
import urllib
import urllib2
from bs4 import BeautifulSoup

s = requests.session()
r = s.get('https://www.linkedin.com/uas/login?goback=&trk=hb_signin')
soup = BeautifulSoup(r.text, 'lxml')
loginCsrfParam = soup.find('input', id = 'loginCsrfParam-login')['value']
csrfToken = soup.find('input', id = 'csrfToken-login')['value']
sourceAlias = soup.find('input', id = 'sourceAlias-login')['value']

headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Referer': 'http://www.zhihu.com/articles'}
payload = {
            'session_key': '877371395@qq.com',
            'session_password': 'kk20080504',
            'loginCsrfParam' : loginCsrfParam,
            'csrfToken' : csrfToken,
            'sourceAlias' : sourceAlias}


data = s.post('https://www.linkedin.com/uas/login-submit', data=payload)
print(data.text)