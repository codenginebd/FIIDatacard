#!/usr/bin/env python
#Required Libraries:
#selenium,chromedriver,simplejson,thrift,happybase,beautifulsoap
import os,sys
from Tkinter import *
from ttk import *
import tkFont
import threading
import time
from FII_BigData_Downloader_Main import *
from FII_BigData_Uploader_Main import *
from LinkedIn import *
from libraries import *
from globals import *
from Crawler import *
import base64
import tkMessageBox
	
class Application(Frame):
    def StartScraping(self):
    	FII_Logger.LogINFO("Crawling Started.")
    	
    	configValues = FIIConfig().Read()
    	
    	fbEmail = configValues.get("FB_EMAIL")
    	fbPass = configValues.get("FB_PASSWORD")
    	linkedInEmail = configValues.get("LI_EMAIL")
    	linkedInPass = configValues.get("LI_PASSWORD")
    	googleEmail = configValues.get("GOOGLE_EMAIL")
    	googlePass = configValues.get("GOOGLE_PASSWORD")
    	
    	FIIConstants.Credentials.Facebook.EMAIL = base64.decodestring(fbEmail)
    	FIIConstants.Credentials.Facebook.PASSWORD = base64.decodestring(fbPass)
    	FIIConstants.Credentials.LinkedIn.EMAIL = base64.decodestring(linkedInEmail)
    	FIIConstants.Credentials.LinkedIn.PASSWORD = base64.decodestring(linkedInPass)
    	FIIConstants.Credentials.Google.EMAIL = base64.decodestring(googleEmail)
    	FIIConstants.Credentials.Google.PASSWORD = base64.decodestring(googlePass)
    	
    	self.crawler = Crawler()
    	self.crawlerThread = threading.Thread(name="Crawler",target=self.crawler.Run)
    	self.crawlerThread.start()
    	
    def UpdateConfig(self):
    	fbEmail = self.facebookUserNameTextbox.get()
    	fbPass = self.facebookPasswordTextbox.get()
    	linkedInEmail = self.linkedInUserNameTextbox.get()
    	linkedInPass = self.linkedInPasswordTextbox.get()
    	googleEmail = self.googleUserNameTextbox.get()
    	googlePass = self.googlePasswordTextbox.get()
    	twitterEmail = self.twitterUserNameTextbox.get()
    	twitterPassword = self.twitterPasswordTextbox.get()
    	
    	FIIConstants.Credentials.Facebook.EMAIL = fbEmail
    	FIIConstants.Credentials.Facebook.PASSWORD = fbPass
    	FIIConstants.Credentials.LinkedIn.EMAIL = linkedInEmail
    	FIIConstants.Credentials.LinkedIn.PASSWORD = linkedInPass
    	FIIConstants.Credentials.Google.EMAIL = googleEmail
    	FIIConstants.Credentials.Google.PASSWORD = googlePass
    	FIIConstants.Credentials.Twitter.EMAIL = twitterEmail
    	FIIConstants.Credentials.Twitter.PASSWORD = twitterPassword
    	
    	configValues = {}
    	configValues["FB_EMAIL"] = fbEmail
    	configValues["FB_PASSWORD"] = fbPass
    	configValues["LI_EMAIL"] = linkedInEmail
    	configValues["LI_PASSWORD"] = linkedInPass
    	configValues["GOOGLE_EMAIL"] = googleEmail
    	configValues["GOOGLE_PASSWORD"] = googlePass
    	configValues["TWITTER_EMAIL"] = twitterEmail
    	configValues["TWITTER_PASSWORD"] = twitterPassword
    	FIIConfig().Update(configValues)
    	
    	FII_Logger.LogINFO("Configuration has been updated.")
    	tkMessageBox.showinfo("Update Successful", "Successfully updated configuration. Thanks.")
    	
