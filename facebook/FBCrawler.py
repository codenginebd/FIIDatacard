import pdb
from bs4 import BeautifulSoup
import re
from facebook import *

class FBCrawler:
	def __init__(self):
		pass
	def FindSingleTypeFavorites(self,link):
		self.browser.OpenURL(link)
		pageSource = self.browser.GetPage()
		pageSoup = BeautifulSoup(pageSource)
		likeCategoriesAnchors = pageSoup.find_all("a", {"class":"_3c_"})
		likeProductList = []
		categoriesDataIds = []
		for eachCategory in likeCategoriesAnchors:
			anchorId = eachCategory["id"]
			ariaControlsAttribute = eachCategory["aria-controls"]
			itemType = eachCategory.contents[0].string
			categoriesDataIds.append({"anchor_id":anchorId,"element_id":ariaControlsAttribute,"item_type":itemType})
		for eachCategoryDataId in categoriesDataIds:
			scrollToLikeElementJSCode = 'var elem = document.getElementById("'+eachCategoryDataId.get("anchor_id")+'");window.scrollTo(0, elem.scrollHeight);'
			self.browser.ExecuteScriptAndWait(scrollToLikeElementJSCode)
			webelement = self.browser.FindElementById(eachCategoryDataId.get("anchor_id"))
			self.browser.ClickElement(webelement)
			eachCategoryPageSource = self.browser.GetPage()
			favoritesItemsLIs = self.parser.FindAllFavoritesItemOfASingleCategory(eachCategoryPageSource,eachCategoryDataId.get("element_id"))
			allItemsPreviousCall,allItemsCurrentCall = [],favoritesItemsLIs
			if len(favoritesItemsLIs) >= 12:
				while len(allItemsPreviousCall) < len(allItemsCurrentCall):
					allItemsPreviousCall = allItemsCurrentCall
					self.browser.ExecuteScriptAndWait("window.scrollTo(0, document.body.scrollHeight);")
					pageSource = self.browser.GetPage()
					allItemsCurrentCall = self.parser.FindAllFavoritesItemOfASingleCategory(pageSource,eachCategoryDataId.get("element_id"))
					if len(allItemsCurrentCall) >= 12:
						break
			likeProductListForACategory = []
			for eachItem in allItemsCurrentCall:
				aProduct = self.parser.FindProductInfo(eachItem)
				likeProductListForACategory.append(aProduct)
			if len(likeProductListForACategory) > 0:
				likeProductList.append({"type":eachCategoryDataId.get("item_type"),"data":likeProductListForACategory})
		return likeProductList
	def CrawlProfile(self,browser,parser,facebookBasicProfile):
		self.browser = browser
		self.parser = parser
		if facebookBasicProfile.get("link") is None or facebookBasicProfile.get("link") == "":
			raise Exception,"Facebook profile link could not be found."
		profileLink = facebookBasicProfile.get("link")
		timeLineLink = profileLink
		aboutLink = profileLink+"about"
		infoLink = profileLink+"info"
		moviesLink = profileLink+"movies"
		tvShowsLink = profileLink+"tv"
		musicLink = profileLink+"music"
		booksLink = profileLink+"books"
		likesLink = profileLink+"favorites"
		userFacebookProfile = {}
		userLikesAndFavorites = {}
		userFavorites = {}
		userFacebookProfile["email"] = facebookBasicProfile.get("email")
		self.browser.OpenURL(timeLineLink)
		timeLinePageSource = self.browser.GetPage()
		friendsCount = self.parser.ParseFriendsCount(timeLinePageSource)
		userFacebookProfile["friends_count"] = friendsCount
		
		"""Now scroll the timeline page for sometimes."""
		scrollCount = 1
		userWallPosts = []
		while scrollCount <= 3 and len(userWallPosts) <= 10:
			self.browser.ExecuteScriptAndWait("window.scrollTo(0, document.body.scrollHeight);")
			timeLinePageSource = self.browser.GetPage()
			userWallPosts = self.parser.ParsePostsWithLikeAndCommentsCount(timeLinePageSource)
			scrollCount += 1
		userFacebookProfile["posts"] = userWallPosts
		self.browser.OpenURL(infoLink)
		infoPageSource = self.browser.GetPage()
		favorites = []
		userFacebookProfile["facebook_profile"] = profileLink
		fullName = self.parser.ParseFullName(infoPageSource)
		userFacebookProfile["full_name"] = fullName
		aboutInfo = self.parser.ParseAllAboutInfo(infoPageSource)
		userFacebookProfile["about"] = aboutInfo
		likeItems = self.FindSingleTypeFavorites(likesLink)
		userLikesAndFavorites["user_likes"] = likeItems
		musicItems = self.FindSingleTypeFavorites(musicLink)
		userFavorites["favorites_music"] = musicItems
		moviesItems = self.FindSingleTypeFavorites(moviesLink)
		userFavorites["favorites_movies"] = moviesItems
		tvItems = self.FindSingleTypeFavorites(tvShowsLink)
		userFavorites["favorites_tvshows"] = tvItems
		booksItems = self.FindSingleTypeFavorites(booksLink)
		userFavorites["favorites_books"] = booksItems
		userLikesAndFavorites["user_favorites"] = userFavorites
		userFacebookProfile["favorites"] = userLikesAndFavorites 
		return userFacebookProfile