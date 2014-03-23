#!/usr/bin/python2.6
import os.path
import json
import urllib2
import urllib
import urlparse
import BaseHTTPServer
import webbrowser
import sys
 
APP_ID = '519230051433986'
APP_SECRET = '05021b2664bb3a4197fcdcabd6e41c88'
ENDPOINT = 'graph.facebook.com'
REDIRECT_URI = 'http://localhost:1572'
ACCESS_TOKEN = None
LOCAL_FILE = '.fb_access_token'
STATUS_TEMPLATE = u"{name}\033[0m: {message}"
 
def get_url(path, args=None):
    args = args or {}
    if ACCESS_TOKEN:
        args['access_token'] = ACCESS_TOKEN
    if 'access_token' in args or 'client_secret' in args:
        endpoint = "https://"+ENDPOINT
    else:
        endpoint = "http://"+ENDPOINT
    return endpoint+path+'?'+urllib.urlencode(args)
 
def get(path, args=None):
    return urllib2.urlopen(get_url(path, args=args)).read()
 
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
 
    def do_GET(self):
        global ACCESS_TOKEN
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
 
        code = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('code')
        code = code[0] if code else None
        if code is None:
            self.wfile.write("Sorry, authentication failed.")
            sys.exit(1)
        response = get('/oauth/access_token', {'client_id':APP_ID,
                                               'redirect_uri':REDIRECT_URI,
                                               'client_secret':APP_SECRET,
                                               'code':code})
        ACCESS_TOKEN = urlparse.parse_qs(response)['access_token'][0]
        print str(ACCESS_TOKEN)+""
        open(LOCAL_FILE,'w').write(ACCESS_TOKEN)
        self.wfile.write("You have successfully logged in to facebook. "
                         "You can close this window now.")
 
def print_status(item, color=u'\033[1;35m'):
    print color+STATUS_TEMPLATE.format(name=item['from']['name'],
                                       message=item['message'].strip())
#'graph.facebook.com//oauth/authorize?client_id=519230051433986&redirect_uri=https://www.facebook.com/QualityLeads&scope=read_stream' 
#'graph.facebook.com//oauth/access_token?client_id=519230051433986&client_secret=05021b2664bb3a4197fcdcabd6e41c88&redirect_uri=https://www.facebook.com/QualityLeads&code=AQCZXS0oqEKLC8RgnreOpoj97xoHLAhoW0rzxhqwrb8UxWh66vC1SzF0VtD5eqdLuh6dctUW8ktAF_4MQE4nFDMEWzF0jtHbSTx9vvn2v3iId_ZJ0c_wlgHHHn3vMPyUC3ISkyUp79pPTHbU6q10GxdAGwiCn7mcITawAGRCg-blcCN315m0Q41-qCrkbchuj6ysJj-h1aiDxEAtPWOTR6MS#_=_'
if __name__ == '__main__':
    if not os.path.exists(LOCAL_FILE):
        print "Logging you in to facebook..."
        webbrowser.open(get_url('/oauth/authorize',
                                {'client_id':APP_ID,
                                 'redirect_uri':REDIRECT_URI,
                                 'scope':'read_stream'}))
 
        httpd = BaseHTTPServer.HTTPServer(('127.0.0.1', 1572), RequestHandler)
        print ACCESS_TOKEN
        while ACCESS_TOKEN is None:
            httpd.handle_request()
    else:
        ACCESS_TOKEN = open(LOCAL_FILE).read()
    for item in json.loads(get('/me/feed'))['data']:
        if item['type'] == 'status':
            print_status(item)
            if 'comments' in item:
                for comment in item['comments']['data']:
                    print_status(comment, color=u'\033[1;33m')
            print '---'