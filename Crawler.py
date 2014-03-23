#!/usr/bin/env python
#Required Libraries:
#selenium,chromedriver,simplejson
from Tkinter import *
from selenium import webdriver
from facebook import *
import threading
import time
import datetime
import simplejson as json
from ConfigParser import *
import pdb
from Browser import *
from globals import *
from bs4 import BeautifulSoup
import re
from facebook import *
from LinkedIn import *
from GooglePlus import *
from libraries import *
from Twitter import *
from KLout import *
import json
from hbase import *

class Crawler:
	def __init__(self):
		print "Initializing Crawler..."
		self.browser = Browser()
		self.parserBase = FIIParser()
		self.parser = FII_FBParser()
		self.fbGraph = FBGraph()
		self.fbOauth = FBOauth(self.browser)
		self.facebookCrawler = FBCrawler()
		self.linkedin = LinkedIn()
		self.googlePlus = FIIGooglePlus(self.browser)
		self.twitter = Twitter()
		self.klout = KLout()
		self.hbase = HBase()
		self.merger = Merger()
		self.utility = Utility()
		self.matcher = ProfileMatcher()
	def Authenticate(self):
		facebookLoginStatus,linkedInLoginStatus,googleLoginStatus,twitterLoginStatus,kloutLoginStatus = False,False,False,False,False
		"""Authorize Facebook"""
		fbLoginCredentials = {"email":FIIConstants.Credentials.Facebook.EMAIL,"password":FIIConstants.Credentials.Facebook.PASSWORD}
		self.browser.OpenURL(FIIConstants.FACEBOOK_ROOT_URL)
		facebookLoginStatus = self.browser.LoginFacebook(fbLoginCredentials)
		
		if facebookLoginStatus is True:
			passwordElement = self.browser.CheckIfPasswordElementExistsInFacebook()
			if passwordElement is not None:
				return False
		else:
			return False
		""" Authorize LinkedIn """
		linkedInCredentials = {"email":FIIConstants.Credentials.LinkedIn.EMAIL,"password":FIIConstants.Credentials.LinkedIn.PASSWORD}
		linkedInLoginStatus = self.linkedin.Authorize(self.browser,linkedInCredentials)
		
		if linkedInLoginStatus is True:
			linkedInPasswordBox = self.browser.CheckIfPasswordElementExistsInLinkedIn()
			if linkedInPasswordBox is not None:
				return False
		else:
			return False
		"""Authorize Google Plus"""
		googlePlusLoginCredentials = {"email":FIIConstants.Credentials.Google.EMAIL,"password":FIIConstants.Credentials.Google.PASSWORD}
		googleLoginStatus = self.googlePlus.Authenticate(googlePlusLoginCredentials)
		
		if googleLoginStatus is True:
			googlePasswordButton = self.browser.CheckIfPasswordElementExistsInGoogle()
			if googlePasswordButton is not None:
				return False
		else:
			return False
		
		"""Authorize Twitter"""
		twitterLoginCredentials = {"email":FIIConstants.Credentials.Twitter.EMAIL,"password":FIIConstants.Credentials.Twitter.PASSWORD}
		twitterLoginStatus = self.twitter.Login(self.browser,twitterLoginCredentials)
		
		if twitterLoginStatus is True:
			twitterPasswordElement = self.browser.CheckIfTwitterPasswordElementExists()
			if twitterPasswordElement is not None:
				return False
		else:
			return False
		
		"""Authorize KLout"""
		kloutLoginCredentials = {"email":FIIConstants.Credentials.KLout.EMAIL,"password":FIIConstants.Credentials.KLout.PASSWORD}
		kloutLoginStatus = self.klout.Login(self.browser,kloutLoginCredentials)
		
		if kloutLoginStatus is True:
			passwordBoxKlout = self.browser.CheckIfPasswordElementExistsInKLout()
			if passwordBoxKlout is not None:
				return False
		else:
			return False
		
		return True
	
	def GetTwitterLinksFromLinkedInProfile(self,linkedInProfile):
		twitterProfiles = []
		try:
			if linkedInProfile is not None:
				linkedInContactInfo = linkedInProfile.get("contact_info")
				if linkedInContactInfo is not None:
					twitterDataArray = linkedInContactInfo.get("twitter")
					if twitterDataArray is not None:
						for eachTwitterData in twitterDataArray:
							twitterProfileLink = eachTwitterData.get("data")
							if twitterProfileLink is not None:
								twitterProfiles.append(twitterProfileLink)
		except Exception,exp:
			pass
		return twitterProfiles
	
	def FindTwitterProfileThatHaveMaximumFollowersCount(self,twitterLinksArray):
		followersCount = 0
		twitterProfileWithMaxFollowerCount = None
		for eachTwitterProfileLink in twitterLinksArray:
			tempTwitterProfile = self.twitter.CrawlProfile(self.browser,{"link":eachTwitterProfileLink})
			if tempTwitterProfile is not None:
				if twitterProfileWithMaxFollowerCount is None:
					twitterProfileWithMaxFollowerCount = tempTwitterProfile
				else:
					twitterFollowersCount = tempTwitterProfile.get("followers_count")
					if twitterFollowersCount is not None:
						tempFollowersCount = int(twitterFollowersCount)
						if tempFollowersCount > followersCount:
							followersCount = tempFollowersCount
							twitterProfileWithMaxFollowerCount = tempTwitterProfile
		return twitterProfileWithMaxFollowerCount
		
	def Run(self):
		LIMIT = 50
		accessToken = ""
		try:
			authenticationStatus = self.Authenticate()
			if authenticationStatus is True:
				usersResponse = self.hbase.DownloadBasicProfile(count=LIMIT)
				if usersResponse.get("failure_indication") == 1:
					print "Basic info reading failed from database."
					return
				else:
					while True:
						users = usersResponse.get('data')
						if users is not None and type(users) is list:
							if len(users) == 0:
								print "Crawling has been done successfully."
								return	
							if accessToken == "":
								accessToken = self.fbOauth.GetAccessToken()
							if accessToken is None or accessToken == "":
								raise Exception,"Getting access token for facebook failed!"
							for eachUser in users:
								email = eachUser.get("d:email")
								firstName = eachUser.get("d:first_name")
								lastName = eachUser.get("d:last_name")
								facebookProfileLink = eachUser.get("d:facebook")
								twitterLink = eachUser.get("d:twitter")
								linkedInProfileLink = eachUser.get("d:linkedin")
								googlePlusProfileLink = eachUser.get("d:google_plus")
								
								
								facebookProfile,linkedInProfile,googlePlusProfile,twitterProfile,kloutProfile = None,None,None,None,None
								
								facebookProfileBasic = None
								facebookProfileLinkFoundInBasicProfileInfo = False
								
								if facebookProfileLink is not None and facebookProfileLink != "":
									facebookProfileBasic["link"] = facebookProfileLink
									facebookProfileLinkFoundInBasicProfileInfo = True
								
								if facebookProfileLinkFoundInBasicProfileInfo is False:
									simplifiedEachUser = {"email":email,"first_name":firstName,"last_name":lastName,"twitter":twitterLink,"linkedin":linkedInProfileLink}
								
									facebookProfileBasic = self.fbGraph.SearchUsersAndGetProfileLinks(self.browser,self.parserBase,self.utility,accessToken,simplifiedEachUser)
									if facebookProfileBasic is not None and facebookProfileBasic == "SEARCH_FAILED_WITH_OAUTH_EXCEPTION":
										print "Facebook Profile Search failed. Maybe the netweok connection problem or user's facebook credentials has been changed. Program exiting..."
										return
								
								facebookProfileNotFound = True
								
								if facebookProfileBasic is not None:
									facebookProfile = self.facebookCrawler.CrawlProfile(self.browser,self.parser,facebookProfileBasic)
									
			#						f = open("facebook_data.json","w")
			#						f.write(json.dumps(facebookProfile))
									
									if facebookProfile is None:
										facebookProfile = {"email":email}
										facebookProfileNotFound = True
									else:
										facebookProfile["email"] = email
										facebookProfileNotFound = False
								else:
									facebookProfile = {"email":email}
									facebookProfileNotFound = True
										
								if googlePlusProfileLink is not None and googlePlusProfileLink != "":
									googlePlusProfileBasic = {"link":googlePlusProfileLink}
									googlePlusProfile = self.googlePlus.CrawlProfile(googlePlusProfileBasic)
								else:
									if facebookProfileNotFound is False:
										userFirstName = eachUser.get("first_name") if eachUser.get("first_name") is not None else ""
										userLastName = eachUser.get("last_name") if eachUser.get("last_name") is not None else ""
										userFullName = userFirstName+userLastName
										googlePlusProfileBasic = {}
										profileMatched = False
										if userFullName != "":
											googlePlusProfileBasic["full_name"] = userFullName
											googlePlusSearchResult = self.googlePlus.SearchPeople(googlePlusProfileBasic)
											if googlePlusSearchResult is not None:
												for eachSearchResult in googlePlusSearchResult:
													if eachSearchResult is not None and eachSearchResult.get("profile_link") is not None and eachSearchResult.get("profile_link") != "":
														googlePlusProfileBasic["link"] = eachSearchResult.get("profile_link")
														googlePlusProfile = self.googlePlus.CrawlProfile(googlePlusProfileBasic)
														"""Match google plus profile."""
														profileMatched = self.matcher.MatchGooglePlus(facebookProfile,googlePlusProfile)
														if profileMatched is True:
															break
										if profileMatched is False:
											googlePlusProfile = None
											
								if linkedInProfileLink is not None and linkedInProfileLink != "":
									linkedInProfile = self.linkedin.CrawlProfile(self.browser,linkedInProfileLink)
								
								twitterName = None
								
								if twitterLink is not None:
									twitterName = twitterLink[twitterLink.rindex("/")+1:len(twitterLink)]
									twitterProfile = self.twitter.CrawlProfile(self.browser,{"link":twitterLink})
								else:
									###Get twitter link from linkedin profile.
									if linkedInProfile is not None:
										twitterLinksArray = self.GetTwitterLinksFromLinkedInProfile(linkedInProfile)
										twitterProfile = self.FindTwitterProfileThatHaveMaximumFollowersCount(twitterLinksArray)
										
									if twitterProfile is None:
										###Now check for twitter profile links in Google Plus.
										if googlePlusProfile is not None:
											googlePlusNetworkLinks = googlePlusProfile.get("network_links")
											if googlePlusNetworkLinks is not None:
												googlePlusTwitterLinks = googlePlusNetworkLinks.get("twitter")
												if googlePlusNetworkLinks is not None:
													###googlePlusTwitterLinks is a list of twitter profile links.
													###Now we will traverse each twitter profile and get the profile that have maximum number
													###of followers count.
													twitterProfile = self.FindTwitterProfileThatHaveMaximumFollowersCount(googlePlusNetworkLinks)
								
								if twitterName is not None:
									kloutProfile = self.klout.CrawlKLoutProfile(self.browser,{"twitter_user_name":twitterName})
								else:
									if twitterProfile is not None:
										twitterProfileUrl = twitterProfile.get("twitter_profile_link")
										if twitterProfileUrl[len(twitterProfileUrl) - 1] == "/":
											twitterProfileUrl = twitterProfileUrl[:-1]
										twitterName = twitterLink[twitterLink.rindex("/")+1:len(twitterLink)]
										if twitterName is not None:
											kloutProfile = self.klout.CrawlKLoutProfile(self.browser,{"twitter_user_name":twitterName})
									
								merger = Merger()
								completeProfile = self.merger.Merge(facebookProfile,linkedInProfile,googlePlusProfile,twitterProfile,kloutProfile)
								if completeProfile is not None and type(completeProfile) is dict:
									if twitterLink is not None:
										completeProfile["twitter_profile_link"] = twitterLink
									if linkedInProfileLink is not None:
										completeProfile["linkedin_profile_link"] = linkedInProfileLink
									basicInfoCity = eachUser.get("city")
									if basicInfoCity is not None:
										if completeProfile.get("living_info") is not None:
											completeProfile.get("living_info")["city"] = basicInfoCity
									basicInfoState = eachUser.get("state")
									if basicInfoState is not None:
										if completeProfile.get("living_info") is not None:
											completeProfile.get("living_info")["state"] = basicInfoState
									basicInfoZip = eachUser.get("zip")
									if basicInfoZip is not None:
										if completeProfile.get("living_info") is not None:
											completeProfile.get("living_info")["zip"] = basicInfoZip
									basicInfoAddressOne = eachUser.get("address1")
									if basicInfoAddressOne is not None and basicInfoAddressOne != "null":
										if completeProfile.get("living_info") is not None:
											completeProfile.get("living_info")["address_one"] = basicInfoAddressOne
									basicInfoAddressTwo = eachUser.get("address2")
									if basicInfoAddressTwo is not None and basicInfoAddressTwo != "null":
										if completeProfile.get("living_info") is not None:
											completeProfile.get("living_info")["address_two"] = basicInfoAddressTwo
									basicInfoContactPhone = eachUser.get("phone1")
									if basicInfoContactPhone is not None:
										if completeProfile.get("contact_info") is not None:
											completeProfile.get("contact_info")["contact_phone"] = basicInfoContactPhone
									basicInfoHSGradYear = eachUser.get("hs_grad_year")
									if basicInfoHSGradYear is not None:
										if completeProfile.get("general_info") is not None:
											completeProfile.get("general_info")["hs_grad_year"] = basicInfoHSGradYear
				#				print completeProfile
								"""Saving will be done here."""
								if completeProfile is not None and type(completeProfile) is dict:
									updateTime = datetime.datetime.utcnow()
									completeProfile["last_update_time"] = updateTime
								
											
								fullProfileUploadResponse = self.hbase.UploadSingleFullProfile(completeProfile)
								if fullProfileUploadResponse.get("failure_indication") == 0:
									print "Successfully uploaded."
								else:
									print "Uploading failed! Response returned: "+str(fullProfileUploadResponse)
								"""Processing has been done for the list of users."""
			else:
				print "Authentication Failed.."
				return
		except Exception,exp:
			print "Exception occured."+str(exp)
			return