#    	print "I am here: "+str(FIIConstants.Credentials.Facebook.EMAIL)
        
    def createWidgets(self):
    	
    	self.customFont = tkFont.Font(family="Helvetica", size=12)
    	self.pack(fill=BOTH, expand=1)
    	
    	self.columnconfigure(0, pad=3)
    	self.columnconfigure(1, pad=3)
    	self.columnconfigure(2, pad=3)
    	self.columnconfigure(3, pad=3)
    	
    	self.rowconfigure(0, pad=3)
    	self.rowconfigure(1, pad=8)
    	self.rowconfigure(2, pad=3)
    	self.rowconfigure(3, pad=3)
    	self.rowconfigure(4, pad=3)
    	self.rowconfigure(5, pad=3)
    	self.rowconfigure(6, pad=8)
    	self.rowconfigure(7, pad=0)
    	self.rowconfigure(8, pad=3)
    	self.rowconfigure(9, pad=8)
    	
    	self.facebookCredLabel = Label(self,font=self.customFont)
    	self.facebookCredLabel["text"] = "Facebook Login Credentials"
    	self.facebookCredLabel.grid(row=0,columnspan = 4)
    	
    	self.facebookUserNameLabel = Label(self)
        self.facebookUserNameLabel["text"] = "Facebook Email"
        self.facebookUserNameLabel.grid(row=1,column = 0,pady=10)
#        self.facebookUserNameLabel.pack(side = LEFT,padx=6,pady=2,expand=100)		

        facebookUserNameFromFile = StringVar()
        facebookUserNameFromFile.set(FIIConstants.Credentials.Facebook.EMAIL)
        self.facebookUserNameTextbox = Entry(self,width = 30)
        self.facebookUserNameTextbox["text"] = facebookUserNameFromFile
        self.facebookUserNameTextbox.grid(row=1,column=1,pady=10)
#        self.facebookUserNameTextbox.pack(side= LEFT,padx=6,pady=2,expand=100)
		
        self.facebookPasswordLabel = Label(self)
        self.facebookPasswordLabel["text"] = "Facebook Password"
        self.facebookPasswordLabel.grid(row=1,column=2,pady=10)
#        self.facebookPasswordLabel.pack(side = LEFT,padx=6,pady=2,expand=100)		

        facebookPasswordFromFile = StringVar()
        facebookPasswordFromFile.set(FIIConstants.Credentials.Facebook.PASSWORD)
        self.facebookPasswordTextbox = Entry(self,width = 30,show="*")
        self.facebookPasswordTextbox["text"] = facebookPasswordFromFile
        self.facebookPasswordTextbox.grid(row=1,column=3,pady=10)
        
        self.linkedInCredLabel = Label(self,font=self.customFont)
        self.linkedInCredLabel["text"] = "LinkedIn Login Credentials"
        self.linkedInCredLabel.grid(row=2,columnspan=4)
        
        self.linkedInUserNameLabel = Label(self)
        self.linkedInUserNameLabel["text"] = "LinkedIn Email"
        self.linkedInUserNameLabel.grid(row=3,column=0)
#        self.linkedInUserNameLabel.pack(side = LEFT,padx=6,pady=2,expand=100)
        
        linkedInUserNameFromFile = StringVar()
        linkedInUserNameFromFile.set(FIIConstants.Credentials.LinkedIn.EMAIL)
        self.linkedInUserNameTextbox = Entry(self,width = 30)
        self.linkedInUserNameTextbox["text"] = linkedInUserNameFromFile
        self.linkedInUserNameTextbox.grid(row=3,column=1,pady=10)
