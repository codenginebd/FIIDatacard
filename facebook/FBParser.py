from facebook import *
class FII_FBParser(FIIParser):
	def __init__(self):
		super(FIIParser,self).__init__()
	def ParseTitle(self,infoSource):
		headerTitle = ""
		try:
			headerTitleHtml = super(FII_FBParser,self).ParseSingle(infoSource,r"<h4(.+?)</h4>")
			if headerTitleHtml is not None:
				headerTitle = super(FII_FBParser,self).ParseAndReplace(headerTitleHtml,r"<(.+?)>","")
			if headerTitle is not None and headerTitle != "":
				headerTitle = headerTitle.strip()
		except Exception,e:
			pass
		return headerTitle
	def ParseInfoHeaderTitle(self,contents):
		headingTitle = ""
		try:
			headingSource = super(FII_FBParser,self).ParseSingle(contents,r"<th(.+?)</th>")
			if headingSource is not None:
				headingTitle = super(FII_FBParser,self).ParseAndReplace(headingSource,r"<(.+?)>","")
				if headingTitle is not None and headingTitle != "":
					headingTitle = headingTitle.strip()
		except Exception,e:
			pass
		return headingTitle
	def ParseExperiences(self,contents):
		experiences = []
		try:
			experiencesList = super(FII_FBParser,self).Parse(contents,r"<li(.+?)</li>")
			for eachExperience in experiencesList:
				experienceTitleHtml = super(FII_FBParser,self).ParseSingle(eachExperience,r"<div[\s]+class=[\'\"]?experienceTitle(.+?)</div>")
				experienceTitle = super(FII_FBParser,self).ParseAndReplace(experienceTitleHtml,r"<(.+?)>","")
				experienceBodyHtml = super(FII_FBParser,self).ParseSingle(eachExperience,r"<div[\s]+class=[\'\"]?experienceBody[\s]fsm(.+?)</div>")
				experienceBody = super(FII_FBParser,self).ParseAndReplace(experienceBodyHtml,r"<(.+?)>","")
				if experienceBody is not None:
					experienceBody = experienceBody.strip()
				data = {"experience_title":experienceTitle,"experience_body":experienceBody}
				experiences.append(data)
		except Exception,e:
			pass
		return experiences
			
	def ParseWorkAndEducation(self,page):
		allInfosAboutWorksAndEducation = []
		worksAndEducationEntity = None
		try:
			workAndEducationSource = page #super(FII_FBParser,self).ParseSingle(page,r"<div id=[\'\"]?pagelet_eduwork(.+?)</table>")
			workAndEducationHeaderTitle = self.ParseTitle(workAndEducationSource)
			dataTBodys = super(FII_FBParser,self).Parse(workAndEducationSource,r"<tbody>(.+?)</tbody>")
			for eachTbody in dataTBodys:
				try:
					infoTitle = self.ParseInfoHeaderTitle(eachTbody)
					experiences = self.ParseExperiences(eachTbody)
					infoData = {"info_title":infoTitle,"experiences":experiences}
					allInfosAboutWorksAndEducation.append(infoData)
				except Exception,e:
					pass
			worksAndEducationEntity = {"header_title":workAndEducationHeaderTitle,"data":allInfosAboutWorksAndEducation}
		except Exception,e:
			pass
		return worksAndEducationEntity
		#print workAndEducationSource
	def ParseContactInfoBodyContents(self,page):
		source = page
		sourceLIs = super(FII_FBParser,self).Parse(source,r"<li(.+?)</li>")
		singleContent = ""
		try:
			for eachLI in sourceLIs:
				try:
					formattedLI = super(FII_FBParser,self).ParseAndReplace(eachLI,r"<(.+?)>"," ")
					formattedLI = super(FII_FBParser,self).ParseAndReplace(formattedLI,r"(.+?)>"," ")
					formattedLI = super(FII_FBParser,self).ParseAndReplace(formattedLI,r"<(.+?)"," ")
					formattedLI = super(FII_FBParser,self).ParseAndReplace(formattedLI,r"(\s)+"," ")
					if formattedLI is not None:
						formattedLI = formattedLI.strip()
					singleContent += (formattedLI + ",")
				except Exception,e:
					continue
			singleContent = singleContent[:-1] # trancat the last comma. e.g Ahsanullah Hall,Buet,Dhaka, Bangladesh, to 
											   #e.g Ahsanullah Hall,Buet,Dhaka, Bangladesh
		except Exception,e:					   
			pass
		return singleContent

	def ParseContactInfoSinglePhone(self,page):
		mobilePhone = ""
		try:
			mobilePhone = super(FII_FBParser,self).ParseSingle(page,r"td[\s]+class=[\'\"]?contactInfoPhone(.+?)</td>")
			mobilePhone = super(FII_FBParser,self).ParseAndReplace(mobilePhone,r"<(.+?)>"," ")
			mobilePhone = super(FII_FBParser,self).ParseAndReplace(mobilePhone,r"(.+?)>"," ")
			mobilePhone = super(FII_FBParser,self).ParseAndReplace(mobilePhone,r"<(.+?)"," ")
			if mobilePhone is not None:
				mobilePhone = mobilePhone.strip()
		except Exception,e:
			mobilePhone = ""
		return mobilePhone

	def ParseContactInfoFacebook(self,page):
		facebookLink = ""
		try:
			facebookAnchor = super(FII_FBParser,self).ParseSingle(page,r"<a(.+?)</a>")
			facebookAnchorHref = super(FII_FBParser,self).ParseSingle(facebookAnchor,r"href=[\'\"]?(.+?)\"")
			facebookLink = super(FII_FBParser,self).ParseAndReplace(facebookAnchorHref,r"\"","")
			facebookLink = super(FII_FBParser,self).ParseAndReplace(facebookLink,r"href=","")
			if facebookLink is not None:
				facebookLink = facebookLink.strip()
		except Exception,e:
			pass
		return facebookLink

	def ParseContactInfo(self,page):
		allInfosAboutContactInfo = []
		contactInfoEntity = None
		try:
			contactInfoTitle = self.ParseTitle(page)
			dataTBodys = super(FII_FBParser,self).Parse(page,r"<tbody>(.+?)</tbody>")
			for eachTbody in dataTBodys:
				try:
					infoTitle = self.ParseInfoHeaderTitle(eachTbody)
					infoBody = ""
					if "Facebook</th>" in eachTbody: #If the contact info is facebook url.# It need to process differently cause it's structure is different from otheres.
						infoBody = self.ParseContactInfoFacebook(eachTbody)                     
					else: #If contact info is other than facebook. e.g. Mobile Phones,Address,Screen Name etc.
						infoBody = self.ParseContactInfoBodyContents(eachTbody)
					if infoTitle == "Mobile Phones" and infoBody == "":
						infoBody = self.ParseContactInfoSinglePhone(eachTbody)
					infoData = {"contact_info_title":infoTitle,"contact_info_body":infoBody}
					allInfosAboutContactInfo.append(infoData)
				except Exception,e:
					print "Exception: "+str(e)
					continue
			contactInfoEntity = {"header_title":contactInfoTitle,"data":allInfosAboutContactInfo}
		except Exception,e:
			print "Exception2: "+str(e)
			pass
		return contactInfoEntity
	
	def ParseBasicInfoBodyContents(self,page):
		contentsPartSource = ""
		try:
			contentsPartSource = super(FII_FBParser,self).ParseSingle(page,r"<td[\s]+class=[\'\"]?data(.+?)[(<hr>)(</ul>)]?</td></tr>")
			content = super(FII_FBParser,self).ParseAndReplace(contentsPartSource,r"<(.+?)>"," ")
			content = super(FII_FBParser,self).ParseAndReplace(content,r"^[\s]+"," ")
			content = super(FII_FBParser,self).ParseAndReplace(content,r"[\s]+$"," ")
			content = super(FII_FBParser,self).ParseAndReplace(content,r"\s[\s]+",",")
			return content
		except Exception,e:
			print str(contentsPartSource)+str(e)
			return ""
		
	def ParseFullName(self,page):
		fullName = None
		try:
			coverImageContainerElement = super(FII_FBParser,self).ParseSingle(page,r"<div[\s]class=[\'\"]coverImage(.+?)</h2>")
			if coverImageContainerElement is not None:
				fullNameContainerElement = super(FII_FBParser,self).ParseSingle(coverImageContainerElement,r"<h2(.+?)</h2>")
				if fullNameContainerElement is not None:
					fullName = super(FII_FBParser,self).ParseAndReplace(fullNameContainerElement,r"<(.+?)>","")
					fullName = super(FII_FBParser,self).ParseAndReplace(fullNameContainerElement,r"<(.+?)","")
					fullName = super(FII_FBParser,self).ParseAndReplace(fullNameContainerElement,r"(.+?)>","")
					if fullName is not None:
						fullName = fullName.strip()
		except Exception,exp:
			print str(exp)
		return fullName
					
	def ParseBasicInfo(self,page):
		allInfosAboutBasicInfo = []
		basicInfoEntity = None
		try:
			basicInfoTitle = self.ParseTitle(page)
			dataTBodys = super(FII_FBParser,self).Parse(page,r"<tbody>(.+?)</tbody>")
			for eachTbody in dataTBodys:
				infoTitle = self.ParseInfoHeaderTitle(eachTbody)
				infoBody = self.ParseBasicInfoBodyContents(eachTbody)
				basicInfoContentsRow = {"basic_info_data_title":infoTitle,"basic_info_data_body":infoBody}
				allInfosAboutBasicInfo.append(basicInfoContentsRow)
			basicInfoEntity = {"header_title":basicInfoTitle,"data":allInfosAboutBasicInfo}
		except Exception,e:
			print "Exception: "+str(e)
		return basicInfoEntity
		
	def ParseLivingLocations(self,page):
		locations = []
		livingEntity = None
		try:
			livingTitle = self.ParseTitle(page)
			dataBodysTd = super(FII_FBParser,self).Parse(page,r"<td[\s]+class=[\'\"]?data(.+?)</td>")
			for eachTd in dataBodysTd:
				locationType = super(FII_FBParser,self).ParseSingle(eachTd,r"<div[\s]+class=[\'\"]aboutSubtitle[\s]fsm(.+?)</div>")
				locationType = super(FII_FBParser,self).ParseAndReplace(locationType,r"<(.+?)>","")
				locationName = super(FII_FBParser,self).ParseSingle(eachTd,r"<div[\s]+class=[\'\"]fsl[\s]fwb[\s]fcb(.+?)</div>")
				locationName = super(FII_FBParser,self).ParseAndReplace(locationName,r"<(.+?)>","")
				locationName = super(FII_FBParser,self).ParseAndReplace(locationName,r"<(.+?)","")
				locationName = super(FII_FBParser,self).ParseAndReplace(locationName,r"(.+?)>","")
				if locationName is not None:
					locationName = locationName.strip()
				
				locationTuple = {}
				locationTuple["location_type"] = locationType
				locationTuple["location_name"] = locationName
				locations.append(locationTuple)
			livingEntity = {"header_title":livingTitle,"data":locations}
		except Exception,e:
			print "Exception"+str(e)
		return livingEntity
		
	def ParseAllAboutInfo(self,page): #This is the main entry file to call for users about information.
		#allInfo = super(FII_FBParser,self).Parse(page,r"<div[\s]+class=[\'\"]?fbTimelineSection mtm[\s]+(fbYearlyHistorySection[\s]+)?fbTimelineCompactSection(.+?)</code>")
		#fileP = open("source.html","wb")
		#fileP.write(page)
		#fileP.close()
		userAboutInfos = []
		worksAndEducationSource = super(FII_FBParser,self).ParseSingle(page,r"id=[\'\"]?pagelet_eduwork(.+?)</table>")
		contactInfoSource = super(FII_FBParser,self).ParseSingle(page,r"id=[\'\"]?pagelet_contact(.+?)</table></div></div>")
		basicInfoSource = super(FII_FBParser,self).ParseSingle(page,r"id=[\'\"]?pagelet_basic(.+?)</table></div></div>")
		livingLocationSource = super(FII_FBParser,self).ParseSingle(page,r"id=[\'\"]?pagelet_hometown(.+?)</table></div></div>")
		
		contactInfo = self.ParseContactInfo(contactInfoSource)
		worksAndEducations = self.ParseWorkAndEducation(worksAndEducationSource)
		basicInfo = self.ParseBasicInfo(basicInfoSource)
		livingLocationInfo = self.ParseLivingLocations(livingLocationSource)
		
		userAboutInfos.append(worksAndEducations)
		userAboutInfos.append(contactInfo)
		userAboutInfos.append(basicInfo)
		userAboutInfos.append(livingLocationInfo)
		
		return userAboutInfos
	def ParseMediasPageNameAndLink(self,page):
		mediaContents = super(FII_FBParser,self).Parse(page,r"<div[\s]+class=[\'\"]?mediaPortrait(.+?)</a>")
		allMedia = []
		try:
			for eachMediaContent in mediaContents:
				actualMediaContent = super(FII_FBParser,self).ParseSingle(eachMediaContent,r"<a(.+?)</div>")
				#print actualMediaContent
				mediaNameSource = super(FII_FBParser,self).ParseSingle(actualMediaContent,r"<div[\s]+class=[\'\"]?mediaPageName(.+?)</div>")
				mediaName = super(FII_FBParser,self).ParseAndReplace(mediaNameSource,r"<(.+?)>","")
				mediaLinkSource = super(FII_FBParser,self).ParseSingle(eachMediaContent,r"href=(.+?)\"")
				mediaLink = super(FII_FBParser,self).ParseAndReplace(mediaLinkSource,"\"","")
				mediaLink = super(FII_FBParser,self).ParseAndReplace(mediaLink,"href=","")
				if mediaLink is not None:
					mediaLink = mediaLink.strip()
				allMedia.append({"media_title":mediaName,"media_link":mediaLink})
		except Exception,exp:
			pass
		return allMedia
	def ParseFavoriteItemTitle(self,page):
		title = ""
		try:
			titleSource = super(FII_FBParser,self).ParseSingle(page,r"<th(.+?)</th>")
			if titleSource is not None:
				title = super(FII_FBParser,self).ParseAndReplace(titleSource,r"<(.+?)>","")
				if title is not None:
					title = title.strip()
		except Exception,exp:
			pass
		return title
	def ParseFavoriteItemContents(self,page):
		bodyContents = []
		try:
			bodyContents = self.ParseMediasPageNameAndLink(page)
		except Exception,exp:
			pass
		return bodyContents
	def FindAllFavoritesItemOfASingleCategory(self,page,elementId):
		favoritesItemsLIs = []
		try:
			favoritesContentArea = super(FII_FBParser,self).ParseSingle(page,r"id=[\'\"]?"+elementId+"(.+?)</ul>")
			if favoritesContentArea is not None:
				favoritesItemsLIs =  super(FII_FBParser,self).Parse(favoritesContentArea,r"<li[\s]+class=[\'\"]?_5rz(.+?)</li>")
		except Exception,exp:
			pass
		return favoritesItemsLIs
		
	def FindProductInfo(self,productSource):
		productInfo = {}
		try:
			productNameContainerAnchor = super(FII_FBParser,self).ParseSingle(productSource,r"<a[\s]+class=[\'\"]?_gx7(.+?)</a>")
			if productNameContainerAnchor is not None:
				productName = super(FII_FBParser,self).ParseAndReplace(productNameContainerAnchor,r"<(.+?)>","")
				productLinkSource = super(FII_FBParser,self).ParseSingle(productNameContainerAnchor,r"href=[\'\"](.+?)\"")   
				productLink = super(FII_FBParser,self).ParseAndReplace(productLinkSource,r"href=","")
				productLink = super(FII_FBParser,self).ParseAndReplace(productLink,r"\"","")
				productInfo["title"] = productName
				productInfo["link"] = productLink
			productTypeContainerElementSpan = super(FII_FBParser,self).ParseSingle(productSource,r"<span[\s]+class=[\'\"]?_4-if[\s]fwn(.+?)</span>")
			if productInfo.get("title") is not None and productTypeContainerElementSpan is not None:
				productType = super(FII_FBParser,self).ParseAndReplace(productTypeContainerElementSpan,r"<(.+?)>","")
				productInfo["type"] = productType
		except Exception,e:
			print str(e)
		return productInfo
	def ParseAllFavoritesInfo(self,page):
		allFavorites = []
		try:
			contentTable = super(FII_FBParser,self).ParseSingle(page,r"<table[\s]+class=[\'\"]?uiInfoTable(.+?)</table>")
			contentTbodys = super(FII_FBParser,self).Parse(contentTable,r"<tbody>[\s]*<tr>(.+?)</tbody>")
			for eachItem in contentTbodys:
				itemTitle = self.ParseFavoriteItemTitle(eachItem)
				favoritesBodyContents = self.ParseFavoriteItemContents(eachItem)
				allFavorites.append({"favorites_title":itemTitle,"favorites_contents":favoritesBodyContents})
		except Exception,exp:
			pass
		return allFavorites
	def ParseContentNotAvailableInfo(self,page):
		try:
			return super(FII_FBParser,self).ParseSingle(page,r"<h2[\s]+class=[\'\"]?_4-dp(.+?)Sorry,[\s]this[\s]page[\s]isn[\']t[\s]available</h2>")
		except Exception,exp:
			return None
	def ParseLikeYearContainerLIs(self,page):
		lIs = []
		try:
			lIs = super(FII_FBParser,self).Parse(page,r"<li[\s]+class=[\'\"]?mbs[\s]uiFavoritesStory([\s]uiListItem)?(.+?)</li>")
		except Exception,exp:
			pass
		return lIs
	def ParseLikePageContents(self,likeContentEntireRow):
		try:
			empty,likeContentRow = likeContentEntireRow
			pageCategorySource = super(FII_FBParser,self).ParseSingle(likeContentRow,r"<div[\s]+class=[\'\"]?fsm[\s]fwn[\s]fcg(.+?)</div>")
			pageCategory = super(FII_FBParser,self).ParseAndReplace(pageCategorySource,r"<(.+?)>","")
			pageNameAndLinkSource = super(FII_FBParser,self).ParseSingle(likeContentRow,r"<div[\s]+class=[\'\"]?nameText(.+?)</div>")
			pageLinkSource = super(FII_FBParser,self).ParseSingle(pageNameAndLinkSource,r"href=[\'\"]?(.+?)\"")
			pageLink = super(FII_FBParser,self).ParseAndReplace(pageLinkSource,r"\"","")
			pageLink = super(FII_FBParser,self).ParseAndReplace(pageLink,r"href=","")
			pageName = super(FII_FBParser,self).ParseAndReplace(pageNameAndLinkSource,r"<(.+?)>","")
			return {"title":pageName,"link":pageLink,"category":pageCategory}
		except Exception,exp:
			return None
	def ParseFriendsCount(self,pageSource):
		friendsCount = ""
		try:
			friendsListDiv = None
			allDivsSimilarShowingListOfFriends = super(FII_FBParser,self).Parse(pageSource,r"<div[\s]class=[\'\"]fsm[\s]fwn[\s]fcg(.+?)</div>")
			if allDivsSimilarShowingListOfFriends is not None:
				for eachDiv in allDivsSimilarShowingListOfFriends:
					friendsHeading = super(FII_FBParser,self).ParseSingle(eachDiv,r"<span[\s]class=[\'\"]_70n[\'\"]>Friends</span>")
					if friendsHeading is not None and friendsHeading != "":
						friendsCountSpan = super(FII_FBParser,self).ParseSingle(eachDiv,r"<span[\s]class=[\'\"]fwn[\s]fcg[\'\"]>(.+?)</span>")
						if friendsCountSpan is not None:
							friendsCount = super(FII_FBParser,self).ParseAndReplace(friendsCountSpan,r"<(.+?)>","")
						break
		except Exception,exp:
			pass
		return friendsCount
	def ParsePostsWithLikeAndCommentsCount(self,pageSource):
		posts = []
		try:
			postListLIs = super(FII_FBParser,self).Parse(pageSource,r"<li[\s]class=[\'\"]fbTimelineUnit(.+?)</li>")
			for eachPostLI in postListLIs:
				postText = ""
				postContentElement = super(FII_FBParser,self).ParseSingle(eachPostLI,r"<span[\s]class=[\'\"]userContent(.+?)</span>")
				if postContentElement is not None:
					postText = super(FII_FBParser,self).ParseAndReplace(postContentElement,r"<(.+?)>","")
				if postText != "":
					postLikesCount,postCommentsCount,postSharesCount = "","",""
					"""First try to find out the list of reactions elements."""
					postReactionElements = super(FII_FBParser,self).Parse(eachPostLI,r"<span[\s]class=[\'\"]UFIBlingBoxText(.+?)</span>")
					if len(postReactionElements) == 0:
						postLikesCountElement = super(FII_FBParser,self).ParseSingle(eachPostLI,r"<span[\s]class=[\'\"]fbTimelineFeedbackLikes(.+?)</span>")
						if postLikesCountElement is not None:
							postLikesCount = super(FII_FBParser,self).ParseAndReplace(postLikesCountElement,r"<(.+?)>","")
						postCommentsCountElement = super(FII_FBParser,self).ParseSingle(eachPostLI,r"<span[\s]class=[\'\"]fbTimelineFeedbackComments(.+?)</span>")
						if postCommentsCountElement is not None:
							postCommentsCount = super(FII_FBParser,self).ParseAndReplace(postCommentsCountElement,r"<(.+?)>","")
						postSharesCountElement = super(FII_FBParser,self).ParseSingle(eachPostLI,r"<span[\s]class=[\'\"]fbTimelineFeedbackShares(.+?)</span>")
						if postSharesCountElement is not None:
							postSharesCount = super(FII_FBParser,self).ParseAndReplace(postSharesCountElement,r"<(.+?)>","")
					else:
						if len(postReactionElements) > 0:
							postLikesCountElement = postReactionElements[0]
							if postLikesCountElement is not None:
								postLikesCount = super(FII_FBParser,self).ParseAndReplace(postLikesCountElement,r"(.+?)>","")
								postLikesCount = super(FII_FBParser,self).ParseAndReplace(postLikesCount,r"<(.+?)>","")
						if len(postReactionElements) > 1:
							postCommentsCountElement = postReactionElements[1]
							if postCommentsCountElement is not None:
								postCommentsCount = super(FII_FBParser,self).ParseAndReplace(postCommentsCountElement,r"(.+?)>","")
								postCommentsCount = super(FII_FBParser,self).ParseAndReplace(postCommentsCount,r"<(.+?)>","")
						if len(postReactionElements) > 2:
							postSharesCountElement = postReactionElements[2]
							if postSharesCountElement is not None:
								postSharesCount = super(FII_FBParser,self).ParseAndReplace(postSharesCountElement,r"(.+?)>","")
								postSharesCount = super(FII_FBParser,self).ParseAndReplace(postSharesCount,r"<(.+?)>","")
					if postLikesCount == "":
						postLikesCount = "0"
					if postCommentsCount == "":
						postCommentsCount = "0"
					if postSharesCount == "":
						postSharesCount = "0"
					posts.append({"post_message":postText,"likes":{"count":postLikesCount},"comments":{"count":postCommentsCount},"shares":{"count":postSharesCount}})
		except Exception,exp:
			pass
		return posts
		
		