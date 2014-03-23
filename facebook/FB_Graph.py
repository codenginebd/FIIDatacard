class FBGraph:
	def __init__(self):
		print "Initializing Graph..."
	
	def GetProfileLinkById(self,browser,parser,profileId):
		facebookGraphAPIProfileLinkSearchUrl = "https://graph.facebook.com/"+str(profileId)+"?fields=link"
		browser.OpenURL(facebookGraphAPIProfileLinkSearchUrl)
		page = browser.GetPage()
		searchResult = parser.ParseSearchResponse(page)
		return searchResult
		
	def SearchUserByEmail(self,browser,parser,email,accessToken):
		facebookGraphAPISearchUrl = "https://graph.facebook.com/search?fields=id,name,gender,link,username&q=%s&type=user&access_token=%s" % (email,accessToken)
		browser.OpenURL(facebookGraphAPISearchUrl)
		searchResult = browser.GetPage()
		searchResult = parser.ParseSearchResponse(searchResult)
		#searchResult = self.GetProfileLinkById(searchResult)
		return searchResult
	def SearchUsersAndGetProfileLinks(self,browser,parser,utility,accessTokenUser,user):
		profileInfo = None
		try:
			searchJSONResponse = self.SearchUserByEmail(browser,parser,user.get("email"),accessTokenUser)
			#print searchJSONResponse
			jsonResponse = None
			try:
				jsonResponse = utility.JSONEncode(searchJSONResponse)
			except Exception,e:
				jsonResponse = None
			
	#		print jsonResponse
			
			if jsonResponse is not None and jsonResponse.get("error") is not None:
				error = jsonResponse.get("error")
				errorType = error.get("type")
				if errorType == "OAuthException":
					return "SEARCH_FAILED_WITH_OAUTH_EXCEPTION"
			
			jsonArray = []
			if jsonResponse is not None and jsonResponse.get("data") is not None:
				jsonArray = jsonResponse["data"]
			
			if len(jsonArray) > 0: #Check if user exists by this email
				try:
					jsonDict = jsonArray[0]
					userId = jsonDict["id"]
					userName = None
					profileLinkPrototype = None
					profileType = None
					if jsonDict.get("username"):
						userName = jsonDict["username"]
					if userName is None:
						profileType = "OLD"
					else:
						profileType = "TIME_LINE"
					if profileType == "OLD":
						profileLinkPrototype = "https://www.facebook.com/profile.php?id="+userId+"&sk="
					else:
						profileLinkPrototype = "https://www.facebook.com/"+userName+"/"
					if profileLinkPrototype is not None:
						emailAddress = user.get("email")
						profileLink = profileLinkPrototype
						eachUsersEmailAndLink = {
							"email":emailAddress,
							"link":profileLink
						}
						profileInfo = eachUsersEmailAndLink
				except Exception,e:
					print "Inside FB Profile Search"+str(e)
					pass
		except Exception,exp:
			profileInfo = None
		return profileInfo