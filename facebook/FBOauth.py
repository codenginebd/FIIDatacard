FACEBOOK_BASE_URL = "https://www.facebook.com"
FACEBOOK_BASE_URL_GRAPH = "https://graph.facebook.com"
FACEBOOK_OAUTH_DIR_URL = "/dialog/oauth"
FACEBOOK_ACCESS_TOKEN_DIR_URL = "/oauth/access_token"
FACEBOOK_APP_CLIENT_ID = "519230051433986"
FACEBOOK_APP_CLIENT_SECRET = "05021b2664bb3a4197fcdcabd6e41c88"
FACEBOOK_OAUTH_REDIRECT_URI = "https://www.facebook.com/QualityLeads"
FACEBOOK_APP_ACCESS_SCOPE = "read_stream"

from Browser import *
import urllib2

class FBOauth:
    def __init__(self,browser):
        self.REQUEST_URI_AUTHORIZE = FACEBOOK_BASE_URL+FACEBOOK_OAUTH_DIR_URL+"?client_id="+FACEBOOK_APP_CLIENT_ID+"&redirect_uri="+FACEBOOK_OAUTH_REDIRECT_URI+"&scope="+FACEBOOK_APP_ACCESS_SCOPE
        self.browser = browser
#        self.browser.OpenURL("https://www.facebook.com")
#        self.browser.LoginFacebook({"email":"sohel_buet065@yahoo.com","password":"lapsso065CommlinkCommlink"})
    def GetAccessToken(self):
        self.browser.OpenURL(self.REQUEST_URI_AUTHORIZE)
        confirmButton = None
        try:
            confirmButton = self.browser.FindElementByName("__CONFIRM__")
        except Exception,msg:
            pass
        if confirmButton is not None and confirmButton != "":
            self.browser.ClickElement(confirmButton)
        else:
            pass
        pageUrl = self.browser.GetPageURL()
        code = ""
        if "code=" in pageUrl:
            code = pageUrl[pageUrl.index("code=")+5:]
        if code != "":
            self.REQUEST_URI_ACCESS_TOKEN = FACEBOOK_BASE_URL_GRAPH+FACEBOOK_ACCESS_TOKEN_DIR_URL+"?client_id="+FACEBOOK_APP_CLIENT_ID+"&client_secret="+FACEBOOK_APP_CLIENT_SECRET+"&redirect_uri="+FACEBOOK_OAUTH_REDIRECT_URI+"&code="+code
            response = urllib2.urlopen(self.REQUEST_URI_ACCESS_TOKEN)
            self.accessToken = response.read()[13:]
#            print "Access Token"+str(self.accessToken)
        return self.accessToken

#FBOauth(WebBrowser()).GetAccessToken()
