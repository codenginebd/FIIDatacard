from Parser import *
import simplejson as json
from bs4 import BeautifulSoup

class GPlusParser(FIIParser):
    def __init__(self):
        print "Google Plus Parser is initializing..."
    def __init__(self,page):
        self.soup = BeautifulSoup(page)
    def ParseExperiences(self):
        experiences = []
        divsWithClasseEmMnd = self.soup.findAll("div", {"class":"eEmMnd"})
        experienceDiv = None
        for eachDiv in divsWithClasseEmMnd:
            titleContainer = eachDiv.find("div",{"class":"ZMDitf"})
            if titleContainer is not None:
                if titleContainer.text == "Work":
                    experienceDiv = eachDiv
                    break
        if experienceDiv is not None:
            contentRows = experienceDiv.findAll("div", {"class":"D0cs5d"})
            for eachRow in contentRows:
                experienceTitleElement = eachRow.find("div",{"class":"cHz88d"})
                experienceBodyElement = eachRow.find("div",{"class":"umCUbe"})
                experienceTitle,experienceBody = "",""
                if experienceTitleElement is not None:
                    experienceTitle = experienceTitleElement.text
                if experienceBodyElement is not None:
                    experienceBody = experienceBodyElement.text
                if experienceTitle != "" and experienceBody != "":
                    if experienceTitle == "Employment":
                        employmentRecordLIs = eachRow.findAll("li",{"class":"nT"})
                        employmentRecords = []
                        for eachLI in employmentRecordLIs:
                            jobTitle,jobPeriod = "",""
                            jobTitleElement = eachLI.find("div",{"class":"CE"})
                            jobPeriodElement = eachLI.find("div",{"class":"EC"})
                            if jobTitleElement is not None:
                                jobTitle = jobTitleElement.text
                            if jobPeriodElement is not None:
                                jobPeriod = jobPeriodElement.text
                            if jobTitle != "" and jobPeriod != "":
                                employmentRecords.append({"title":jobTitle,"period":jobPeriod})
                        experienceBody = employmentRecords
                    experiences.append({"title":experienceTitle,"body":experienceBody})
        return experiences
    
    def ParseLivingInfo(self):
        livingInfo = {}
        livingAreaContent = self.soup.find("div", {"class":"vKm7A"})
        if livingAreaContent is not None:
            livingInfoContentRows = livingAreaContent.findAll("div",{"class":"Du4XP"})
            for eachLivingInfoRow in livingInfoContentRows:
                locationTitle,locationInfo = "",""
                locationTitleElement = eachLivingInfoRow.find("div",{"class":"cHz88d"})
                locationInfoElement = eachLivingInfoRow.find("div",{"class":"umCUbe"})
                if locationTitleElement is not None:
                    locationTitle = locationTitleElement.text
                if locationInfoElement is not None:
                    locationInfo = locationInfoElement.text
                if locationTitle != "" and locationInfo != "":
                    if locationTitle == "Currently":
                        locationTitle = "current"
                    elif locationTitle == "Previously":
                        locationTitle = "previous"
                    livingInfo[locationTitle] = locationInfo
        return livingInfo
    
    def ParseBasicInfo(self):
        basicInfo = {}
        try:
            basicInfoAreaContent = self.soup.find("div",{"class":"xiyRMb"})
            if basicInfoAreaContent is not None:
                basicInfoContentRows = basicInfoAreaContent.findAll("div",{"class":"D0cs5d"})
                for eachRow in basicInfoContentRows:
                    title,data = "",""
                    titleElement = eachRow.find("div",{"class":"WB221b"})
                    dataElement = eachRow.find("div",{"class":"umCUbe"})
                    if titleElement is not None:
                        title = titleElement.text
                    if dataElement is not None:
                        data = dataElement.text
                    if title != "" and data != "":
                        basicInfo[title] = data
        except Exception,exp:
            print str(exp)
        return basicInfo
    
    def ParseEducations(self):
        educations = []
        educationsInfoArea = self.soup.find("div",{"class":"O0fBzf"})
        if educationsInfoArea is not None:
            educationsInfoRowsLIs = educationsInfoArea.findAll("li",{"class":"nT"})
            for eachRowLI in educationsInfoRowsLIs:
                title,period = "",""
                titleElement = eachRowLI.find("div",{"class":"CE"})
                periodElement = eachRowLI.find("div",{"class":"EC"})
                if titleElement is not None:
                    title = titleElement.text
                if periodElement is not None:
                    period = periodElement.text
                if title != "" and period != "":
                    educations.append({"title":title,"info":period})
        return educations
    
    def FindContactInfoData(self,contactDataElement):
        contactInfo = {}
        try:
            if contactDataElement is not None:
                contactDataRows = contactDataElement.findAll("tr")
                for eachContactDataRow in contactDataRows:
                    contactDataTitle,contactData = "",None
                    contactDataTitleElement = eachContactDataRow.find("td",{"class":"GC"})
                    if contactDataTitleElement is not None:
                        contactDataTitle = contactDataTitleElement.text
                        contactDataElement = contactDataTitleElement.nextSibling
                        if contactDataTitle != "":
                            if contactDataTitle == "Email":
                                emailDataLIs = contactDataElement.findAll("li")
                                emailList = []
                                for eachEmailLI in emailDataLIs:
                                    emailData = eachEmailLI.text
                                    if emailData is not None and emailData != "":
                                        emailList.append(emailData)
                                contactData = emailList
                            
                            else:
                                contactData = contactDataElement.text
                            if contactData is not None:
                                contactInfo[contactDataTitle] = contactData
        except Exception,exp:
            pass
        return contactInfo
    
    def ParseContactInfo(self):
        contactInfo = {}
        contactInfoArea = self.soup.find("div",{"class":"cW9Kh"})
        if contactInfoArea is not None:
            contactInfoContents = contactInfoArea.find("div",{"class":"A4Urud"})
            if contactInfoContents is not None:
                contactInfoDataRows = contactInfoContents.findAll("div",{"class":"D0cs5d"})
                for eachDataRow in contactInfoDataRows:
                    dataContactTypeTitle = ""
                    dataContactTypeTitleElement = eachDataRow.find("div",{"class":"cHz88d"})
                    if dataContactTypeTitleElement is not None:
                        dataContactTypeTitle = dataContactTypeTitleElement.text
                    if dataContactTypeTitle != "":
                        contactDataElement = eachDataRow.find("div",{"class":"umCUbe"})
                        info = self.FindContactInfoData(contactDataElement)
                        if len(info) > 0:
                            if dataContactTypeTitle == "Home":
                                contactInfo["home"] = info
                                                
                            elif dataContactTypeTitle == "Work":
                                contactInfo["work"] = info
                            
        return contactInfo
    
    def ParseProfileNetworkLinks(self):
        links = {}
        try:
            networkLinksContainerElement = self.soup.find("div",{"class":"r6Rtbe bdknsb fNFtPe UXKyxb"})
            if networkLinksContainerElement is not None:
                networkLinksAnchorList = networkLinksContainerElement.findAll("a",{"class":"nX url UHHO0c"})
                for eachAnchor in networkLinksAnchorList:
                    networkLink = eachAnchor["href"]
                    if networkLink is not None and networkLink != "":
                        if "youtube" in networkLink:
                            if links.get("youtube") is None:
                                links["youtube"] = [networkLink]
                            else:
                                links.get("youtube").append(networkLink)
                        elif "facebook" in networkLink:
                            if links.get("facebook") is None:
                                links["facebook"] = [networkLink]
                            else:
                                links.get("facebook").append(networkLink)
                        elif "twitter" in networkLink:
                            if links.get("twitter") is None:
                                links["twitter"] = [networkLink]
                            else:
                                links.get("twitter").append(networkLink)
                        else:
                            if links.get("other") is None:
                                links["other"] = [networkLink]
                            else:
                                links.get("other").append(networkLink)
        except Exception,exp:
            pass
        return links
    
    def ParseFullName(self):
        fullName = None
        try:
            fullNameContentElement = self.soup.find("div",{"class":"ukckZb"})
            if fullNameContentElement is not None:
                fullName = fullNameContentElement.text
        except Exception,exp:
            print str(exp)
        return fullName
            
    def ParseProfile(self):
        profile = {}
        profile["full_name"] = self.ParseFullName()
        profile["basic_info"] = self.ParseBasicInfo()
        profile["educations"] = self.ParseEducations()
        profile["works"] = self.ParseExperiences()
        profile["living_info"] = self.ParseLivingInfo()
        profile["contact_info"] = self.ParseContactInfo()
        profile["network_links"] = self.ParseProfileNetworkLinks()
        return profile