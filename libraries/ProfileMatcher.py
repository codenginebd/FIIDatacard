from fuzzywuzzy import fuzz
import re

class ProfileMatcher:
    def __init__(self):
        pass
    def SimplifyFacebookProfile(self,facebookProfile):
        facebook = {}
        try:
            fbEmail = facebookProfile.get("email")
            if fbEmail is not None:
                facebook["email"] = fbEmail.strip().lower()
            fbFullName = facebookProfile.get("full_name")
            if fbFullName is not None:
                facebook["full_name"] = fbFullName.strip().lower()
            facebookAboutData = None
            if facebookProfile is not None:
                facebookAboutData = facebookProfile.get("about")
            facebookContactInfo,facebookBasicInfo,facebookLivingInfo,facebookWorksAndEducationInfo = None,None,None,None
            if facebookAboutData is not None:
                for eachAboutData in facebookAboutData:
                    if eachAboutData is not None:
                        headerTitle = eachAboutData.get("header_title")
                        if headerTitle is not None:
                            if headerTitle == "Contact Information":
                                facebookContactInfo = eachAboutData.get("data")
                            elif headerTitle == "Basic Information":
                                facebookBasicInfo = eachAboutData.get("data")
                            elif headerTitle == "Living":
                                facebookLivingInfo = eachAboutData.get("data")
                            elif headerTitle == "Work and Education":
                                facebookWorksAndEducationInfo = eachAboutData.get("data")
            
            if facebookContactInfo is not None:
                for eachContactInfo in facebookContactInfo:
                    if eachContactInfo is not None:
                        title = eachContactInfo.get("contact_info_title")
                        if title is not None:
                            data = eachContactInfo.get("contact_info_body")
                            if data is not None and type(data) is str:
                                data = data.replace(r"<","").replace(r">","").strip().lower()
                            if "Facebook" in title:
                                facebook["facebook"] = data
                            elif "Networks" in title:
                                facebook["networks"] = data
                            elif "Email" in title:
                                facebook["emails"] = data
                            elif "Website" in title:
                                facebook["website"] = data
                            elif "Screen Names" in title:
                                screenNamesFacebook = {}
                                if data is not None:
                                    splitedData = data.split(",")
                                    for eachSplitedData in splitedData:
                                        if eachSplitedData is not None:
                                            if eachSplitedData is not None:
                                                match = re.search(r"\((.+?)\)",eachSplitedData)
                                                if match is not None:
                                                    screenNameOp = match.group()
                                                    if screenNameOp is not None:
                                                        screenNameParsed = eachSplitedData.replace(screenNameOp,"")
                                                        if screenNameParsed is not None:
                                                            screenNameParsed = screenNameParsed.replace(r">","")
                                                            screenNameParsed = screenNameParsed.strip()
                                                            screenNameParsed = screenNameParsed.lower()
                                                            if "AIM" in screenNameOp:
                                                                screenNamesFacebook["aim"] = screenNameParsed
                                                            elif "Google Talk" in screenNameOp:
                                                                screenNamesFacebook["google_talk"] = screenNameParsed
                                                            elif "Windows Live Messenger" in screenNameOp:
                                                                screenNamesFacebook["windows_live_messenger"] = screenNameParsed
                                                            elif "Skype" in screenNameOp:
                                                                screenNamesFacebook["skype"] = screenNameParsed
                                                            elif "Yahoo! Messenger" in screenNameOp:
                                                                screenNamesFacebook["yahoo_messenger"] = screenNameParsed
                                                            elif "Gadu-Gadu" in screenNameOp:
                                                                screenNamesFacebook["gadu_gudu"] = screenNameParsed
                                                            elif "ICQ" in screenNameOp:
                                                                screenNamesFacebook["icq"] = screenNameParsed
                                                            elif "QQ" in screenNameOp:
                                                                screenNamesFacebook["qq"] = screenNameParsed
                                                            elif "NateOn" in screenNameOp:
                                                                screenNamesFacebook["nate_on"] = screenNameParsed
                                                            elif "Twitter" in screenNameOp:
                                                                screenNamesFacebook["twitter"] = screenNameParsed
                                                            elif "Hyves" in screenNameOp:
                                                                screenNamesFacebook["hyves"] = screenNameParsed
                                                            elif "Orkut" in screenNameOp:
                                                                screenNamesFacebook["orkut"] = screenNameParsed
                                                            elif "Cyworld" in screenNameOp:
                                                                screenNamesFacebook["cyworld"] = screenNameParsed
                                                            elif "QIP" in screenNameOp:
                                                                screenNamesFacebook["qip"] = screenNameParsed
                                                            elif "Rediff Bol" in screenNameOp:
                                                                screenNamesFacebook["rediff_bol"] = screenNameParsed
                                                            elif "Vkontakte" in screenNameOp:
                                                                screenNamesFacebook["vkontakte"] = screenNameParsed
                                                            elif "eBuddy" in screenNameOp:
                                                                screenNamesFacebook["ebuddy"] = screenNameParsed
                                                            elif "Mail.ru Agent" in screenNameOp:
                                                                screenNamesFacebook["mail_ru_agent"] = screenNameParsed
                                                            elif "Jabber" in screenNameOp:
                                                                screenNamesFacebook["jabber"] = screenNameParsed
                                                            elif "BlackBerry Messenger" in screenNameOp:
                                                                screenNamesFacebook["blackberry_messenger"] = screenNameParsed
                                facebook["screen_names"] = screenNamesFacebook
                            elif "Address" in title:
                                facebook["address"] = data
                            elif "Mobile Phones" in title:
                                facebook["mobile_phones"] = data
            if facebookBasicInfo is not None:
                for eachFacebookBasicInfo in facebookBasicInfo:
                    if eachFacebookBasicInfo is not None:
                        dataTitle = eachFacebookBasicInfo.get("basic_info_data_title")
                        dataContent = eachFacebookBasicInfo.get("basic_info_data_body")
                        if dataTitle is not None and dataContent is not None:
                            dataContent = dataContent.strip().lower()
                            if dataContent != "":
                                if "Birthday" in dataTitle:
                                    facebook["birthday"] = dataContent
                                elif "Gender" in dataTitle:
                                    facebook["gender"] = dataContent
                                elif "Interested In" in dataTitle:
                                    facebook["interested_in"] = dataContent
                                elif "Relationship Status" in dataTitle:
                                    facebook["relationship_status"] = dataContent
                                elif "Languages" in dataTitle:
                                    facebook["languages"] = dataContent
                                elif "Religious Views" in dataTitle:
                                    facebook["religious_views"] = dataContent
            if facebookLivingInfo is not None:
                for eachLivingInfo in facebookLivingInfo:
                    if eachLivingInfo is not None:
                        locationName = eachLivingInfo.get("location_name")
                        locationType = eachLivingInfo.get("location_type")
                        if locationName is not None and locationName != "" and locationType is not None and locationType != "":
                            locationName = locationName.strip().lower()
                            if locationType == "Current City":
                                facebook["current_city"] = locationName
                            elif locationType == "Hometown":
                                facebook["hometown"] = locationName
            if facebookWorksAndEducationInfo is not None:
                for eachFacebookWorksAndEducationInfo in facebookWorksAndEducationInfo:
                    if eachFacebookWorksAndEducationInfo is not None:
                        infoTitle = eachFacebookWorksAndEducationInfo.get("info_title")
                        experiences = eachFacebookWorksAndEducationInfo.get("experiences")
                        if infoTitle is not None:
                            if infoTitle == "High School" and len(experiences) > 0:
                                facebook["high_school"] = experiences
                            elif infoTitle == "College" and len(experiences) > 0:
                                facebook["college"] = experiences
                            elif infoTitle == "Graduate School" and len(experiences) > 0:
                                facebook["graduate_school"] = experiences
        except Exception,exp:
            print str(exp)
        return facebook
    
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
                gPlusChat["home_skype"] = homeSkype.strip().lower()
            homeAim = homeContact.get("AIM")
            if homeAim is not None:
                gPlusChat["home_aim"] = homeAim.strip().lower()
            homeGtalk = homeContact.get("Google Talk")
            if homeGtalk is not None:
                gPlusChat["home_gtalk"] = homeGtalk.strip().lower()
            homeIcq = homeContact.get("ICQ")
            if homeIcq is not None:
                gPlusChat["home_icq"] = homeIcq.strip().lower()
            homeJabber = homeContact.get("Jabber")
            if homeJabber is not None:
                gPlusChat["home_jabber"] = homeJabber.strip().lower()
            homeMsn = homeContact.get("MSN")
            if homeMsn is not None:
                gPlusChat["home_msn"] = homeMsn.strip().lower()
            homeNetMeeting = homeContact.get("Net Meeting")
            if homeNetMeeting is not None:
                gPlusChat["home_net_meeting"] = homeNetMeeting.strip().lower()
            homeQq = homeContact.get("QQ")
            if homeQq is not None:
                gPlusChat["home_qq"] = homeQq.strip().lower()
            homeYahoo = homeContact.get("Yahoo")
            if homeYahoo is not None:
                gPlusChat["home_yahoo"] = homeYahoo.strip().lower()
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
                gPlusChat["work_skype"] = workSkype.strip().lower()
            workAim = workContact.get("AIM")
            if workAim is not None:
                gPlusChat["work_aim"] = workAim.strip().lower()
            workGtalk = workContact.get("Google Talk")
            if workGtalk is not None:
                gPlusChat["work_gtalk"] = workGtalk.strip().lower()
            workIcq = workContact.get("ICQ")
            if workIcq is not None:
                gPlusChat["work_icq"] = workIcq.strip().lower()
            workJabber = workContact.get("Jabber")
            if workJabber is not None:
                gPlusChat["work_jabber"] = workJabber.strip().lower()
            workMsn = workContact.get("MSN")
            if workMsn is not None:
                gPlusChat["work_msn"] = workMsn.strip().lower()
            workNetMeeting = workContact.get("Net Meeting")
            if workNetMeeting is not None:
                gPlusChat["work_net_meeting"] = workNetMeeting.strip().lower()
            workQq = workContact.get("QQ")
            if workQq is not None:
                gPlusChat["work_qq"] = workQq.strip().lower()
            workYahoo = workContact.get("Yahoo")
            if workYahoo is not None:
                gPlusChat["work_yahoo"] = workYahoo.strip().lower()
            
        return (gPlusPhone,gPlusMobile,gPlusPager,gPlusAddress,gPlusChat,gPlusFax)
    
    def SimplifyGooglePlusProfile(self,googlePlusProfile):
        googlePlus = {}
        try:
            gPlusFullName = googlePlusProfile.get("full_name")
            if gPlusFullName is not None:
                googlePlus["full_name"] = gPlusFullName.strip().lower()
            googlePlusContactInfo,googlePlusContactInfoHome,googlePlusContactInfoWork,googlePlusLivingInfo,googlePlusBasicInfo = None,None,None,None,None
            googlePlusEducations,googlePlusWorks = None,None
            googlePlusContactInfo = googlePlusProfile.get("contact_info")
            googlePlusLivingInfo = googlePlusProfile.get("living_info")
            googlePlusBasicInfo = googlePlusProfile.get("basic_info")
            googlePlusEducations = googlePlusProfile.get("educations")
            googlePlusWorks = googlePlusProfile.get("works")
            if googlePlusContactInfo is not None:
                googlePlusContactInfoHome = googlePlusContactInfo.get("home")
                googlePlusContactInfoWork = googlePlusContactInfo.get("work")
                gPlusPhone,gPlusMobile,gPlusPager,gPlusAddress,gPlusChat,gPlusFax = self.SplitGPlusContactInfoData(googlePlusContactInfoHome, googlePlusContactInfoWork)
                emailList = []
                if googlePlusContactInfoHome is not None:
                    homeEmails = googlePlusContactInfoHome.get("Email")
                    if homeEmails is not None and type(homeEmails) is list:
                        for eachHomeEmail in homeEmails:
                            if eachHomeEmail is not None:
                                eachHomeEmail = eachHomeEmail.replace(r">","")
                                eachHomeEmail = eachHomeEmail.replace(r"<","")
                                eachHomeEmail = eachHomeEmail.replace(r"[\\s]+","")
                                emailList.append(eachHomeEmail.strip().lower())
                if googlePlusContactInfoWork is not None:
                    workEmails = googlePlusContactInfoWork.get("Email")
                    if workEmails is not None and type(workEmails) is list:
                        for eachWorkEmail in workEmails:
                            if eachWorkEmail is not None:
                                if not eachWorkEmail in emailList:
                                    emailList.append(eachWorkEmail.strip().lower())
                googlePlus["email"] = emailList
                phonesList = []
                if gPlusPhone.get("home_phone") is not None and gPlusPhone.get("home_phone") != "":
                    phonesList.append(gPlusPhone.get("home_phone"))
                if gPlusPhone.get("work_phone") is not None and gPlusPhone.get("work_phone") != "":
                    phonesList.append(gPlusPhone.get("work_phone"))
                if gPlusMobile.get("home_mobile") is not None and gPlusMobile.get("home_mobile") != "":
                    phonesList.append(gPlusMobile.get("home_mobile"))
                if gPlusMobile.get("work_mobile") is not None and gPlusMobile.get("work_mobile") != "":
                    phonesList.append(gPlusMobile.get("work_mobile"))
                googlePlus["mobile_phones"] = phonesList
                if gPlusAddress.get("home_address") is not None and gPlusAddress.get("home_address") != "":
                    googlePlus["address"] = gPlusAddress.get("home_address").replace(r"<","").replace(r">","").strip().lower()
                googlePlusScreenNames = {}
                if gPlusChat.get("home_skype") is not None and gPlusChat.get("home_skype") != "":
                    googlePlusScreenNames["skype"] = gPlusChat.get("home_skype")
                if gPlusChat.get("home_aim") is not None and gPlusChat.get("home_aim") != "":
                    googlePlusScreenNames["aim"] = gPlusChat.get("home_aim")
                if gPlusChat.get("home_gtalk") is not None and gPlusChat.get("home_gtalk") != "":
                    googlePlusScreenNames["google_talk"] = gPlusChat.get("home_gtalk")
                if gPlusChat.get("home_icq") is not None and gPlusChat.get("home_icq") != "":
                    googlePlusScreenNames["icq"] = gPlusChat.get("home_icq")
                if gPlusChat.get("home_jabber") is not None and gPlusChat.get("home_jabber") != "":
                    googlePlusScreenNames["jabber"] = gPlusChat.get("home_jabber")
                if gPlusChat.get("home_msn") is not None and gPlusChat.get("home_msn") != "":
                    googlePlusScreenNames["msn"] = gPlusChat.get("home_msn")
                if gPlusChat.get("home_net_meeting") is not None and gPlusChat.get("home_net_meeting") != "":
                    googlePlusScreenNames["net_meeting"] = gPlusChat.get("home_net_meeting")
                if gPlusChat.get("home_qq") is not None and gPlusChat.get("home_qq") != "":
                    googlePlusScreenNames["qq"] = gPlusChat.get("home_qq")
                if gPlusChat.get("home_yahoo") is not None and gPlusChat.get("home_yahoo") != "":
                    googlePlusScreenNames["yahoo_messenger"] = gPlusChat.get("home_yahoo")
                googlePlus["screen_names"] = googlePlusScreenNames
            if googlePlusLivingInfo is not None:
                if googlePlusLivingInfo.get("current") is not None:
                    googlePlus["current_city"] = googlePlusLivingInfo.get("current").strip().lower()
                if googlePlusLivingInfo.get("previous") is not None:
                    googlePlus["hometown"] = googlePlusLivingInfo.get("previous").strip().lower()
            if googlePlusBasicInfo is not None:
                if googlePlusBasicInfo.get("Gender") is not None:
                    googlePlus["gender"] = googlePlusBasicInfo.get("Gender").strip().lower()
                if googlePlusBasicInfo.get("Birthday") is not None:
                    googlePlus["birthday"] = googlePlusBasicInfo.get("Birthday").strip().lower()
                if googlePlusBasicInfo.get("Relationship") is not None:
                    googlePlus["relationship_status"] = googlePlusBasicInfo.get("Relationship")
                if googlePlusBasicInfo.get("Other names") is not None:
                    googlePlus["other_names"] = googlePlusBasicInfo.get("Other names")
            googlePlus["educations"] = googlePlusEducations
            googlePlus["works"] = googlePlusWorks
        except Exception,exp:
            print str(exp)
        return googlePlus

    def MatchGooglePlus(self,facebookProfile,googlePlusProfile):
        try:
            if facebookProfile is None or googlePlusProfile is None:
                return False
            """Get the contact info for facebook profile."""
            simplifiedFacebookProfile = self.SimplifyFacebookProfile(facebookProfile)
            simplifiedGooglePlusProfile = self.SimplifyGooglePlusProfile(googlePlusProfile)
            
            """Now calculations begins here."""
            """First match email addresses. If any email is matched then the two profile dictates same."""
            facebookEmailsStr = simplifiedFacebookProfile.get("emails")
            facebookEmails = []
            if facebookEmailsStr is not None:
                facebookEmails = facebookEmailsStr.split(",") ###returns a list of email addresses.
            tempFacebookEmails = []
            for eachFBEmail in facebookEmails:
                if eachFBEmail is not None:
                    while eachFBEmail.find(" ") != -1:
                        eachFBEmail = eachFBEmail.replace(r" ","")
                    eachFBEmail = eachFBEmail.replace(r"<","")
                    eachFBEmail = eachFBEmail.replace(r">","")
                    tempFacebookEmails.append(eachFBEmail)
            facebookEmails = tempFacebookEmails
            if simplifiedFacebookProfile.get("email") is not None:
                if facebookEmails is not None and type(facebookEmails) is list:
                    if not simplifiedFacebookProfile.get("email") in facebookEmails:
                        facebookEmails.append(simplifiedFacebookProfile.get("email"))
                else:
                    facebookEmails = [simplifiedFacebookProfile.get("email")]
            googlePlusEmails = simplifiedGooglePlusProfile.get("email") ###a list of email addresses.
    #        print facebookEmails
    #        print googlePlusEmails
            emailsIntersection = set(facebookEmails) & set(googlePlusEmails)
            if emailsIntersection:
                """Found matches."""
                return True
            facebookScreenNames = simplifiedFacebookProfile.get("screen_names")
            googlePlusScreenNames = simplifiedGooglePlusProfile.get("screen_names")
            if facebookScreenNames is not None and googlePlusScreenNames is not None:
                screennamesIntersection = set(facebookScreenNames.items()) & set(googlePlusScreenNames.items())
                if screennamesIntersection:
                    return True
            """Weight dictionary for different attributes."""
            weights = {"name":0.4,"birthday":0.5,"living_info_current":0.6,"living_info_permanent":0.7,"gender":0.4,"address":0.7}
            newComputedScore = 0.0
            scoreThreshold = 0.7
            new_score = lambda a,b:(2*a*b)/(1+(a*b))
            scoresList = []
            
            fullNameIsFoundInBothProfile = simplifiedFacebookProfile.get("full_name") is not None and simplifiedGooglePlusProfile.get("full_name") is not None and simplifiedFacebookProfile.get("full_name") != "" and simplifiedGooglePlusProfile.get("full_name") != ""
            genderIsFoundInBothProfile = simplifiedFacebookProfile.get("gender") is not None and simplifiedGooglePlusProfile.get("gender") is not None and simplifiedFacebookProfile.get("gender") != "" and simplifiedGooglePlusProfile.get("gender") != ""
            birthdayIsFoundInBothProfile = simplifiedFacebookProfile.get("birthday") is not None and simplifiedGooglePlusProfile.get("birthday") is not None and simplifiedFacebookProfile.get("birthday") != "" and simplifiedGooglePlusProfile.get("birthday") != ""
            currentCityIsFoundInBothProfile = simplifiedFacebookProfile.get("current_city") is not None and simplifiedGooglePlusProfile.get("current_city") is not None and simplifiedFacebookProfile.get("current_city") != "" and simplifiedGooglePlusProfile.get("current_city") != ""
            hometownIsFoundInBothProfile = simplifiedFacebookProfile.get("hometown") is not None and simplifiedGooglePlusProfile.get("hometown") is not None and simplifiedFacebookProfile.get("hometown") != "" and simplifiedGooglePlusProfile.get("homwtown") != ""
            addressIsFoundInBothProfile = simplifiedFacebookProfile.get("address") is not None and simplifiedGooglePlusProfile.get("address") is not None and simplifiedFacebookProfile.get("address") != "" and simplifiedGooglePlusProfile.get("address") != ""
            
            mobilePhonesFacebookStr = simplifiedFacebookProfile.get("mobile_phones")
            mobilePhonesFacebook = []
            if mobilePhonesFacebookStr is not None:
                mobilePhonesFacebook = mobilePhonesFacebookStr.split(",")
            mobilePhonesGooglePlus = simplifiedGooglePlusProfile.get("mobile_phones")
            
            mobileIsFoundInBothProfile = mobilePhonesFacebookStr is not None and mobilePhonesFacebookStr != "" and mobilePhonesGooglePlus is not None and len(mobilePhonesGooglePlus) > 0
            
            if fullNameIsFoundInBothProfile is True and genderIsFoundInBothProfile is True and birthdayIsFoundInBothProfile is True and currentCityIsFoundInBothProfile is True and hometownIsFoundInBothProfile is True and addressIsFoundInBothProfile is True:
                ###Now the calculation begins here.
                nameSimilarityScore = fuzz.partial_token_sort_ratio(simplifiedFacebookProfile.get("full_name"),simplifiedGooglePlusProfile.get("full_name"))
                newComputedScore = new_score(float(nameSimilarityScore)/100,weights.get("name"))
                scoresList.append(newComputedScore)
                
                genderSimilarityScore = fuzz.partial_token_sort_ratio(simplifiedFacebookProfile.get("gender"),simplifiedGooglePlusProfile.get("gender"))
                newComputedScore = new_score(float(genderSimilarityScore)/100,weights.get("gender"))
                scoresList.append(newComputedScore)
                
                birthdaySimilarityScore = fuzz.partial_token_sort_ratio(simplifiedFacebookProfile.get("birthday"),simplifiedGooglePlusProfile.get("birthday"))
                newComputedScore = new_score(float(birthdaySimilarityScore)/100,weights.get("birthday"))
                scoresList.append(newComputedScore)
                
                currentCitySimilarityScore = fuzz.partial_token_sort_ratio(simplifiedFacebookProfile.get("current_city"),simplifiedGooglePlusProfile.get("current_city"))
                newComputedScore = new_score(float(currentCitySimilarityScore)/100,weights.get("living_info_current"))
                scoresList.append(newComputedScore)
                
                homeTownSimiratyScore = fuzz.partial_token_sort_ratio(simplifiedFacebookProfile.get("hometown"),simplifiedGooglePlusProfile.get("hometown"))
                newComputedScore = new_score(float(homeTownSimiratyScore)/100,weights.get("living_info_permanent"))
                scoresList.append(newComputedScore)
                
                addressSimiratyScore = fuzz.partial_token_sort_ratio(simplifiedFacebookProfile.get("address"),simplifiedGooglePlusProfile.get("address"))
                newComputedScore = new_score(float(addressSimiratyScore)/100,weights.get("address"))
                scoresList.append(newComputedScore)
                
                averageScore = 0.0
                
                if len(scoresList) > 0:
                    scoresSum = reduce(lambda a,b:a+b,scoresList)
                    if scoresSum is not None:
                        scoresSum = float(scoresSum)
                        averageScore = scoresSum/len(scoresList)
                
                if averageScore >= scoreThreshold:
                    print averageScore
                    return True
                else:
                    return False
                
            else:
                return False
        except Exception,exp:
            return False
        
    def SimplifyLinkedInProfile(self,linkedInProfile):
        simplifiedLinkedInProfile = {}
        try:
            generalInfo = linkedInProfile.get("general_info")
            if generalInfo is not None:
                if generalInfo.get("full_name") is not None:
                    simplifiedLinkedInProfile["full_name"] = generalInfo.get("full_name")
                if generalInfo.get("heading") is not None:
                    simplifiedLinkedInProfile["heading"] = generalInfo.get("heading")
                if generalInfo.get("location") is not None:
                    simplifiedLinkedInProfile["location"] = generalInfo.get("location")
                if generalInfo.get("industry") is not None:
                    simplifiedLinkedInProfile["industry"] = generalInfo.get("industry")
                if generalInfo.get("past_company") is not None:
                    simplifiedLinkedInProfile["past_company"] = generalInfo.get("past_company")
            worksAndEducations = linkedInProfile.get("works_and_education")
            if worksAndEducations is not None:
                if worksAndEducations.get("working_experience") is not None:
                    simplifiedLinkedInProfile["works"] = worksAndEducations.get("working_experience")
                if worksAndEducations.get("educations") is not None:
                    simplifiedLinkedInProfile["educations"] = worksAndEducations.get("educations")
            contactInfo = linkedInProfile.get("contact_info")
            if contactInfo is not None:
                email = contactInfo.get("email")
                if email is not None and email != "":
                    simplifiedLinkedInProfile["email"] = email.split(",")
                im = contactInfo.get("im")
                if im is not None and im != "":
                    simplifiedLinkedInProfile["im"] = im.split(",")
                phone = contactInfo.get("phone")
                if phone is not None and phone != "":
                    simplifiedLinkedInProfile["phone"] = phone.split(",")
                address = contactInfo.get("address")
                if address is not None and address != "":
                    simplifiedLinkedInProfile["address"] = address
                twitter = []
                twitterDataArray = contactInfo.get("twitter")
                if twitterDataArray is not None:
                    for eachTwitterData in twitterDataArray:
                        if eachTwitterData is not None:
                            title = eachTwitterData.get("title")
                            if title is not None:
                                data = eachTwitterData.get("data")
                                if data is not None:
                                    twitter.append(data)
                if len(twitter) > 0:
                    simplifiedLinkedInProfile["twitter"] = twitter
                websites = []
                websitesDataArray = contactInfo.get("websites")
                if websitesDataArray is not None:
                    for eachWebsite in websitesDataArray:
                        if eachWebsite is not None:
                            data = eachWebsite.get("data")
                            if data is not None:
                                websites.append(data)
                if len(data) > 0:
                    simplifiedLinkedInProfile["websites"] = websites
            personalInfo = linkedInProfile.get("personal_details")
            if personalInfo is not None:
                birthdayInfo = personalInfo.get("birthday")
                if birthdayInfo is not None and birthdayInfo != "":
                    simplifiedLinkedInProfile["birthday"] = birthdayInfo
                maritalStatusInfo = personalInfo.get("marital_status")
                if maritalStatusInfo is not None:
                    simplifiedLinkedInProfile["marital_status"] = maritalStatusInfo
        except Exception,exp:
            pass
        return simplifiedLinkedInProfile
        
    def MatchLinkedInProfile(self,facebookProfile,googlePlusProfile,linkedIn):
        try:
            simplifiedFacebookProfile,simplifiedGooglePlusProfile,simplifiedLinkedInProfile = None,None,None
            if facebookProfile is None and googlePlusProfile is None:
                return False
            if linkedIn is None:
                return False
            if facebookProfile is not None:
                simplifiedFacebookProfile = self.SimplifyFacebookProfile(facebookProfile)
            if googlePlusProfile is not None:
                simplifiedGooglePlusProfile = self.SimplifyGooglePlusProfile(googlePlusProfile)
            simplifiedLinkedInProfile = self.SimplifyLinkedInProfile(linkedIn)
            
            emails = simplifiedLinkedInProfile.get('email')
            
            facebookEmailsStr = simplifiedFacebookProfile.get("emails")
            facebookEmails = []
            if facebookEmailsStr is not None:
                facebookEmails = facebookEmailsStr.split(",") ###returns a list of email addresses.
            tempFacebookEmails = []
            for eachFBEmail in facebookEmails:
                if eachFBEmail is not None:
                    while eachFBEmail.find(" ") != -1:
                        eachFBEmail = eachFBEmail.replace(r" ","")
                    eachFBEmail = eachFBEmail.replace(r"<","")
                    eachFBEmail = eachFBEmail.replace(r">","")
                    tempFacebookEmails.append(eachFBEmail)
            facebookEmails = tempFacebookEmails
            
            if simplifiedFacebookProfile.get("email") is not None:
                if facebookEmails is not None and type(facebookEmails) is list:
                    if not simplifiedFacebookProfile.get("email") in facebookEmails:
                        facebookEmails.append(simplifiedFacebookProfile.get("email"))
                else:
                    facebookEmails = [simplifiedFacebookProfile.get("email")]
            googlePlusEmails = simplifiedGooglePlusProfile.get("email") ###a list of email addresses.
            
        except Exception,exp:
            return False


