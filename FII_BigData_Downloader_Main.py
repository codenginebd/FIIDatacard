from globals import *
from BigQueryDownloader import *

class FII_Service_Downloader:
	def __init__(self):
		print "Initializing data uploader service in BigQuery..."
		
	def DownloadUserDataFromBigQuery(self,projectId,datasetId,limit=1000):
		downloader = BigQueryDownloader()
		bigQueryInfo = {}
		query = "select email,first_name,last_name,address1,address2,city,state,zip,country,phone1,phone2,birth_year from [fii_datacard.user_base] limit %s" % str(limit)
		bigQueryInfo["project_id"] = projectId #"fiibigdata"
		bigQueryInfo["dataset_id"] = datasetId #"fii_datacard"
		bigQueryInfo["query"] = query
		bigQueryInfo["timeout"] = 0
		records = downloader.Download(bigQueryInfo)
		print "Total Records: "+str(len(records))
		###Now save these data in a datafile
		users = []
		for eachRecord in records:
			emailJSON = eachRecord[0]
			email = emailJSON.get("v")
			firstNameJSON = eachRecord[1]
			firstName = firstNameJSON.get("v")
			lastNameJSON = eachRecord[2]
			lastName = lastNameJSON.get("v")
			addressOneJSON = eachRecord[3]
			addressOne = addressOneJSON.get("v")
			addressTwoJSON = eachRecord[4]
			addressTwo = addressTwoJSON.get("v")
			cityJSON = eachRecord[5]
			city = cityJSON.get("v")
			stateJSON = eachRecord[6]
			state = stateJSON.get("v")
			zipJSON = eachRecord[7]
			zipCode = zipJSON.get("v")
			countryJSON = eachRecord[8]
			country = countryJSON.get("v")
			phoneOneJSON = eachRecord[9]
			phoneOne = phoneOneJSON.get("v")
			phoneTwoJSON = eachRecord[10]
			phoneTwo = phoneTwoJSON.get("v")
			birthYearJSON = eachRecord[11]
			birthYear = birthYearJSON.get("v")
			
			singleUserEntityJSON = {
				"email":email,
				"first_name":firstName,
				"last_name":lastName,
				"address_one":addressOne,
				"address_two":addressTwo,
				"city":city,
				"state":state,
				"zip":zipCode,
				"country":country,
				"phone_one":phoneOne,
				"phone_two":phoneTwo,
				"birth_year":birthYear
			}
			users.append(singleUserEntityJSON)
			
		return users
		
	def RunService(self):
		projectId = FIIConstants.BigQueryInfo.PROJECT_ID
		datasetId = FIIConstants.BigQueryInfo.DATASET_ID 
		limit = 1000
		users = self.DownloadUserDataFromBigQuery(projectId, datasetId, limit)
		return users
		