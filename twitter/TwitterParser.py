import re
from Parser import *
import simplejson as json

class TwitterParser(FIIParser):
    def __init__(self):
        print "Initializing twitter parser."
        super(FIIParser,self).__init__()
    def ParseFullName(self,pageSource):
        fullName = None
        try:
            fullNameElement = super(TwitterParser,self).ParseSingle(pageSource,r"<h1[\s]class=[\'\"]fullname(.+?)</h1>")
            if fullNameElement is not None:
                fullName = super(TwitterParser,self).ParseAndReplace(fullNameElement,r"<(.+?)>","") 
                if fullName is not None:
                    fullName = fullName.strip()
        except Exception,exp:
            pass
        return fullName
    def ParseTwitterScreenName(self,pageSource):
        screenName = None
        try:
            screenNameElement = super(TwitterParser,self).ParseSingle(pageSource,r"<span[\s]class=[\'\"]screen-name(.+?)</span>")
            if screenNameElement is not None:
                screenName = super(TwitterParser,self).ParseAndReplace(screenNameElement,r"<(.+?)>","")
                if screenName is not None:
                    screenName = screenName.strip()
        except Exception,exp:
            pass
        return screenName
    def ParseAboutBioFromCover(self,pageSource):
        bio = None
        try:
            bioElement = super(TwitterParser,self).ParseSingle(pageSource,r"<p[\s]class=[\'\"]bio(.+?)</p>")
            if bioElement is not None:
                bio = super(TwitterParser,self).ParseAndReplace(bioElement,r"<(.+?)>","")
                if bio is not None:
                    bio = bio.strip()
        except Exception,exp:
            pass
        return bio
    
    def ParseLocation(self,pageSource):
        location = None
        try:
            locationElement = super(TwitterParser,self).ParseSingle(pageSource,r"<span[\s]class=[\'\"]location(.+?)</span>")
            if locationElement is not None:
                location = super(TwitterParser,self).ParseAndReplace(locationElement,r"<(.+?)>","")
                if location is not None:
                    location = location.strip() 
        except Exception,exp:
            pass
        return location
    
    def ParseFollowActivitiesCount(self,pageSource):
        followActivity = {}
        try:
            followActivityListContainerUL = super(TwitterParser,self).ParseSingle(pageSource,r"<ul[\s]class=[\'\"]stats(.+?)</ul>") 
            if followActivityListContainerUL is not None:
                followActivityListLIs = super(TwitterParser,self).Parse(followActivityListContainerUL,r"<li(.+?)</li>") 
                for eachLI in followActivityListLIs:
                    if eachLI is not None:
                        title = super(TwitterParser,self).ParseAndReplace(eachLI,r"<(.+?)>","")
                        numberCount = super(TwitterParser,self).ParseSingle(eachLI,r"<strong(.+?)</strong>")
                        followActivityCount = None 
                        if numberCount is not None:
                            followActivityCount = super(TwitterParser,self).ParseAndReplace(numberCount,r"<(.+?)>","")
                        if title is not None and followActivityCount is not None:
                            followActivityCount = followActivityCount.strip()
                            if "Tweets" in title:
                                followActivity["tweets_count"] = followActivityCount
                            elif "Following" in title:
                                followActivity["following_count"] = followActivityCount
                            elif "Followers" in title:
                                followActivity["followers_count"] = followActivityCount  
        except Exception,exp:
            pass
        return followActivity
    
    def ParseTweetHeader(self,tweet):
        header = None
        try:
            tweetHeaderContainerElement = super(TwitterParser,self).ParseSingle(tweet,r"<div[\s]class=[\'\"]stream-item-header(.+?)</a>")
            if tweetHeaderContainerElement is not None:
                tweetedByFullNameElement = super(TwitterParser,self).ParseSingle(tweetHeaderContainerElement,r"<strong[\s]class=[\'\"]fullname(.+?)</strong>")
                tweetedByFullName,tweetedByUserName,tweetedByAvaterImgSrc = None,None,None
                if tweetedByFullNameElement is not None:
                    tweetedByFullName = super(TwitterParser,self).ParseAndReplace(tweetedByFullNameElement,r"<(.+?)>","")  
                tweetedByUserNameElement = super(TwitterParser,self).ParseSingle(tweetHeaderContainerElement,r"<span[\s]class=[\'\"]username(.+?)</span>") 
                if tweetedByUserNameElement is not None:
                    tweetedByUserName = super(TwitterParser,self).ParseAndReplace(tweetedByUserNameElement,r"<(.+?)>","")
                tweetedByAvaterImgElement = super(TwitterParser,self).ParseSingle(tweetHeaderContainerElement,r"<img(.+?)>") 
                if tweetedByAvaterImgElement is not None:
                    tweetedByAvaterImgSrcAttr = super(TwitterParser,self).ParseSingle(tweetedByAvaterImgElement,r"src=[\'\"](.+?)[\'\"]")
                    if tweetedByAvaterImgSrcAttr is not None:
                        tweetedByAvaterImgSrc = super(TwitterParser,self).ParseAndReplace(tweetedByAvaterImgSrcAttr,r"src=","")
                        tweetedByAvaterImgSrc = super(TwitterParser,self).ParseAndReplace(tweetedByAvaterImgSrc,r"[\'\"]","")
                headerTemp = {}
                if tweetedByFullName is not None:
                    tweetedByFullName = tweetedByFullName.strip()
                    headerTemp["full_name"] = tweetedByFullName
                if tweetedByUserName is not None:
                    tweetedByUserName = tweetedByUserName.strip()
                    headerTemp["user_name"] = tweetedByUserName
                if tweetedByAvaterImgSrc is not None:
                    tweetedByAvaterImgSrc = tweetedByAvaterImgSrc.strip()
                    headerTemp["avater"] = tweetedByAvaterImgSrc
                if len(headerTemp) > 0:
                    header = headerTemp
        except Exception,exp:
            pass
        return header
    
    def ParseTweetText(self,pageSource):
        tweetText = None
        try:
            tweetTextElement = super(TwitterParser,self).ParseSingle(pageSource,r"<p[\s]class=[\'\"]js-tweet-text(.+?)</p>")
            if tweetTextElement is not None:
                tweetText = super(TwitterParser,self).ParseAndReplace(tweetTextElement,r"<(.+?)>","")
                if tweetText is not None:
                    tweetText = tweetText.strip()
        except Exception,exp:
            pass
        return tweetText
    
    def ParseTweets(self,pageSource,max = 10):
        tweets = []
        try:
            tweetsListContainerElementOL = super(TwitterParser,self).ParseSingle(pageSource,r"<ol[\s]class=[\'\"]stream-items(.+?)</ol>")
            if tweetsListContainerElementOL is not None:
                tweetsContainerListLIs = super(TwitterParser,self).Parse(tweetsListContainerElementOL,r"<li(.+?)</li>")
                if tweetsContainerListLIs is not None:
                    for eachLI in tweetsContainerListLIs:
                        if eachLI is not None:
                            header = self.ParseTweetHeader(eachLI)
                            tweet = self.ParseTweetText(eachLI)
                            if header is not None and tweet is not None:
                                tweets.append({"tweeted_by":header,"tweet":tweet})
        except Exception,exp:
            pass
        if len(tweets) > max:
            tempTweets = []
            counter = 0
            for eachTweet in tweets:
                tempTweets.append(eachTweet)
                counter += 1
                if counter >= max:
                    break
            tweets = tempTweets
        return tweets
    
    def ParseFavorites(self,pageSource,max=10):
        return self.ParseTweets(pageSource, max)
    
    def ParseGroupHeader(self,listSource):
        header = None
        try:
            headerContainerElement = super(TwitterParser,self).ParseSingle(listSource,r"<div[\s]class=[\'\"]stream-item-header(.+?)</div>")
            if headerContainerElement is not None:
                groupLink,groupName,groupCreatorProfileLink,groupCreatorName = None,None,None,None
                groupLinkAnchorElement = super(TwitterParser,self).ParseSingle(headerContainerElement,r"<a[\s]class=[\'\"]js-list-link(.+?)</a>")
                if groupLinkAnchorElement is not None:
                    groupLinkHref = super(TwitterParser,self).ParseSingle(groupLinkAnchorElement,r"href=[\'\"](.+?)[\'\"]")
                    if groupLinkHref is not None:
                        groupLink = super(TwitterParser,self).ParseAndReplace(groupLinkHref,r"href=","")
                        groupLink = super(TwitterParser,self).ParseAndReplace(groupLink,r"[\'\"]","")
                    groupNameElement = super(TwitterParser,self).ParseSingle(groupLinkAnchorElement,r"<strong(.+?)</strong>")
                    if groupNameElement is not None:
                        groupName = super(TwitterParser,self).ParseAndReplace(groupNameElement,r"<(.+?)>","")
                groupCreatorContainerElement = super(TwitterParser,self).ParseSingle(headerContainerElement,r"<span[\s]class=[\'\"]username(.+?)</span>")
                if groupCreatorContainerElement is not None:
                    groupCreatorContainerAnchor = super(TwitterParser,self).ParseSingle(groupCreatorContainerElement,r"<a(.+?)</a>")
                    if groupCreatorContainerAnchor is not None:
                        groupCreatorProfileLinkHref = super(TwitterParser,self).ParseSingle(groupCreatorContainerAnchor,r"href=[\'\"](.+?)[\'\"]")
                        if groupCreatorProfileLinkHref is not None:
                            groupCreatorProfileLink = super(TwitterParser,self).ParseAndReplace(groupCreatorProfileLinkHref,r"href=","")
                            groupCreatorProfileLink = super(TwitterParser,self).ParseAndReplace(groupCreatorProfileLink,r"[\'\"]","")
                        groupCreatorName = super(TwitterParser,self).ParseAndReplace(groupCreatorContainerAnchor,r"<(.+?)>","")
                headerTemp = {}
                if groupLink is not None:
                    groupLink = groupLink.strip()
                    headerTemp["link"] = groupLink
                if groupName is not None:
                    groupName = groupName.strip()
                    headerTemp["title"] = groupName
                groupCreator = {}
                if groupCreatorProfileLink is not None:
                    groupCreatorProfileLink = groupCreatorProfileLink.strip()
                    groupCreator["profile_link"] = groupCreatorProfileLink
                if groupCreatorName is not None:
                    groupCreatorName = groupCreatorName.strip()
                    groupCreator["title"] = groupCreatorName
                if len(groupCreator) > 0:
                    headerTemp["creator"] = groupCreator
                if len(headerTemp) > 0:
                    header = headerTemp
        except Exception,exp:
            pass
        return header
    
    def ParseGroupBio(self,listSource):
        groupBio = None
        try:
            groupBioContainerElement = super(TwitterParser,self).ParseSingle(listSource,r"<p[\s]class=[\'\"]bio(.+?)</p>")
            if groupBioContainerElement is not None:
                groupBio = super(TwitterParser,self).ParseAndReplace(groupBioContainerElement,r"<(.+?)>","")
                if groupBio is not None:
                    groupBio = groupBio.strip()
        except Exception,exp:
            pass
        return groupBio
    
    def ParseLists(self,pageSource,max=10):
        lists = []
        try:
            listsContainerElementOL = super(TwitterParser,self).ParseSingle(pageSource,r"<ol[\s]class=[\'\"]stream-items(.+?)</ol>")
            if listsContainerElementOL is not None:
                listLIs = super(TwitterParser,self).Parse(listsContainerElementOL,r"<li(.+?)</li>")
                for eachLI in listLIs:
                    if eachLI is not None:
                        groupHeader = self.ParseGroupHeader(eachLI)
                        groupBio = self.ParseGroupBio(eachLI)
                        lists.append({"group_and_creator_info":groupHeader,"bio":groupBio})
        except Exception,exp:
            pass
        return lists
    
    def ParsePersonalBlog(self,pageSource):
        blog = {}
        try:
            blogElement = super(TwitterParser,self).ParseSingle(pageSource,r"<span[\s]class=[\'\"]url(.+?)</span>")
            if blogElement is not None:
                blogAnchorElement = super(TwitterParser,self).ParseSingle(blogElement,r"<a(.+?)</a>")
                if blogAnchorElement is not None:
                    blogLinkHrefElement = super(TwitterParser,self).ParseSingle(blogAnchorElement,r"href=[\'\"](.+?)[\'\"]")
                    blogLink,blogScreenName = None,None
                    if blogLinkHrefElement is not None and blogLinkHrefElement != "":
                        blogLink = super(TwitterParser,self).ParseAndReplace(blogLinkHrefElement,r"href=","")
                        if blogLink is not None and blogLink != "":
                            blogLink = super(TwitterParser,self).ParseAndReplace(blogLink,r"[\'\"]","")
                    blogScreenName = super(TwitterParser,self).ParseAndReplace(blogAnchorElement,r"<(.+?)>","")
                    if blogLink is not None and blogLink != "":
                        blogLink = blogLink.strip()
                        blog["link"] = blogLink
                    if blogScreenName is not None and blogScreenName != "":
                        blogScreenName = blogScreenName.strip()
                        blog["title"] = blogScreenName
        except Exception,exp:
            pass
        return blo