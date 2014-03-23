class Merger:
    def __init__(self):
        print "Initializing merger..."
    def SplitGPlusContactInfoData(self,homeContact,workContact):
        """Get all contact infos for home and work."""
        gPlusPhone,gPlusMobile,gPlusPager,gPlusAddress,gPlusChat,gPlusFax = {},{},{},{},{},{}
        
        if homeContact is not None:
            homePhone = homeContact.get("Phone") 
            if homePhone is not None:
                gPlusPhone["home_phone"] = homePhone
            homeMobile = homeContact.get("Mobile")
            if homeMobile is not None:
                gPlusMobile["home_mobile"] = homeMobile
            homePager = homeContact.get("Pager")
            if homePager is not None:
                gPlusPager["home_pager"] = homePager
            homeAddress = homeContact.get("Address")
            if homeAddress is not None:
                gPlusAddress["home_address"] = homeAddress
            homeFax = homeContact.get("Fax")
            if homeFax is not None:
                gPlusFax["home_fax"] = homeFax
            homeSkype = homeContact.get("Skype")
            if homeSkype is not None:
                gPlusChat["home_skype"] = homeSkype
            homeAim = homeContact.get("AIM")
            if homeAim is not None:
                gPlusChat["home_aim"] = homeAim
            homeGtalk = homeContact.get("Google Talk")
            if homeGtalk is not None:
                gPlusChat["home_gtalk"] = homeGtalk
            homeIcq = homeContact.get("ICQ")
            if homeIcq is not None:
                gPlusChat["home_icq"] = homeIcq
            homeJabber = homeContact.get("Jabber")
            if homeJabber is not None:
                gPlusChat["home_jabber"] = homeJabber
            homeMsn = homeContact.get("MSN")
            if homeMsn is not None:
                gPlusChat["home_msn"] = homeMsn
            homeNetMeeting = homeContact.get("Net Meeting")
            if homeNetMeeting is not None:
                gPlusChat["home_net_meeting"] = homeNetMeeting
            homeQq = homeContact.get("QQ")
            if homeQq is not None:
                gPlusChat["home_qq"] = homeQq
            homeYahoo = homeContact.get("Yahoo")
            if homeYahoo is not None:
                gPlusChat["home_yahoo"] = homeYahoo
        if workContact is not None:
            workPhone = workContact.get("Phone") 
            if workPhone is not None:
                gPlusPhone["work_phone"] = workPhone
            workMobile = workContact.get("Mobile")
            if workMobile is not None:
                gPlusMobile["work_mobile"] = workMobile
            workPager = workContact.get("Pager")
            if workPager is not None:
                gPlusPager["work_pager"] = workPager
            workAddress = workContact.get("Address")
            if workAddress is not None:
                gPlusAddress["work_address"] = workAddress
            workFax = workContact.get("Fax")
            if workFax is not None:
                gPlusFax["work_fax"] = workFax
            workSkype = workContact.get("Skype")
            if workSkype is not None:
                gPlusChat["work_skype"] = workSkype
            workAim = workContact.get("AIM")
            if workAim is not None:
                gPlusChat["work_aim"] = workAim
            workGtalk = workContact.get("Google Talk")
            if workGtalk is not None:
                gPlusChat["work_gtalk"] = workGtalk
            workIcq = workContact.get("ICQ")
            if workIcq is not None:
                gPlusChat["work_icq"] = workIcq
            workJabber = workContact.get("Jabber")
            if workJabber is not None:
                gPlusChat["work_jabber"] = workJabber
            workMsn = workContact.get("MSN")
            if workMsn is not None:
                gPlusChat["work_msn"] = workMsn
            workNetMeeting = workContact.get("Net Meeting")
            if workNetMeeting is not None:
                gPlusChat["work_net_meeting"] = workNetMeeting
            workQq = workContact.get("QQ")
            if workQq is not None:
                gPlusChat["work_qq"] = workQq
            workYahoo = workContact.get("Yahoo")
            if workYahoo is not None:
                gPlusChat["work_yahoo"] = workYahoo
            
        return (gPlusPhone,gPlusMobile,gPlusPager,gPlusAddress,gPlusChat,gPlusFax)
        
                    
    def MergeContactInfos(self):
        mergedContactInfo = {}
        try:
            facebookAboutData = None
            if self.facebookProfile is not None:
                facebookAboutData = self.facebookProfile.get("about")
            facebookContactInfo = None
            if facebookAboutData is not None:
                for eachAboutData in facebookAboutData:
                    if eachAboutData is not None:
                        headerTitle = eachAboutData.get("header_title")
                        if headerTitle is not None and headerTitle == "Contact Information":
                            facebookContactInfo = eachAboutData.get("data")
                            break
            linkedInContactInfo = None
            if self.linkedInProfile is not None:
                linkedInContactInfo = self.linkedInProfile.get("contact_info")
            
            googlePlusContactInfo,googlePlusContactInfoHome,googlePlusContactInfoWork = None,None,None
            if self.googleplus is not None:
                googlePlusContactInfo = self.googleplus.get("contact_info")
                if googlePlusContactInfo is not None:
                    googlePlusContactInfoHome = googlePlusContactInfo.get("home")
                    googlePlusContactInfoWork = googlePlusContactInfo.get("work")
                    
            gPlusPhone,gPlusMobile,gPlusPager,gPlusAddress,gPlusChat,gPlusFax = self.SplitGPlusContactInfoData(googlePlusContactInfoHome, googlePlusContactInfoWork)
            ###Merge twitter 
            twitter = []
            if linkedInContactInfo is not None:
                twitterDataArray = linkedInContactInfo.get("twitter")
                if twitterDataArray is not None:
                    for eachTwitterData in twitterDataArray:
                        if eachTwitterData is not None:
                            title = eachTwitterData.get("title")
                            if title is not None:
                                data = eachTwitterData.get("data")
                                if data is not None:
                                    mergedTwitter = {}
                                    mergedTwitter["user_name"] = title
                                    mergedTwitter["profile_link"] = data
                                    twitter.append(mergedTwitter)
                                
            ###Merge facebook
            facebook = ""
            if facebookContactInfo is not None:
                for eachContactInfo in facebookContactInfo:
                    if eachContactInfo is not None:
                        title = eachContactInfo.get("contact_info_title")
                        if title is not None and title == "Facebook":
                            data = eachContactInfo.get("contact_info_body")
                            if data is not None and data != "":
                                facebook = data
                            break
                    
            ###Merge websites
            websites =[]
            if linkedInContactInfo is not None:
                websitesDataArray = linkedInContactInfo.get("websites")
                if websitesDataArray is not None:
                    for eachWebsiteData in websitesDataArray:
                        if eachWebsiteData is not None:
                            title = eachWebsiteData.get("title")
                            if title is not None:
                                data = eachWebsiteData.get("data")
                                if data is not None:
                                    mergedFacebook = {}
                                    mergedFacebook["title"] = title
                                    mergedFacebook["website_link"] = data
                                    websites.append(mergedFacebook)
            ###Merge Address
            address = None
            addressAdded = False
            if len(gPlusAddress) > 0:
                address = gPlusAddress
                addressAdded = True
            if linkedInContactInfo is not None and linkedInContactInfo.get("address") is not None and linkedInContactInfo.get("address") != "" and addressAdded is False:
                address = linkedInContactInfo.get("address")
                addressAdded = True
            if facebookContactInfo is not None and addressAdded is False:
                for eachContactInfo in facebookContactInfo:
                    if eachContactInfo is not None:
                        title = eachContactInfo.get("contact_info_title")
                        if title is not None and title == "Address":
                            data = eachContactInfo.get("contact_info_body")
                            if data is not None and data != "":
                                address = data
                                addressAdded = True
                            break
                    
            ###Merge Phone
            phone = None
            phoneAdded = False
            if linkedInContactInfo is not None and linkedInContactInfo.get("phone") is not None and linkedInContactInfo.get("phone") != "":
                phone = linkedInContactInfo.get("phone")
                phoneAdded = True
            if facebookContactInfo is not None and phoneAdded is False:
                for eachContactInfo in facebookContactInfo:
                    if eachContactInfo is not None:
                        title = eachContactInfo.get("contact_info_title")
                        if title is not None and title == "Mobile Phones":
                            data = eachContactInfo.get("contact_info_body")
                            if data is not None and data != "":
                                phone = data
                                phoneAdded = True
                            break
            if len(gPlusPhone) > 0 and phoneAdded is False:
                phone = gPlusPhone
                    
            ###Merge Mobile.
            mobile = gPlusMobile
                    
            ###Merge Screen Name
            im = None
            imAdded = False
            if len(gPlusChat) > 0:
                im = gPlusChat
                imAdded = True
            if linkedInContactInfo is not None and linkedInContactInfo.get("im") is not None and linkedInContactInfo.get("im") != "" and imAdded is False:
                im = linkedInContactInfo.get("im")
                imAdded = True
            if facebookContactInfo is not None and imAdded is False:
                for eachContactInfo in facebookContactInfo:
                    if eachContactInfo is not None:
                        title = eachContactInfo.get("contact_info_title")
                        if title is not None and title == "Screen Name":
                            data = eachContactInfo.get("contact_info_body")
                            if data is not None and data != "":
                                im = data
                            break
            
            ###Merge Email
            email = None
            if linkedInContactInfo is not None and linkedInContactInfo.get("email") is not None:
                email = linkedInContactInfo.get("email")
            
            if len(twitter) > 0:
                mergedContactInfo["twitter"] = twitter
            if facebook != "":
                mergedContactInfo["facebook"] = facebook
            if len(websites) > 0:
                mergedContactInfo["websites"] = websites
            if address is not None:
                mergedContactInfo["address"] = address
            if phone is not None:
                mergedContactInfo["phone"] = phone
            if im is not None:
                mergedContactInfo["chat"] = im
            if len(mobile) > 0:
                mergedContactInfo["mobile"] = mobile
            if len(gPlusFax) > 0:
                mergedContactInfo["fax"] = gPlusFax
            if len(gPlusPager) > 0:
                mergedContactInfo["pager"] = gPlusPager
            if email is not None:
                mergedContactInfo["other_emails"] = email
        except Exception,exp:
            print "Exception occured in MergeContactInfos in Merger.py %s" % str(exp)
        return mergedContactInfo
    
    def MergeGeneralInfos(self):
        mergedGeneralInfos = {}
        try:
            facebookAboutData = None
            if self.facebookProfile is not None:
                facebookAboutData = self.facebookProfile.get("about")
            facebookBasicInfo = None
            if facebookAboutData is not None:
                for eachAboutData in facebookAboutData:
                    if eachAboutData is not None:
                        headerTitle = eachAboutData.get("header_title")
                        if headerTitle is not None and headerTitle == "Basic Information":
                            facebookBasicInfo = eachAboutData.get("data")
                            break
            linkedInBasicInfo = None
            if self.linkedInProfile is not None:
                linkedInBasicInfo = self.linkedInProfile.get("general_info")
            
            if linkedInBasicInfo is not None:
                if linkedInBasicInfo.get("full_name") is not None and linkedInBasicInfo.get("full_name") != "":
                    mergedGeneralInfos["full_name"] = linkedInBasicInfo.get("full_name")
                if linkedInBasicInfo.get("heading") is not None and linkedInBasicInfo.get("heading") != "":
                    mergedGeneralInfos["current_job_title"] = linkedInBasicInfo.get("heading")
                if linkedInBasicInfo.get("past_company") is not None and linkedInBasicInfo.get("past_company") != "":
                    mergedGeneralInfos["previous_company"] = linkedInBasicInfo.get("past_company")
                if linkedInBasicInfo.get("industry") is not None and linkedInBasicInfo.get("industry") != "":
                    mergedGeneralInfos["current_job_industry"] = linkedInBasicInfo.get("industry")
                if linkedInBasicInfo.get("location") is not None and linkedInBasicInfo.get("location") != "":
                    mergedGeneralInfos["current_job_location"] = linkedInBasicInfo.get("location")
                
            if facebookBasicInfo is not None:
                for eachFacebookBasicInfo in facebookBasicInfo:
                    if eachFacebookBasicInfo is not None:
                        dataTitle = eachFacebookBasicInfo.get("basic_info_data_title")
                        dataContent = eachFacebookBasicInfo.get("basic_info_data_body")
                        if dataTitle is not None and dataContent is not None:
                            if dataContent != "":
                                if dataTitle == "Birthday":
                                    mergedGeneralInfos["birthday"] = dataContent
                                elif dataTitle == "Sex":
                                    mergedGeneralInfos["gender"] = dataContent
                                elif dataTitle == "Interested In":
                                    mergedGeneralInfos["interested_in"] = dataContent
                                elif dataTitle == "Relationship Status":
                                    mergedGeneralInfos["relationship_status"] = dataContent
                                elif dataTitle == "Languages":
                                    mergedGeneralInfos["languages"] = dataContent
                                elif dataTitle == "Religious Views":
                                    mergedGeneralInfos["religious_views"] = dataContent
                                
            if self.googleplus is not None:
                gPlusBasicInfo = self.googleplus.get("basic_info")
                if gPlusBasicInfo is not None:
                    gPlusGender = gPlusBasicInfo.get("Gender")
                    if gPlusGender is not None and mergedGeneralInfos.get("gender") is None:
                        mergedGeneralInfos["gender"] = gPlusGender
                    lookingFor = gPlusBasicInfo.get("Looking for")
                    if lookingFor is not None and mergedGeneralInfos.get("interested_in") is None:
                        mergedGeneralInfos["interested_in"] = lookingFor
                    gPlusBirthday = gPlusBasicInfo.get("Birthday")
                    if gPlusBirthday is not None and mergedGeneralInfos.get("birthday") is None:
                        mergedGeneralInfos["birthday"] = gPlusBirthday
                    relationshipStatus = gPlusBasicInfo.get("Relationship")
                    if relationshipStatus is not None and mergedGeneralInfos.get("relationship_status") is None:
                        mergedGeneralInfos["relationship_status"] = relationshipStatus
                    otherNames = gPlusBasicInfo.get("Other names")
                    if otherNames is not None:
                        mergedGeneralInfos["other_names"] = otherNames
        except Exception,exp:
            print "Exception occured inside MergedGeneralInfos() method in Merger.py %s" % str(exp)
        return mergedGeneralInfos
    
    def MergeEducation(self):
        mergedEducation = {}
        try:
            facebookAboutData = None
            if self.facebookProfile is not None:
                facebookAboutData = self.facebookProfile.get("about")
            facebookWorksAndEducationInfo = None
            if facebookAboutData is not None:
                for eachAboutData in facebookAboutData:
                    if eachAboutData is not None:
                        headerTitle = eachAboutData.get("header_title")
                        if headerTitle is not None and headerTitle == "Work and Education":
                            facebookWorksAndEducationInfo = eachAboutData.get("data")
                            break
            linkedInEducation = None
            linkedInWorksAndEducationInfo = None
            if self.linkedInProfile is not None:
                linkedInWorksAndEducationInfo = self.linkedInProfile.get("works_and_education")
            if linkedInWorksAndEducationInfo is not None:
                linkedInEducation = linkedInWorksAndEducationInfo.get("educations")
            if facebookWorksAndEducationInfo is not None:
                for eachFacebookWorksAndEducationInfo in facebookWorksAndEducationInfo:
                    if eachFacebookWorksAndEducationInfo is not None:
                        infoTitle = eachFacebookWorksAndEducationInfo.get("info_title")
                        experiences = eachFacebookWorksAndEducationInfo.get("experiences")
                        if infoTitle is not None:
                            if infoTitle == "High School" and len(experiences) > 0:
                                mergedEducation["high_school"] = experiences
                            elif infoTitle == "College" and len(experiences) > 0:
                                mergedEducation["college"] = experiences
                            elif infoTitle == "Graduate School" and len(experiences) > 0:
                                mergedEducation["graduate_school"] = experiences
            else:
                if linkedInEducation is not None and len(linkedInEducation) > 0:
                    mergedEducation["schools"] = linkedInEducation
        except Exception,exp:
            print "Exception occured in MergeEducation method in Merger.py %s"%str(exp)
        
        return mergedEducation
    
    def MergeExperiences(self):
        mergedExperiences = None
        try:
            facebookAboutData = None
            if self.facebookProfile is not None:
                facebookAboutData = self.facebookProfile.get("about")
            facebookWorksAndEducationInfo = None
            if facebookAboutData is not None:
                for eachAboutData in facebookAboutData:
                    if eachAboutData is not None:
                        headerTitle = eachAboutData.get("header_title")
                        if headerTitle is not None and headerTitle == "Work and Education":
                            facebookWorksAndEducationInfo = eachAboutData.get("data")
                            break
            linkedInExperiences = None
            linkedInWorksAndEducationInfo = None
            if self.linkedInProfile is not None:
                linkedInWorksAndEducationInfo = self.linkedInProfile.get("works_and_education")
            if linkedInWorksAndEducationInfo is not None:
                linkedInExperiences = linkedInWorksAndEducationInfo.get("working_experience")
            if linkedInExperiences is not None and len(linkedInExperiences) > 0:
                mergedExperiences = linkedInExperiences
            else:
                if facebookWorksAndEducationInfo is not None:
                    for eachFacebookWorksAndEducationInfo in facebookWorksAndEducationInfo:
                        if eachFacebookWorksAndEducationInfo is not None:
                            infoTitle = eachFacebookWorksAndEducationInfo.get("info_title")
                            experiences = eachFacebookWorksAndEducationInfo.get("experiences")
                            if infoTitle is not None:
                                if infoTitle == "Employers" and len(experiences) > 0:
                                    mergedExperiences = experiences
                                    break
        except Exception,exp:
            print "Exception occured in MergeExperiences method in Merger.py %s"%str(exp)
                        
        return mergedExperiences 
      
    def MergeLivingInfo(self):
        mergedLivingInfo = {}
        try:
            facebookAboutData = None
            if self.facebookProfile is not None:
                facebookAboutData = self.facebookProfile.get("about")
            facebookLivingInfo = None
            if facebookAboutData is not None:
                for eachAboutData in facebookAboutData:
                    if eachAboutData is not None:
                        headerTitle = eachAboutData.get("header_title")
                        if headerTitle is not None and headerTitle == "Living":
                            facebookLivingInfo = eachAboutData.get("data")
                            break
            if facebookLivingInfo is not None:
                for eachLivingInfo in facebookLivingInfo:
                    if eachLivingInfo is not None:
                        locationName = eachLivingInfo.get("location_name")
                        locationType = eachLivingInfo.get("location_type")
                        if locationName is not None and locationName != "" and locationType is not None and locationType != "":
                            mergedLivingInfo[locationType] = locationName
            if self.googleplus is not None:
                gPlusLivingInfo = self.googleplus.get("living_info")
                if gPlusLivingInfo is not None:
                    gPlusCurrentLivingInfo = gPlusLivingInfo.get("current")
                    if gPlusCurrentLivingInfo is not None and mergedLivingInfo.get("Current City") is None:
                        mergedLivingInfo["Current City"] = gPlusCurrentLivingInfo
                    gPlusHomeLivingInfo = gPlusLivingInfo.get("previous")
                    if gPlusHomeLivingInfo is not None and mergedLivingInfo.get("Hometown") is None:
                        mergedLivingInfo["Hometown"] = gPlusHomeLivingInfo
        except Exception,exp:
            print "Exception occured inside MergeLivingInfo method in Merger.py %s" % str(exp)
                    
        return mergedLivingInfo
    
    def MergeUserLikes(self):
        mergedLikes = None
        try:
            facebookFavoritesData = None
            if self.facebookProfile is not None:
                facebookFavoritesData = self.facebookProfile.get("favorites")
            if facebookFavoritesData is not None:
                mergedLikes = facebookFavoritesData.get("user_likes")
        except Exception,exp:
            print "Exception occured inside MergeUserLikes method in Merger.py %s"%str(exp)
        return mergedLikes
    
    def MergeUserFavorites(self):
        mergedFavorites = None
        try:
            facebookFavoritesData = None
            if self.facebookProfile is not None:
                facebookFavoritesData = self.facebookProfile.get("favorites")
            if facebookFavoritesData is not None:
                mergedFavorites = facebookFavoritesData.get("user_favorites")
        except Exception,exp:
            print "Exception occured inside MergeUserFavorites method in Merger.py %s"%str(exp)
        return mergedFavorites
    
    def MergeInterests(self):
        mergedInterests = None
        try:
            if self.linkedInProfile is not None:
                mergedInterests = self.linkedInProfile.get("interests")
        except Exception,exp:
            print "Exception occured inside MergeInterests method in Merger.py %s"%str(exp)
        return mergedInterests
    
    def MergeCertifications(self):
        mergedCertifications = None
        try:
            if self.linkedInProfile is not None:
                mergedCertifications = self.linkedInProfile.get("certifications")
        except Exception,exp:
            print "Exception occured inside MergeCertifications method in Merger.py %s"%str(exp)
        return mergedCertifications
    
    def MergeSkillsAndExpertise(self):
        mergedSkillsAndExpertise = None
        try:
            if self.linkedInProfile is not None:
                mergedSkillsAndExpertise = self.linkedInProfile.get("skills_and_expertise")
        except Exception,exp:
            print "Exception occured inside MergeSkillsAndExpertise method in Merger.py %s"%str(exp)
        return mergedSkillsAndExpertise
    
    def MergeHonoursAndAwards(self):
        mergedHonoursAndAwards = None
        try:
            if self.linkedInProfile is not None:
                mergedHonoursAndAwards = self.linkedInProfile.get("honours_and_awards")
        except Exception,exp:
            print "Exception occured inside MergeHonoursAndAwards method in Merger.py %s"%str(exp)
        return mergedHonoursAndAwards
    
    def AddTwitterProfile(self,mergedProfile):
        modifiedProfile = mergedProfile
        if self.twitterProfile is not None:
            if mergedProfile is not None:
                modifiedProfile = dict(mergedProfile.items()+self.twitterProfile.items())
        return modifiedProfile
    
    def AddKLoutProfile(self,mergedProfile):
        modifiedProfile = mergedProfile
        if self.kloutProfile is not None:
            if mergedProfile is not None:
                modifiedProfile = dict(mergedProfile.items()+self.kloutProfile.items())
        return modifiedProfile
    
    def AddNetworksLinksFromGooglePlus(self,mergedProfile):
        modifiedProfile = mergedProfile
        if self.googleplus is not None:
            if mergedProfile is not None:
                networkLinksGooglePlus = self.googleplus.get("network_links")
                if networkLinksGooglePlus is not None and type(networkLinksGooglePlus) is dict:
                    modifiedProfile = dict(mergedProfile.items()+networkLinksGooglePlus.items())
        return modifiedProfile
                     
    def Merge(self,facebook,linkedin,googleplus,twitter,klout):
        self.facebookProfile = facebook
        self.linkedInProfile = linkedin
        self.googleplus = googleplus
        self.twitterProfile = twitter
        self.kloutProfile = klout
        completeProfile = {}
        try:
            completeProfile["email"] = self.facebookProfile.get("email")
            completeProfile["general_info"] = self.MergeGeneralInfos()
            completeProfile["contact_info"] = self.MergeContactInfos()
            completeProfile["education"] = self.MergeEducation()
            completeProfile["experiences"] = self.MergeExperiences()
            completeProfile["living_info"] = self.MergeLivingInfo()
            completeProfile["likes"] = self.MergeUserLikes()
            completeProfile["favorites"] = self.MergeUserFavorites()
            completeProfile["interests"] = self.MergeInterests()
            completeProfile["certifications"] = self.MergeCertifications()
            completeProfile["skills_and_expertise"] = self.MergeSkillsAndExpertise()
            completeProfile["honours_and_awards"] = self.MergeHonoursAndAwards()
            completeProfile = self.AddTwitterProfile(completeProfile)
            completeProfile = self.AddKLoutProfile(completeProfile)
            completeProfile = self.AddNetworksLinksFromGooglePlus(completeProfile)
        except Exception,exp:
            pass
        return completeProfile
        