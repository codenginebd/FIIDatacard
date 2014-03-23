from selenium import webdriver
import time
class WebBrowser:
	def __init__(self):
		try:
#			self.browser = webdriver.Firefox()
			self.browser = webdriver.Chrome()
		except Exception,exp:
			print "Webdriver open failed."
	def OpenURL(self,url):
		try:
			self.browser.get(url)
		except Exception,exp:
			pass
	def GetPage(self):
		try:
			self.page = self.browser.page_source
			encodedStr = self.page.encode("ascii","xmlcharrefreplace") 
			return encodedStr
		except Exception,exp:
			return None
	def FindMoreLinkedElements(self):
		try:
			elements = self.browser.find_elements_by_class_name("mediaRowRevealer")
			return elements
		except Exception,exp:
			return None
	def ClickElement(self,element):
		try:
			if element is not None:
				try:
					element.click()
					time.sleep(10)
					return True
				except Exception,e:
					print "Click Exception: "+str(e)
					return False
		except Exception,exp:
			return False
	def ClickOnMoreInfoElements(self):
		try:
			elements = self.FindMoreLinkedElements()
			for anElement in elements:
				if anElement is not None:
					try:
						anElement.click()
					except Exception,e:
						pass
			time.sleep(6)
		except Exception,exp:
			pass
	def FindLikesYearLinkElement(self):
		elements = self.browser.find_elements_by_class_name("prl")
		return elements
		#WebDriverWait(browser, 6).until(lambda driver : driver.find_element_by_xpath("//div[@class='mediaRowWrapper']/div[@class='mediaRowWrapper']"))
	def LoginFacebook(self,loginCredentials):
		try:
			email = loginCredentials["email"]
			password = loginCredentials["password"]
			emailField = self.browser.find_element_by_id("email")
			emailField.send_keys(email)
			passwordField = self.browser.find_element_by_id("pass")
			passwordField.send_keys(password)
			submitButton = self.browser.find_element_by_id("loginbutton")
			submitButton.click()
			return True
		except Exception,exp:
			return False
	def LoginLinkedIn(self,loginCredentials):
		email = loginCredentials["email"]
		password = loginCredentials["password"]
		try:
			emailField = self.browser.find_element_by_id("session_key-login")
			emailField.send_keys(email)
			passwordField = self.browser.find_element_by_id("session_password-login")
			passwordField.send_keys(password)
			time.sleep(6)
			submitButton = self.browser.find_element_by_id("signin")
			submitButton.click()
		except Exception,exp:
			pass
	def LoginGoogle(self,loginCredentials):
		try:
			email = loginCredentials["email"]
			password = loginCredentials["password"]
			emailField = self.browser.find_element_by_id("Email")
			emailField.send_keys(email)
			passwordField = self.browser.find_element_by_id("Passwd")
			passwordField.send_keys(password)
			signInButton = self.browser.find_element_by_id("signIn")
			signInButton.click()
			return True
		except Exception,exp:
			return False
	def LoginTwitter(self,loginCredentials):
		try:
			email = loginCredentials.get("email")
			password = loginCredentials.get("password")
			emailField = self.browser.find_element_by_id("signin-email")
#			print emailField
			if emailField is not None:
				emailField.send_keys(email)
			passwordField = self.browser.find_element_by_id("signin-password")
			if passwordField is not None:
				passwordField.send_keys(password)
			time.sleep(2)
			signInButton = self.browser.find_element_by_css_selector(".submit.btn.primary-btn.flex-table-btn.js-submit")
			if signInButton is not None:
				signInButton.click()
				return True
		except Exception,exp:
			return False
	def ClickTwitterConnectButtonInKLout(self):
		try:
			time.sleep(2)
			twitterConnectButton = self.browser.find_element_by_css_selector(".tw-connect.button")
			if twitterConnectButton is not None:
				twitterConnectButton.click()
				time.sleep(10)
		except Exception,exp:
			print "ClickTwitterConnectButtonInKLout: "+str(exp)
	def LoginKLout(self,loginCredentials):
		email = loginCredentials.get("email")
		password = loginCredentials.get("password")
		try:
			emailField = self.browser.find_element_by_id("username_or_email")
			if emailField is not None:
				emailField.send_keys(email)
			passwordField = self.browser.find_element_by_id("password")
			if passwordField is not None:
				passwordField.send_keys(password)
			signInButton = self.browser.find_element_by_id("allow")
			if signInButton is not None:
				signInButton.click()
		except Exception,exp:
			print "KLout Login: "+str(exp)
	def FindElementByName(self,elementName):
		try:
			element = self.browser.find_element_by_name(elementName)
			return element
		except Exception,exp:
			return None
	def FindElementById(self,elementId):
		try:
			element = self.browser.find_element_by_id(elementId)
			return element
		except Exception,exp:
			return None
	def ExecuteScriptAndWait(self,code):
		try:
			self.browser.execute_script(code)
			time.sleep(10)
		except Exception,exp:
			pass
	def GetPageURL(self):
		try:
			return self.browser.current_url
		except Exception,exp:
			return None
	def Close(self):
		try:
			self.browser.close()
		except Exception,exp:
			print "Browser closing failed."