#        self.linkedInUserNameTextbox.pack(side= LEFT,padx=6,pady=2,expand=100)
        
        self.linkedInPasswordLabel = Label(self)
        self.linkedInPasswordLabel["text"] = "LinkedIn Password"
        self.linkedInPasswordLabel.grid(row=3,column=2,pady=10)
        
        linkedInPasswordFromFile = StringVar()
        linkedInPasswordFromFile.set(FIIConstants.Credentials.LinkedIn.PASSWORD)
        self.linkedInPasswordTextbox = Entry(self,width = 30,show="*")
        self.linkedInPasswordTextbox["text"] = linkedInPasswordFromFile
        self.linkedInPasswordTextbox.grid(row=3,column=3,pady=10)
        
        self.googleCredLabel = Label(self,font=self.customFont)
        self.googleCredLabel["text"] = "Google Login Credentials"
        self.googleCredLabel.grid(row=4,columnspan=4)
        
        self.googleUserNameLabel = Label(self)
        self.googleUserNameLabel["text"] = "Google Email"
        self.googleUserNameLabel.grid(row=5,column=0)
#        self.linkedInUserNameLabel.pack(side = LEFT,padx=6,pady=2,expand=100)
        
        googleUserNameFromFile = StringVar()
        googleUserNameFromFile.set(FIIConstants.Credentials.Google.EMAIL)
        self.googleUserNameTextbox = Entry(self,width = 30)
        self.googleUserNameTextbox["text"] = googleUserNameFromFile
        self.googleUserNameTextbox.grid(row=5,column=1,pady=10)
#        self.linkedInUserNameTextbox.pack(side= LEFT,padx=6,pady=2,expand=100)
        
        self.googlePasswordLabel = Label(self)
        self.googlePasswordLabel["text"] = "Google Password"
        self.googlePasswordLabel.grid(row=5,column=2,pady=10)
#        self.linkedInPasswordLabel.pack(side = LEFT,padx=6,pady=2,expand=100)
        
        googlePasswordFromFile = StringVar()
        googlePasswordFromFile.set(FIIConstants.Credentials.Google.PASSWORD)
        self.googlePasswordTextbox = Entry(self,width = 30,show="*")
        self.googlePasswordTextbox["text"] = googlePasswordFromFile
        self.googlePasswordTextbox.grid(row=5,column=3,pady=10)
        
        self.twitterCredLabel = Label(self,font=self.customFont)
        self.twitterCredLabel["text"] = "Twitter Login Credentials"
        self.twitterCredLabel.grid(row=6,columnspan = 4)
        
        self.twitterUserNameLabel = Label(self)
        self.twitterUserNameLabel["text"] = "Twitter Email"
        self.twitterUserNameLabel.grid(row=7,column = 0,pady=10)
        
        twitterUserNameFromFile = StringVar()
        twitterUserNameFromFile.set(FIIConstants.Credentials.Twitter.EMAIL)
        self.twitterUserNameTextbox = Entry(self,width = 30)
        self.twitterUserNameTextbox["text"] = twitterUserNameFromFile
        self.twitterUserNameTextbox.grid(row=7,column=1,pady=10)
        
        self.twitterPasswordLabel = Label(self)
        self.twitterPasswordLabel["text"] = "Twitter Password"
        self.twitterPasswordLabel.grid(row=7,column=2,pady=10)
        
        twitterPasswordFromFile = StringVar()
        twitterPasswordFromFile.set(FIIConstants.Credentials.Twitter.PASSWORD)
        self.twitterPasswordTextbox = Entry(self,width = 30,show="*")
        self.twitterPasswordTextbox["text"] = twitterPasswordFromFile
        self.twitterPasswordTextbox.grid(row=7,column=3,pady=10)
        
        self.updateConfigButton = Button(self,width=20)
        self.updateConfigButton["text"] = "Update Configuration"
        self.updateConfigButton["command"] = self.UpdateConfig
        self.updateConfigButton.grid(row=8,column=1,pady=10)
        
        self.start_scraping = Button(self,width=20)
        self.start_scraping["text"] = "Start Scraping"
        self.start_scraping["command"] = self.StartScraping
        self.start_scraping.grid(row=8,column=2,pady=10)
        
        self.statusStartedLabel = Label(self)
        self.statusStartedLabel["text"] = "Program started at "
        self.statusStartedLabel.grid(row=9,column = 0,pady=10)
        
        self.statusLabel = Label(self)
        self.statusLabel["text"] = "Not started yet."
        self.statusLabel.grid(row=9,column = 3,pady=10)
        
    def __init__(self, master=None):
    	""" Initialize the log file directory in globals/FIIConstants.py """
    	logfileName = FIIConstants.LOG_FILE_NAME
    	fileDirectory = os.getcwd()
    	FIIConstants.LOG_FILE_PATH = os.path.join(fileDirectory,logfileName)
    	
    	FIIConstants.CONFIG_FILE_PATH = os.path.join(fileDirectory,"globals")
    	FIIConstants.CONFIG_FILE_PATH = os.path.join(FIIConstants.CONFIG_FILE_PATH,FIIConstants.CONFIG_FILE_NAME)
    	FIIConstants.DIRS.GOOGLE_PLUS_DIR = os.path.join(fileDirectory,"googleplus")
