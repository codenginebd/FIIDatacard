import oauth2 as oauth
import urlparse
from LinkedInParser import *

class LIOauth:
	def __init__(self,appKey,appSecret):
		self.consumer_key = appKey
		self.consumer_secret = appSecret
		self.request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken?scope=r_emailaddress+r_network'
		self.access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
		self.authorize_url = 'https://www.linkedin.com/uas/oauth/authenticate'
		print "Initializing LinkedIn Oauth Library..."
	def GetPIN(self,browser,requestUrl,linkedInCredentials):
		accessCode = ""
		email = linkedInCredentials.get("email")
		password = linkedInCredentials.get("password")
		browser.OpenURL(requestUrl)
		#authPageSource = browser.GetPage()
		allowAccessButton = browser.FindElementByName("authorize")
		if allowAccessButton is not None:
			emailInputBox = browser.FindElementByName("session_key")
			emailInputBox.send_keys(email)
			passwordInputBox = browser.FindElementByName("session_password")
			passwordInputBox.send_keys(password)
			allowAccessButton.click()
		accessCodePageSource = browser.GetPage()
		liParser = LinkedInParser()
		accessCode = liParser.ParseAccessCode(accessCodePageSource)
		return accessCode
	def Authorize(self,browser,linkedInCredentials):
		consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
		client = oauth.Client(consumer)
		resp, content = client.request(self.request_token_url, "POST")
		request_token = dict(urlparse.parse_qsl(content))
		requestUrl = "%s?oauth_token=%s" % (self.authorize_url, request_token['oauth_token'])
		#print "Copy this url into the browser: "
		print requestUrl
		oauth_verifier = self.GetPIN(browser,requestUrl,linkedInCredentials)
		#oauth_verifier = raw_input('Enter the PIN here: ')
		#Now pass in verifier code in order to upgrade for access token
		token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
		token.set_verifier(oauth_verifier)
		client = oauth.Client(consumer, token)
		resp, content = client.request(self.access_token_url, "POST")
		access_token = dict(urlparse.parse_qsl(content))
		# API call to retrieve profile using access token
		token = oauth.Token(key=access_token['oauth_token'],secret=access_token['oauth_token_secret'])
		self.client = oauth.Client(consumer, token)
		print "LinkedIn Authorization Successful."
	def Call(self,url):
		returnedContent = None,None
		if self.client is not None:
			resp, content = self.client.request(url)
			if resp is not None and resp["status"] == "200":
				returnedContent = content
			else:
				returnedContent = ""
		return returnedContent ###Return JSON response
				
		return resp,content
	
	