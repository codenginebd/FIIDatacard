import re
from Parser import *
import simplejson as json
from Lib import *
class LinkedInParser(FIIParser):
	def __init__(self):
		print "Parser is initializing..."
		super(FIIParser,self).__init__()
	def ParseAccessCode(self,pageSource):
		accessCode = ""
		accessCodeSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]+class=[\'\"]?access-code(.+?)</div>")
		if accessCodeSource is not None:
			accessCode = super(LinkedInParser,self).ParseAndReplace(accessCodeSource,r"<(.+?)>","")
		return accessCode
	def CountTotalResultsSearch(self,response):
		jsonResponse = json.loads(response)
		total = 0
		try:
			if jsonResponse.get("people") is not None:
				peoplePart = jsonResponse.get("people")
				if peoplePart.get("_total") is not None:
					total = peoplePart.get("_total")
		except Exception,e:
			print e
		return total
	def ParseStart(self,response):
		jsonResponse = json.loads(response)
		start = 0
		try:
			if jsonResponse.get("people") is not None:
				peoplePart = jsonResponse.get("people")
				if peoplePart.get("_start") is not None:
					start = peoplePart.get("_start")
		except Exception,e:
			print e
		return start
	def ParseProfileLinks(self,response):
		jsonResponse = json.loads(response)
		profileLinks = []
		try:
			if jsonResponse.get("people") is not None:
				peoplePart = jsonResponse.get("people")
				if peoplePart.get("values") is not None:
					searchValues = peoplePart.get("values")
					for eachSearchValue in searchValues:
						if eachSearchValue.get("siteStandardProfileRequest") is not None:
							apiStandardProfileRequest = eachSearchValue.get("siteStandardProfileRequest")
							if apiStandardProfileRequest.get("url") is not None:
								profileUrl = apiStandardProfileRequest.get("url")
								profileLinks.append(profileUrl)				
		except Exception,e:
			pass
		return profileLinks
	def ParseFullName(self,pageSource):
		fullName = ""
		try:
			fullNameSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<span[\s]+class=[\'\"]?full-name(.+?)</span>")
			if fullNameSource is not None:
				fullName = super(LinkedInParser,self).ParseAndReplace(fullNameSource,r"<(.+?)>","")
		except Exception,exp:
			pass
		return fullName
	def ParseHeading(self,pageSource):
		heading = ""
		try:
			headingSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]+id=[\'\"]?headline(.+?)</div>")
			if headingSource is not None:
				headingSource = super(LinkedInParser,self).ParseSingle(headingSource,r"<p(.+?)</p>")
				if headingSource is not None:
					heading = super(LinkedInParser,self).ParseAndReplace(headingSource,r"<(.+?)>","")
		except Exception,exp:
			pass
		return heading
	def ParseLocation(self,pageSource):
		location = ""
		try:
			locationSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<span[\s]+class=[\'\"]?locality(.+?)</span>")
			if locationSource is not None:
				location = super(LinkedInParser,self).ParseAndReplace(locationSource,r"<(.+?)>","")
		except Exception,exp:
			pass
		return location
	def ParseIndustry(self,pageSource):
		industry = ""
		try:
			industrySource = super(LinkedInParser,self).ParseSingle(pageSource,r"<dd[\s]+class=[\'\"]?industry(.+?)</dd>")
			if industrySource is not None:
				industry = super(LinkedInParser,self).ParseAndReplace(industrySource,r"<(.+?)>","")
		except Exception,exp:
			pass
		return industry
	def ParseOverviewPast(self,pageSource):
		pastWorks = ""
		try:
			overviewPastSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<tr[\s]+id=[\'\"]?overview-summary-past(.+?)</tr>")
			if overviewPastSource is not None:
				overviewPastSourceLIs =  super(LinkedInParser,self).Parse(overviewPastSource,r"<li>(.+?)</li>")
				for eachLI in overviewPastSourceLIs:
					if eachLI is not None:
						tempPastWorks = super(LinkedInParser,self).ParseAndReplace(eachLI,r"<(.+?)>","") 
						pastWorks += tempPastWorks + ";"
			if pastWorks != "":
				pastWorks = pastWorks[:-1]
		except Exception,exp:
			pass
		return pastWorks
	def ParseGeneralInfo(self,pageSource):
		fullName = self.ParseFullName(pageSource)
		heading = self.ParseHeading(pageSource)
		location = self.ParseLocation(pageSource)
		industry = self.ParseIndustry(pageSource)
		overviewPast = self.ParseOverviewPast(pageSource)
		generalInfo = {}
		if fullName != "":
			generalInfo["full_name"] = fullName
		if heading != "":
			generalInfo["heading"] = heading
		if location != "":
			generalInfo["location"] = location
		if industry != "":
			generalInfo["industry"] = industry
		if overviewPast != "":
			generalInfo["past_company"] = overviewPast 
		return generalInfo
	def ParseExperienceHeading(self,pageSource):
		heading = ""
		headingSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<h4>(.+?)</h4>")
		if headingSource is not None:
			heading = super(LinkedInParser,self).ParseAndReplace(headingSource,r"<(.+?)>","")
		return heading
	def ParseCompanyName(self,pageSource):
		companyName = ""
		companyNameSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<h5>(.+?)</h5>")
		if companyNameSource is not None:
			companyName = super(LinkedInParser,self).ParseAndReplace(companyNameSource,r"<(.+?)>","")
		return companyName
	def ParseExperienceTime(self,pageSource):
		experienceTime = ""
		experienceTimeSources = super(LinkedInParser,self).Parse(pageSource,r"<time(.+?)</time>")
		for eachTimeSource in experienceTimeSources:
			 eachTime = super(LinkedInParser,self).ParseAndReplace(eachTimeSource,r"(.+?)>","")
			 experienceTime += eachTime
		return experienceTime
	def ParseExperiences(self,pageSource):
		experiences = []
		workingExperiencesSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]+id=[\'\"]?background-experience(.+?)</div></div></div></div><script")
		if workingExperiencesSource is not None:
			workingExperiencesSourceList = super(LinkedInParser,self).Parse(workingExperiencesSource,r"<div[\s]+id=[\'\"]?experience(.+?)</div></div>")
			for eachworkingExperiencePart in workingExperiencesSourceList:
				eachExperience = {}
				heading = self.ParseExperienceHeading(eachworkingExperiencePart)
				if heading != "":
					eachExperience["title"] = heading
				companyName = self.ParseCompanyName(eachworkingExperiencePart)
				if companyName != "":
					eachExperience["company_name"] = companyName
				experienceTime = self.ParseExperienceTime(eachworkingExperiencePart)
				if experienceTime != "":
					eachExperience["time"] = experienceTime
				experiences.append(eachExperience)
		return experiences
	def ParseEducationHeading(self,pageSource):
		heading = ""
		headingSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<h4(.+?)</h4>")
		if headingSource is not None:
			heading = super(LinkedInParser,self).ParseAndReplace(headingSource,r"<(.+?)>","")
		return heading
	def ParseEducationDegreeAndCourses(self,pageSource):
		degreeAndCourses = ""
		degreeAndCoursesSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<h5>(.+?)</h5>")
		if degreeAndCoursesSource is not None:
			degreeAndCourses = super(LinkedInParser,self).ParseAndReplace(degreeAndCoursesSource,r"<(.+?)>","")
		return degreeAndCourses
	def ParseEducationDate(self,pageSource):
		educationTime = ""
		educationDateSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<span[\s]+class=[\'\"]?education-date(.+?)</span>")
		if educationDateSource is not None:
			educationTime = super(LinkedInParser,self).ParseAndReplace(educationDateSource,r"<(.+?)>","")
		return educationTime
	def ParseEducationActivities(self,pageSource):
		#educationActivitiesEntity = None
		educationActivities = []
		educationActivitiesSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<p[\s]+class=[\'\"]?activities(.+?)</p>")
		if educationActivitiesSource is not None:
			educationActivitiesAll = super(LinkedInParser,self).Parse(educationActivitiesSource,r"<a(.+?)</a>")
			for eachActivity in educationActivitiesAll:
				eachActivityTemp = super(LinkedInParser,self).ParseAndReplace(eachActivity,r"(.+?)>","")
				if eachActivityTemp is not None or eachActivityTemp != "":
					educationActivities.append(eachActivityTemp)
			#educationActivitiesEntity["header_title"] = "Activities And Societies"
			#educationActivitiesEntity["data"] = educationActivities
		return educationActivities
	def ParseEducations(self,pageSource):
		educations = []
		educationsSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]+id=[\'\"]?background-education(.+?)</div></div></div></div>")
		if educationsSource is not None:
			educationSources = super(LinkedInParser,self).Parse(pageSource,r"<div[\s]+id=[\'\"]?education(.+?)</div></div></div>")
			for eachEducationSource in educationSources:
				educationEntity = {}
				schoolName = self.ParseEducationHeading(eachEducationSource)
				if schoolName != "":
					educationEntity["school_name"] = schoolName
				degreeAndCourses = self.ParseEducationDegreeAndCourses(eachEducationSource)
				if degreeAndCourses != "":
					educationEntity["courses_and_degree"] = degreeAndCourses
				time = self.ParseEducationDate(eachEducationSource)
				if time != "":
					educationEntity["date"] = time
				activities = self.ParseEducationActivities(eachEducationSource)
				educationEntity["activities"] = activities
				educations.append(educationEntity)
		return educations 
			
	def ParseExperiencesAndEducations(self,pageSource):
		experienceAndEducations = {}
		experiences = self.ParseExperiences(pageSource)
		experienceAndEducations["working_experience"] = experiences
		educations = self.ParseEducations(pageSource)
		experienceAndEducations["educations"] = educations
		return experienceAndEducations
	def ParseAdditionalInfoHeading(self,pageSource):
		heading = ""
		headingSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<h4>(.+?)</h4>")
		if headingSource is not None:
			heading = super(LinkedInParser,self).ParseAndReplace(headingSource,r"<(.+?)>","")
		return heading
	def ParsePersonalInfoHeading(self,pageSource):
		heading = ""
		headingSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<th(.+?)</th>")
		if headingSource is not None:
			heading = super(LinkedInParser,self).ParseAndReplace(headingSource,r"<(.+?)>","")
		return heading
	def ParsePersonalInfoContent(self,pageSource):
		content = ""
		contentSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<td>(.+?)</td>")
		if contentSource is not None:
			content = super(LinkedInParser,self).ParseAndReplace(contentSource,r"<(.+?)>","")
		return content
	def ParseAdditionalInfoContents(self,title,pageSource):
		utility = LIUtility()
		if title == "Interests":
			additionalInfoContents = []
			additionalInfoContentsSource = super(LinkedInParser,self).Parse(pageSource,r"<li>(.+?)</li>")
			for eachAdditionalInfoContentsSource in additionalInfoContentsSource:
				additionalInfoContent = super(LinkedInParser,self).ParseAndReplace(eachAdditionalInfoContentsSource,r"<(.+?)>","")
				additionalInfoContents.append(additionalInfoContent)
			return additionalInfoContents
		elif title == "Personal Details":
			additionalInfoContents = {}
			additionalInfoContentsSource = super(LinkedInParser,self).Parse(pageSource,r"<tr>(.+?)</tr>")
			for eachAdditionalInfoContentsSource in additionalInfoContentsSource:
				heading = self.ParsePersonalInfoHeading(eachAdditionalInfoContentsSource)
				variableFormattedHeading = utility.MakeVariableFormattedNameFromString(heading)
				content = self.ParsePersonalInfoContent(eachAdditionalInfoContentsSource)
				if heading != "" and content != "":
					if additionalInfoContents.has_key(variableFormattedHeading) is False:
						additionalInfoContents[variableFormattedHeading] = content
			return additionalInfoContents
		elif title == "Advice for Contacting Andrew":
			additionalInfoContents = ""
			additionalInfoContentsSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<p(.+?)</p>")
			if additionalInfoContentsSource is not None:
				additionalInfoContents = super(LinkedInParser,self).ParseAndReplace(additionalInfoContentsSource,r"<(.+?)>","")
			return additionalInfoContents
		else:
			return None
	def ParseAdditionalInfo(self,pageSource):
		additionalInfoList = {}
		utility = LIUtility()
		additionalInfoSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]+id=[\'\"]?background-additional-info(.+?)</div></div>")
		if additionalInfoSource is not None:
			additionalInfos = super(LinkedInParser,self).Parse(additionalInfoSource,r"<li[\s]+id=(.+?)[(</table>)(</div>)]</li>")
			for eachAdditionalInfo in additionalInfos:
				title = self.ParseAdditionalInfoHeading(eachAdditionalInfo)
				contents = self.ParseAdditionalInfoContents(title,eachAdditionalInfo)
				variableFormattedTitle = utility.MakeVariableFormattedNameFromString(title)
				if title != "" and contents is not None and additionalInfoList.has_key(variableFormattedTitle) is False:
					additionalInfoList[variableFormattedTitle] = contents
		return additionalInfoList
	def ParseOnlineContactInfoTitle(self,pageSource):
		title = ""
		titleSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<th>(.+?)</th>")
		if titleSource is not None:
			title = super(LinkedInParser,self).ParseAndReplace(titleSource,r"<(.+?)>","")
		return title
	def ParseOnlineContactInfo(self,pageSource):
		onlineContactInfoSingle = {}
		utility = LIUtility()
		onlineContactInfoSectionSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<table[\s]+summary=[\'\"]?Online(.+?)</table>")
		if onlineContactInfoSectionSource is not None:
			onlineContactInfoRows = super(LinkedInParser,self).Parse(onlineContactInfoSectionSource,r"<tr>(.+?)</tr>")
			for eachOnlineContactInfoRow in onlineContactInfoRows:
				title = self.ParseOnlineContactInfoTitle(eachOnlineContactInfoRow)
				contents = ""
				onlineContactInfoContactLIs = super(LinkedInParser,self).Parse(eachOnlineContactInfoRow,r"<li>(.+?)</li>")
				for eachOnlineContactInfoContactLI in onlineContactInfoContactLIs:
					contentTemp = super(LinkedInParser,self).ParseAndReplace(eachOnlineContactInfoContactLI,r"<(.+?)>","")
					contents += (contentTemp+",")
				if contents!= "":
					contents = contents[:-1]
				if title != "" and contents != "":
					variableFormattedTitle = utility.MakeVariableFormattedNameFromString(title)
					if onlineContactInfoSingle.has_key(variableFormattedTitle) is False:
						onlineContactInfoSingle[variableFormattedTitle] = contents
		return onlineContactInfoSingle
	
	def ParseOfflineContactInfoTitle(self,pageSource):
		title = ""
		titleSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<th>(.+?)</th>")
		if titleSource is not None:
			title = super(LinkedInParser,self).ParseAndReplace(titleSource,r"<(.+?)>","")
		return title
	def ParseOfflineContactInfo(self,pageSource):
		offlineContactEntity = {}
		utility = LIUtility()
		offlineContactInfoSectionSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<table[\s]+summary=[\'\"]?Contact(.+?)</table>")
		if offlineContactInfoSectionSource is not None:
			offlineContactInfoSectionRows = super(LinkedInParser,self).Parse(offlineContactInfoSectionSource,r"<tr>(.+?)</tr>")
			for eachOfflineContactInfoSectionRow in offlineContactInfoSectionRows:
				title = self.ParseOfflineContactInfoTitle(eachOfflineContactInfoSectionRow)
				contents = ""
				eachOfflineContactInfoSectionRowLIs = super(LinkedInParser,self).Parse(eachOfflineContactInfoSectionRow,r"<li>(.+?)</li>")
				for eachOfflineContactInfoLI in eachOfflineContactInfoSectionRowLIs:
					contentTemp = super(LinkedInParser,self).ParseAndReplace(eachOfflineContactInfoLI,r"<(.+?)>","")
					contents += (contentTemp+",")
				if contents != "":
					contents = contents[:-1]
				if title != "" and contents != "":
					variableFormattedTitle = utility.MakeVariableFormattedNameFromString(title)
					if offlineContactEntity.has_key(variableFormattedTitle) is False:
						offlineContactEntity[variableFormattedTitle] = contents #contentsofflineContactInfos.append(offlineContactEntity)
		return offlineContactEntity
	def ParseInternetPresenceInfoTitle(self,pageSource):
		title = ""
		titleSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<th>(.+?)</th>")
		if titleSource is not None:
			title = super(LinkedInParser,self).ParseAndReplace(titleSource,r"<(.+?)>","")
		return title
		
	def ParseInternetPresenceInfo(self,pageSource):
		internetPresenceInfos = {}
		utility = LIUtility()
		internetPresenceInfoSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<table[\s]+summary=[\'\"]?Internet(.+?)</table>")
		if internetPresenceInfoSource is not None:
			internetPresenceInfoSourceRows = super(LinkedInParser,self).Parse(internetPresenceInfoSource,r"<tr(.+?)</tr>")
			for eachInternetPresenceInfoSourceRow in internetPresenceInfoSourceRows:
				title = self.ParseInternetPresenceInfoTitle(eachInternetPresenceInfoSourceRow)
				contents = []
				eachInternetPresenceInfoSourceRowLIs = super(LinkedInParser,self).Parse(eachInternetPresenceInfoSourceRow,r"<li>(.+?)</li>")
				for eachInternetPresenceInfoSourceRowLI in eachInternetPresenceInfoSourceRowLIs:
					heading = super(LinkedInParser,self).ParseAndReplace(eachInternetPresenceInfoSourceRowLI,r"<(.+?)>","")
					urlSource = super(LinkedInParser,self).ParseSingle(eachInternetPresenceInfoSourceRowLI,r"url=(.+?)\"")
					urlSource = super(LinkedInParser,self).ParseAndReplace(urlSource,r"url=","")
					urlSource = super(LinkedInParser,self).ParseAndReplace(urlSource,r"&amp;urlhash(.+)","")
					urlLink = utility.EscapeURL(urlSource)
					if heading != "" and urlLink != "":
						temp = {}
						temp["title"] = heading
						temp["data"] = urlLink
						contents.append(temp)
				if title != "" and len(contents) >= 0:
					variableFormattedTitle = utility.MakeVariableFormattedNameFromString(title)
					if internetPresenceInfos.has_key(variableFormattedTitle) is False:
						internetPresenceInfos[variableFormattedTitle] = contents
		return internetPresenceInfos		 				
				
	def ParseContactInfo(self,pageSource):
		contactInfos = {}
		contactInfoSectionSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]+class=[\'\"]?profile-card-extras(.+?)</div></div></div>")
		if contactInfoSectionSource is not None:
			onlineContactInfos = self.ParseOnlineContactInfo(contactInfoSectionSource)
			offlineContactInfos = self.ParseOfflineContactInfo(contactInfoSectionSource)
			internetPresenceInfo = self.ParseInternetPresenceInfo(contactInfoSectionSource)
			#contactInfos += (onlineContactInfos + offlineContactInfos + internetPresenceInfo)
			contactInfos = dict(onlineContactInfos.items()+offlineContactInfos.items()+internetPresenceInfo.items())
		return contactInfos
	
	def ParseHonoursAndAwards(self,pageSource):
		honoursAndAwardRecords = []
		honoursAndAwardsSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]+id=[\'\"]?background-honors-container(.+?)</div></div></div></div>")
		if honoursAndAwardsSource is not None:
			honoursAndAwardsList = super(LinkedInParser,self).Parse(honoursAndAwardsSource,r"<div[\s]+id=[\'\"]?honors-53(.+?)</div></div></div>")
			for eachHonourAndAward in honoursAndAwardsList:
				title = ""
				titleSource = super(LinkedInParser,self).ParseSingle(eachHonourAndAward,r"<h4(.+?)</h4>")
				if titleSource is not None:
					title = super(LinkedInParser,self).ParseAndReplace(titleSource,r"<(.+?)>","")
				institution = ""
				institutionSource = super(LinkedInParser,self).ParseSingle(eachHonourAndAward,r"<h5(.+?)</h5>")
				if institutionSource is not None:
					institution = super(LinkedInParser,self).ParseAndReplace(institutionSource,r"<(.+?)>","")
				date = ""
				dateSource = super(LinkedInParser,self).ParseSingle(eachHonourAndAward,r"<time(.+?)</time>")
				if dateSource is not None:
					date = super(LinkedInParser,self).ParseAndReplace(dateSource,r"<(.+?)>","")
				if title != "":	 
					tempEntity = {}
					tempEntity["title"] = title
					tempEntity["institution"] = institution
					tempEntity["time"] = date
					honoursAndAwardRecords.append(tempEntity)
		additionalHonoursSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]+id=[\'\"]?honors-additional-item(.+?)</div></div></div></div>")
		if additionalHonoursSource is not None:
			additionalHonoursParagraphSource = super(LinkedInParser,self).ParseSingle(additionalHonoursSource,r"<p(.+?)</p>")
			if additionalHonoursParagraphSource is not None:
				additionalHonoursList = super(LinkedInParser,self).Parse(additionalHonoursParagraphSource,r">(.+?)<")
				for eachAdditionalHonour in additionalHonoursList:
					if eachAdditionalHonour != "":
						tempEntity = {}
						tempEntity["title"] = eachAdditionalHonour
						honoursAndAwardRecords.append(tempEntity)
		return honoursAndAwardRecords		
		
	def ParseEndorseTitle(self,pageSource):
		title = ""
		titleSource = super(LinkedInParser,self).ParseSingle(pageSource,r"data-endorsed-item-name=[\'\"](.+?)[\'\"]")
		if titleSource is not None:
			title = super(LinkedInParser,self).ParseAndReplace(titleSource,r"(.+?)=\"","")
			title = super(LinkedInParser,self).ParseAndReplace(title,r"\"","")
		return title
	
	def ParseTechSkillsAndExpertise(self,pageSource):
		endorseList = []
		skillsAndExpertiseSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]+id=[\'\"]?background-skills-container(.+?)</div></div></div></div>")
		if skillsAndExpertiseSource is not None:
			skillsAndExpertiseSourceLIs = super(LinkedInParser,self).Parse(skillsAndExpertiseSource,r"<li(.+?)>")
			for eachSkillsAndExpertiseSourceLI in skillsAndExpertiseSourceLIs:
				endorseTitle = self.ParseEndorseTitle(eachSkillsAndExpertiseSourceLI)
				if endorseTitle != "":  
					endorseList.append(endorseTitle)
		return endorseList
	
	def ParseCertificationTitle(self,pageSource):
		title = ""
		certificationTitleSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<h4(.+?)</h4>")
		if certificationTitleSource is not None:
			title = super(LinkedInParser,self).ParseAndReplace(certificationTitleSource,r"<(.+?)>","")
		return title
	
	def ParseCertificationInstitutionsTitle(self,pageSource):
		companyTitle = ""
		certificationCompanyTitleSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<h5(.+?)</h5>")
		if certificationCompanyTitleSource is not None:
			companyTitle = super(LinkedInParser,self).ParseAndReplace(certificationCompanyTitleSource,r"<(.+?)>","")
		return companyTitle
	
	def ParseCertificationDate(self,pageSource):
		date = ""
		certificationDateSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<span[\s]+class=[\'\"]?certification-date(.+?)</span>")
		if certificationDateSource is not None:
			date = super(LinkedInParser,self).ParseAndReplace(certificationDateSource,r"<(.+?)>","")
		return date
	
	def ParseCertifications(self,pageSource):
		certifications = []
		certificationsSource = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]+id=[\'\"]?background-certifications-container(.+?)</div></div></div></div>")
		if certificationsSource is not None:
			certificationsRows = super(LinkedInParser,self).Parse(certificationsSource,r"<div[\s]+id=[\'\"]?certification(.+?)</div></div>")
			for eachCertificationsRow in certificationsRows:
				title = self.ParseCertificationTitle(eachCertificationsRow)
				institution = self.ParseCertificationInstitutionsTitle(eachCertificationsRow)
				date = self.ParseCertificationDate(eachCertificationsRow)
				if title != "":
					eachCertification = {}
					eachCertification["title"] = title
					if institution != "":
						eachCertification["institution"] = institution
					if date != "":
						eachCertification["date"] = date
					certifications.append(eachCertification)
		return certifications	
	
	def ParseConnectionsCount(self,pageSource):
		connectionsCount = ""
		connectionsCountElement = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]class=[\'\"]member-connections(.+?)</div>")
		if connectionsCountElement is not None:
			connectionsCountAnchorElement = super(LinkedInParser,self).ParseSingle(connectionsCountElement,r"<a(.+?)</a>")
			if connectionsCountAnchorElement is not None:
				connectionsCount = super(LinkedInParser,self).ParseAndReplace(connectionsCountAnchorElement,r"<(.+?)>","")
				###Now try to match the numeric pattern.
				if connectionsCount is not None:
					matcherObj = re.match(r"[\\d+]*",connectionsCount)
					if matcherObj is not None:
						return connectionsCount
					else:
						return None
	
	def ParseGroups(self,pageSource):
		groups = []
		groupsAreaContainer = super(LinkedInParser,self).ParseSingle(pageSource,r"<div[\s]id=[\'\"]groups-container(.+?)</ul></div>")
		if groupsAreaContainer is not None:
			groupListLIs = super(LinkedInParser,self).Parse(groupsAreaContainer,r"<li(.+?)</li>")
			for eachLI in groupListLIs:
				try:
					groupContainerLinkAnchorList = super(LinkedInParser,self).Parse(eachLI,r"<a(.+?)</a>")
					groupNameContainerLinkAnchor = None
					if len(groupContainerLinkAnchorList) > 1:
						groupNameContainerLinkAnchor = groupContainerLinkAnchorList[1]
					if groupNameContainerLinkAnchor is not None:
						groupHref = super(LinkedInParser,self).ParseSingle(groupNameContainerLinkAnchor,r"href=[\'\"](.+?)[\'\"]")
						groupName = super(LinkedInParser,self).ParseSingle(groupNameContainerLinkAnchor,r"<strong>(.+?)</strong>")
						if groupHref is not None and groupName is not None:
							groupHref = super(LinkedInParser,self).ParseAndReplace(groupHref,r"href=","")
							groupHref = super(LinkedInParser,self).ParseAndReplace(groupHref,r"[\'\"]","")
							groupName = super(LinkedInParser,self).ParseAndReplace(groupName,r"<(.+?)>","")
							groups.append({"link":groupHref,"name":groupName})
				except Exception,exp:
					print exp
					continue
		return groups	 	  
		
	def ParseUserProfile(self,pageSource):
		profile = {}
		profile["general_info"] = self.ParseGeneralInfo(pageSource)
		profile["connections"] = {"count":self.ParseConnectionsCount(pageSource)}
		profile["works_and_education"] = self.ParseExperiencesAndEducations(pageSource)
		additionalInfo = self.ParseAdditionalInfo(pageSource)
		profile = dict(profile.items()+additionalInfo.items())
		contactInfo = self.ParseContactInfo(pageSource)
		profile["contact_info"] = contactInfo 
		skillsAndExpertise = self.ParseTechSkillsAndExpertise(pageSource)
		if len(skillsAndExpertise) > 0:
			profile["skills_and_expertise"] = skillsAndExpertise
		honoursAndAwards = self.ParseHonoursAndAwards(pageSource)
		if len(honoursAndAwards) > 0:
			profile["honours_and_awards"] = honoursAndAwards
		certifications = self.ParseCertifications(pageSource)
		profile["certifications"] = certifications
		profile["groups"] = self.ParseGroups(pageSource)
		return profile
	def ConvertURL(self,siteStandardProfileUrl):
		###https://www.linkedin.com/profile/view?id=36379560&authType=NAME_SEARCH&authToken=Xu6Q&trk=api*a231405*s2393+07*
		#https://www.linkedin.com/profile?viewProfile=&key=36379560&authToken=Xu6Q&authType=NAME_SEARCH&trk=api*a231405*s239307*
		compatibleURL = ""
		try:
			userId = super(LinkedInParser,self).ParseSingle(siteStandardProfileUrl,r"key=[\d]+")
			userId = super(LinkedInParser,self).ParseAndReplace(userId,r"key=","")
			authType = super(LinkedInParser,self).ParseSingle(siteStandardProfileUrl,r"authType=(.+?)\&")
			authType = super(LinkedInParser,self).ParseAndReplace(authType,r"authType=","")
			authType = super(LinkedInParser,self).ParseAndReplace(authType,r"\&","")
			authToken = super(LinkedInParser,self).ParseSingle(siteStandardProfileUrl,r"authToken=(.+?)\&")
			authToken = super(LinkedInParser,self).ParseAndReplace(authToken,r"authToken=","")
			authToken = super(LinkedInParser,self).ParseAndReplace(authToken,r"\&","")
			trk = super(LinkedInParser,self).ParseSingle(siteStandardProfileUrl,r"trk=(.+)")
			trk = super(LinkedInParser,self).ParseAndReplace(trk,r"trk=","")
			
			compatibleURL += "https://www.linkedin.com/profile/view?id="+userId+"&authType="+authType+"&authToken="+authToken+"&trk="+trk
			
		except Exception,exp:
			print "Exception Occured..."
			print exp
			compatibleURL = siteStandardProfileUrl
		return compatibleURL
		
		
		
	