#    	print FIIConstants.DIRS.GOOGLE_PLUS_DIR
    	
    	""" Read Configuration File And Initialize Constant Credentioals For Facebook And LinkedIn """
    	configValues = FIIConfig().Read()
    	
    	fbEmail = configValues.get("FB_EMAIL")
    	fbPass = configValues.get("FB_PASSWORD")
    	linkedInEmail = configValues.get("LI_EMAIL")
    	linkedInPass = configValues.get("LI_PASSWORD")
    	googleEmail = configValues.get("GOOGLE_EMAIL")
    	googlePass = configValues.get("GOOGLE_PASSWORD")
    	twitterEmail = configValues.get("TWITTER_EMAIL")
    	twitterPassword = configValues.get("TWITTER_PASSWORD")
    	
    	if fbEmail is not None:
    		FIIConstants.Credentials.Facebook.EMAIL = base64.decodestring(fbEmail)
    	if fbPass is not None:
    		FIIConstants.Credentials.Facebook.PASSWORD = base64.decodestring(fbPass)
    	if linkedInEmail is not None:
    		FIIConstants.Credentials.LinkedIn.EMAIL = base64.decodestring(linkedInEmail)
    	if linkedInPass is not None:
    		FIIConstants.Credentials.LinkedIn.PASSWORD = base64.decodestring(linkedInPass)
    	if googleEmail is not None:
    		FIIConstants.Credentials.Google.EMAIL = base64.decodestring(googleEmail)
    	if googlePass is not None:
    		FIIConstants.Credentials.Google.PASSWORD = base64.decodestring(googlePass)
    	if twitterEmail is not None:
    		FIIConstants.Credentials.Twitter.EMAIL = base64.decodestring(twitterEmail)
    	if twitterPassword is not None:
    		FIIConstants.Credentials.Twitter.PASSWORD = base64.decodestring(twitterPassword)
    	
#    	""" Creating services """
#    	self.crawlerService = Crawler()
#    	self.uploaderService = FII_Service_Uploader()
#    	
#    	""" Creating threads """
#    	self.crawlerThread = threading.Thread(name="Crawler",target=self.crawlerService.Run) ###Initiate the crawler thread
#    	self.uploaderThread = threading.Thread(name="Uploader",target=self.uploaderService.RunService) ###Initiate the uploader service.
    	
        self.root = master
        Frame.__init__(self, master)
        self.pack(padx=15,pady=15)
        self.createWidgets()
        
    def OnClose(self):
        print "Application Closing..."
        self.root.destroy()

root = Tk()
app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", app.OnClose)
app.master.title("FII BigData")
menubar = Menu(root)
menubar.add_cascade(label="Status")
menubar.add_cascade(label="Configurations")
menubar.add_cascade(label="Help")
root.config(menu=menubar)
app.master.minsize(400,400)
app.mainloop()
root.destroy()