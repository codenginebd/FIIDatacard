from linkedin import *

###https://www.linkedin.com/profile/view?id=36379560&authType=NAME_SEARCH&authToken=Xu6Q&trk=api*a231405*s2393+07*
###https://www.linkedin.com/profile?viewProfile=&key=36379560&authToken=Xu6Q&authType=NAME_SEARCH&trk=api*a231405*s239307*
###Andrews Profile: https://www.linkedin.com/profile/view?id=12285308&authType=NAME_SEARCH&authToken=Xu6Q&trk=api*a231405*s2393+07*
### Another profile ID: 453613
class LinkedIn:
    def __init__(self):
        print "Initializing LinkedIn..."
        self.parser = LinkedInParser()
        
    def Authorize(self,browserInstance,linkedInCredentials):
        print "Authorizing LinkedIn..."
        try:
            self.oauthLI = LIOauth("uugjyzgm6537","vJvp4cEipe7fcuHq") 
            self.oauthLI.Authorize(browserInstance,linkedInCredentials)
            return True
        except Exception,exp:
            return False
        
    def SearchByFirstAndLastName(self,firstName,lastName,start,count):
        response = self.oauthLI.Call("http://api.linkedin.com/v1/people-search:(people:(id,first-name,last-name,site-standard-profile-request))?first-name="+firstName+"&last-name="+lastName+"&format=json&start="+str(start)+"&count="+str(count))
        print "Response: "
        print response
        total = self.parser.CountTotalResultsSearch(response)
        _start = self.parser.ParseStart(response)
        profiles = self.parser.ParseProfileLinks(response)
        return {"start":_start,"total":total,"data":profiles}
        
    def CrawlProfile(self,browserInstance,profileLink):
        #response = self.SearchByFirstAndLastName("michelle","margolis",1,2)
        print "LinkedIn Crawling starting..."
#        profileLinks = response.get("data")
        browser = browserInstance
#        browser.OpenURL("https://www.linkedin.com/")
#        loginCredentials ={}
#        loginCredentials["email"] = "codenginebd@gmail.com"
#        loginCredentials["password"] = "lapsso065lapsso065"
#        browser.LoginLinkedIn(loginCredentials)
        #profileLinks[0] = profileLinks[0].replace("http:","https:")
        compatibleURL = self.parser.ConvertURL(profileLink)
#        print compatibleURL
        
#        compatibleURL = "https://www.linkedin.com/profile/view?id=12285308&authType=NAME_SEARCH&authToken=Xu6Q&trk=api*a231405*s2393+07*"
        
        browser.OpenURL(compatibleURL)
        pageSource = browser.GetPage()
        #f = open("linkedinpage.html","w")
        #f.write(pageSource)
        #f.close()
        profile = self.parser.ParseUserProfile(pageSource)
        return profile