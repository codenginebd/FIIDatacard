import ConfigParser
import base64
from FIIConstants import *

""" This is a configuration file. It stores the Facebook and LinkedIn Credentials as base64 encoded string. """

class FIIConfig:
    def __init__(self):
        print "Config Initializing..."
        self.configParser = ConfigParser.ConfigParser()
        self.FACEBOOK_SECTION_NAME = "FACEBOOK"
        self.LINKEDIN_SECTION_NAME = "LINKEDIN"
        self.GOOGLE_SECTION_NAME = "GOOGLE"
        self.TWITTER_SECTION_NAME = "TWITTER"
    def Update(self,dictionaryValues):
        facebookEmail = base64.b64encode(dictionaryValues.get("FB_EMAIL"))
        facebookPassword = base64.b64encode(dictionaryValues.get("FB_PASSWORD"))
        linkedInEmail = base64.b64encode(dictionaryValues.get("LI_EMAIL"))
        linkedInPassword = base64.b64encode(dictionaryValues.get("LI_PASSWORD"))
        googleEmail = base64.b64encode(dictionaryValues.get("GOOGLE_EMAIL"))
        googlePassword = base64.b64encode(dictionaryValues.get("GOOGLE_PASSWORD"))
        twitterEmail = base64.b64encode(dictionaryValues.get("TWITTER_EMAIL"))
        twitterPassword = base64.b64encode(dictionaryValues.get("TWITTER_PASSWORD"))

        try:
            self.configParser.add_section(self.FACEBOOK_SECTION_NAME)
        except ConfigParser.DuplicateSectionError,err:
            print "Facebook Section already exist. No need to add."
        try:
            self.configParser.add_section(self.LINKEDIN_SECTION_NAME)
        except ConfigParser.DuplicateSectionError,err:
            print "LinkedIn Section already exist. No need to add."
        try:
            self.configParser.add_section(self.GOOGLE_SECTION_NAME)
        except ConfigParser.DuplicateSectionError,err:
            print "Google Section already exist. No need to add."
        try:
            self.configParser.add_section(self.TWITTER_SECTION_NAME)
        except ConfigParser.DuplicateSectionError,err:
            print "Twitter Section already exist. No need to add."
            
        try:
            self.configParser.set(self.FACEBOOK_SECTION_NAME,"EMAIL",facebookEmail)
            self.configParser.set(self.FACEBOOK_SECTION_NAME, "PASSWORD", facebookPassword)
            self.configParser.set(self.LINKEDIN_SECTION_NAME, "EMAIL", linkedInEmail)
            self.configParser.set(self.LINKEDIN_SECTION_NAME, "PASSWORD", linkedInPassword)
            self.configParser.set(self.GOOGLE_SECTION_NAME, "EMAIL", googleEmail)
            self.configParser.set(self.GOOGLE_SECTION_NAME, "PASSWORD", googlePassword)
            self.configParser.set(self.TWITTER_SECTION_NAME, "EMAIL", twitterEmail)
            self.configParser.set(self.TWITTER_SECTION_NAME, "PASSWORD", twitterPassword)
            
            """ Now write the values into the config file. """
            with open(FIIConstants.CONFIG_FILE_PATH, 'wb') as configfile:
                self.configParser.write(configfile)
            
        except ConfigParser.Error,errorMessage:
            print "Error! No section with the name specified. %s" % errorMessage
            
    def Read(self):
        self.configParser.read(FIIConstants.CONFIG_FILE_PATH)
        valuesDictionary = {}
        try:
            valuesDictionary["FB_EMAIL"] = self.configParser.get(self.FACEBOOK_SECTION_NAME, "EMAIL")
            valuesDictionary["FB_PASSWORD"] = self.configParser.get(self.FACEBOOK_SECTION_NAME, "PASSWORD")
            valuesDictionary["LI_EMAIL"] = self.configParser.get(self.LINKEDIN_SECTION_NAME, "EMAIL")
            valuesDictionary["LI_PASSWORD"] = self.configParser.get(self.LINKEDIN_SECTION_NAME, "PASSWORD")
            valuesDictionary["GOOGLE_EMAIL"] = self.configParser.get(self.GOOGLE_SECTION_NAME, "EMAIL")
            valuesDictionary["GOOGLE_PASSWORD"] = self.configParser.get(self.GOOGLE_SECTION_NAME, "PASSWORD")
            valuesDictionary["TWITTER_EMAIL"] = self.configParser.get(self.TWITTER_SECTION_NAME, "EMAIL")
            valuesDictionary["TWITTER_PASSWORD"] = self.configParser.get(self.TWITTER_SECTION_NAME,"PASSWORD")
        except Exception,exp:
            pass
#        print valuesDictionary
        return valuesDictionary
            
#FIIConfig().Update({"FB_EMAIL":"1234","FB_PASSWORD":"1234","LI_EMAIL":"1234","LI_PASSWORD":"lapsso065CommlinkCommlink"})
#FIIConfig().Read()
        