from googleplus import *
from libraries import *
from facebook import *

class FIIGooglePlus:
    def __init__(self,browser):
        self.browser = browser
        self.plus = GooglePlus()
        print "Starting Google Plus"
    def Authenticate(self,loginCredentials):
        try:
            self.browser.OpenURL("https://accounts.google.com/ServiceLogin?hl=en&continue=https://www.google.com/")
            self.browser.LoginGoogle(loginCredentials)
            return True
        except Exception,exp:
            return False
    def SearchPeople(self,basicInfo):
        searchResults = self.plus.Search(basicInfo)
        return searchResults
    def CrawlProfile(self,plusProfileBasic):
        profileId = plusProfileBasic.get("id")
        link = plusProfileBasic.get("link")
        aboutLink = link+"/about"
        self.browser.OpenURL(aboutLink)
        pageSource = self.browser.GetPage()
        gPlusParser = GPlusParser(pageSource)
        return gPlusParser.ParseProfile()
        
#basicProfile = {}
#basicProfile["id"] = "100206344210127994323"
#basicProfile["link"] = "https://plus.google.com/u/0/100206344210127994323"
##browser = WebBrowser()
#plus = FIIGooglePlus(None)
##plus.Authenticate({"email":"codenginebd@gmail.com","password":"lapsso065Commlink"})
#for each in plus.SearchPeople({"full_name":"Md Shariful Islam Sohel"}):
#    print each
#    break