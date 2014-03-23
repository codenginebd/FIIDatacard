from Parser import *

class KLoutParser(FIIParser):
    def __init__(self):
        print "Initializing KLout Parser."
        super(FIIParser,self).__init__()
    def ParseKLoutScore(self,pageSource):
        kloutScrore = None
        try:
            kloutScoreContainerElement = super(KLoutParser,self).ParseSingle(pageSource,r"<span[\s]class=[\'\"]kscore(.+?)</span>")
            if kloutScoreContainerElement is not None:
                kloutScrore = super(KLoutParser,self).ParseAndReplace(kloutScoreContainerElement,r"<(.+?)>","")
                if kloutScrore is not None:
                    kloutScrore = kloutScrore.strip()
        except Exception,exp:
            pass
        return kloutScrore
    def ParseUserBio(self,pageSource):
        userBio = None
        try:
            userBioContainerElement = super(KLoutParser,self).ParseSingle(pageSource,r"<div[\s]class=[\'\"]user-bio(.+?)</div>")
            if userBioContainerElement is not None:
                userBio = super(KLoutParser,self).ParseAndReplace(userBioContainerElement,r"<(.+?)>","")
                if userBio is not None:
                    userBio = userBio.strip()
        except Exception,exp:
            pass
        return userBio
    def ParseSocialMediaProfileLinks(self,pageSource):
        links = None
        try:
            socialNetworksContainerElement = super(KLoutParser,self).ParseSingle(pageSource,r"<div[\s]class=[\'\"]user-networks(.+?)</ul></div>")
            if socialNetworksContainerElement is not None:
                socialMediaContainerLIs = super(KLoutParser,self).Parse(socialNetworksContainerElement,r"<li(.+?)</li>")
                if socialMediaContainerLIs is not None:
                    linksTemp = {}
                    for eachLI in socialMediaContainerLIs:
                        if eachLI is not None:
                            socialMediaLinkHref = super(KLoutParser,self).ParseSingle(eachLI,r"href=[\'\"](.+?)[\'\"]")
                            if socialMediaLinkHref is not None:
                                socialMediaLinkHref = super(KLoutParser,self).ParseAndReplace(socialMediaLinkHref,r"href=","")
                                socialMediaLinkHref = super(KLoutParser,self).ParseAndReplace(socialMediaLinkHref,r"[\'\"]","")
                                if socialMediaLinkHref is not None:
                                    socialMediaLinkHref = socialMediaLinkHref.strip()
                                if "twitter" in socialMediaLinkHref:
                                    linksTemp["twitter"] = socialMediaLinkHref
                                elif "facebook" in socialMediaLinkHref:
                                    linksTemp["facebook"] = socialMediaLinkHref
                                elif "plus" in socialMediaLinkHref:
                                    linksTemp["google_plus"] = socialMediaLinkHref
                                elif "linkedin" in socialMediaLinkHref:
                                    linksTemp["linkedin"] = socialMediaLinkHref
                                elif "foursquare" in socialMediaLinkHref:
                                    linksTemp["four_square"] = socialMediaLinkHref
                                elif "youtube" in socialMediaLinkHref:
                                    linksTemp["youtube"] = socialMediaLinkHref
                                elif "instagram" in socialMediaLinkHref:
                                    linksTemp["instagram"] = socialMediaLinkHref
                    if len(linksTemp) > 0:
                        links = linksTemp
        except Exception,exp:
            pass
        return links
    def ParseKLoutProfile(self,pageSource):
        kloutProfile = {}
        kloutScore = self.ParseKLoutScore(pageSource)
        userBio = self.ParseUserBio(pageSource)
        socialNetworks = self.ParseSocialMediaProfileLinks(pageSource)
        if kloutScore is not None:
            kloutProfile["score"] = kloutScore
        if userBio is not None:
            kloutProfile["user_bio"] = userBio
        if socialNetworks is not None:
            kloutProfile["social_media_profiles"] = socialNetworks
        return kloutProfile