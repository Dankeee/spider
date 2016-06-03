from bs4 import BeautifulSoup
import urllib
import httplib2
import requests
import Cookie
import time
import sys
from linkedincrawl.configs import LinkedInAccount
reload(sys)
sys.setdefaultencoding( "utf-8" )


# Login, the user login data will come from a database.
def linkedin_login(user, pw):

    login_get_url = "https://www.linkedin.com/uas/login"

    # Initialize cookies session here.
    session = requests.Session()

    # Get the html on the login page to grab the tokens needed to log in later.
    login_get = session.get(login_get_url, verify=False).text
    soup = BeautifulSoup(login_get, "lxml")
    csrf_param = soup.find(id="loginCsrfParam-login")['value']
    csrf_token = soup.find(id="csrfToken-login")['value']
    source_alias = soup.find(id="sourceAlias-login")['value']

    payload = {
        'isJsEnabled': 'yes',
        'source_app': '',
        'tryCount': '',
        'clickedSuggestion': 'false',
        'session_key': user,
        'session_password': pw,
        'signin': 'Sign In',
        'session_redirect': '',
        'trk': '',
        'loginCsrfParam': csrf_param,
        'fromEmail': '',
        'csrfToken': csrf_token,
        'sourceAlias': source_alias
    }

    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    raw = urllib.urlencode(payload)

    login_post_url = "https://www.linkedin.com/uas/login-submit"


    sessionCookies = session.cookies
    login_post = session.post(login_post_url, data=raw, cookies=sessionCookies, headers=headers).text
    soup = BeautifulSoup(login_post, "lxml")
    f = open("text.txt",'wb')
    f.write(login_post)
    f.close()

    return sessionCookies
