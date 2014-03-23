import time
from klout import *

KLOUT_BASE_URL = "http://klout.com/#/"
class KLout:
    def __init__(self):
        self.parser = KLoutParser()
    def Login(self,browser,loginCredentials):
        try:
            browser.OpenURL("http://klout.com")
            browser.ClickTwitterConnectButtonInKLout()
            browser.LoginKLout(loginCredentials)
            return True
        except Exception,exp:
            return False
    def CrawlKLoutProfile(self,browserRef,user):
        browser = browserRef
        twitterUserName = user.get("twitter_user_name")
        KLOUT_PROFILE_URL = KLOUT_BASE_URL+twitterUserName
        browser.OpenURL(KLOUT_PROFILE_URL)
        kloutProfilePageSource = browser.GetPage()
        kloutProfile = self.parser.ParseKLoutProfile(kloutProfilePageSource)
        return kloutProfile