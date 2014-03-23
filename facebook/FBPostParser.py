import simplejson as json
from bs4 import BeautifulSoup

class FBPostParser:
	def __init__(self,pageSource):
		self.page = pageSource
		self.soup = BeautifulSoup(self.page)
	def Parse(self):
		posts = []
		timeLineUnitListLIs = self.soup.findAll("div",{"class":"timelineUnitContainer"})
		for eachTimeLineUnitLI in timeLineUnitListLIs:
			userContentSpanElement = eachTimeLineUnitLI.find("span",{"class":"userContent"})
			postText = ""
			if userContentSpanElement is not None:
				postText = userContentSpanElement.text
			postLikesCount,postCommentsCount,postShareCount="","",""
			if postText != "":
				postFeedbackActionsList = eachTimeLineUnitLI.findAll("span",{"class":"UFIBlingBoxText"})
				if len(postFeedbackActionsList) > 0:
					postLikesCount = postFeedbackActionsList[0].text if postFeedbackActionsList[0] is not None else ""
				if len(postFeedbackActionsList) > 1:
					postCommentsCount = postFeedbackActionsList[1].text if postFeedbackActionsList[1] is not None else ""
				if len(postFeedbackActionsList) > 2:
					postShareCount = postFeedbackActionsList[2].text if postFeedbackActionsList[2] is not None else ""
				if postLikesCount == "":
					postLikesCount = "0"
				if postCommentsCount == "":
					postCommentsCount = "0"
				if postShareCount == "":
					postShareCount = "0"
				posts.append({"post_message":postText,"likes":{"count":postLikesCount},"comments":{"count":postCommentsCount},"shares":{"count":postShareCount}})
		return posts