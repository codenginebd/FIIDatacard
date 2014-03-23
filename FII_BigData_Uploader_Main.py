from globals import *
from BigQueryUploader import *
import os

class FII_Service_Uploader:
	def __init__(self):
		self.uploader = BigQueryUploader()
		print "Initializing data uploader service in BigQuery..."
	
	def UploadUserDataIntoBigQuery(self,projectId,datasetId,tableId,schemaFileName,dataFileName):
		bigQueryInfo = {}
		bigQueryInfo["project_id"] = projectId
		bigQueryInfo["dataset_id"] = datasetId
		bigQueryInfo["table_id"] = tableId
		tableSchemaReference = open(schemaFileName,r"r")
		sourceDataFileReference = open(dataFileName,r"r")
		self.uploader.Upload(tableSchemaReference,sourceDataFileReference,bigQueryInfo)
	
	def RunService(self):
		while FIIVars.stop is False:
			
			""" Wait until crawler thread notifies. """
			FIIVars.downloaderBusy.acquire()
			print "Waiting to the download be completed."
			FIIVars.uploaderBusy.acquire()
			FIIVars.downloaderBusy.wait()
			print "Waiting is done. Now uploading..."
			FIIVars.uploading = True
			
			projectId = FIIConstants.BigQueryInfo.PROJECT_ID
			datasetId = FIIConstants.BigQueryInfo.DATASET_ID
			
			""" Getting all file names for output and schema """
			
			###For general info
			generalTable = FIIConstants.Tables.GENERAL 
			generalOutputFile = os.path.join(FIIDirs.outputDir,FIIConstants.OutputFileName.USER_PROFILE_BASE)
			generalSchemaFile = os.path.join(FIIDirs.schemaDir,FIIConstants.Schema.USER_PROFILE_BASE)
			
#			FII_Logger.LogINFO("Uploading profile data to  "+generalTable)
			
			self.UploadUserDataIntoBigQuery(projectId, datasetId, generalTable, generalSchemaFile, generalOutputFile)
			
			###For favorites info
			favoritesTable = FIIConstants.Tables.FAVORITES
			favoritesOutputFile = os.path.join(FIIDirs.outputDir,FIIConstants.OutputFileName.USER_PROFILE_FAVORITES)
			favoritesSchemaFile = os.path.join(FIIDirs.schemaDir,FIIConstants.Schema.USER_PROFILE_FAVORITES)
			
#			FII_Logger.LogINFO("Uploading profile data to  "+favoritesTable)
			
			self.UploadUserDataIntoBigQuery(projectId, datasetId, favoritesTable, favoritesSchemaFile, favoritesOutputFile)
			
			###For interests
			interestsTable = FIIConstants.Tables.INTERESTS
			interestsOutputFile = os.path.join(FIIDirs.outputDir,FIIConstants.OutputFileName.USER_PROFILE_INTERESTS)
			interestsSchemaFile = os.path.join(FIIDirs.schemaDir,FIIConstants.Schema.USER_PROFILE_INTERESTS)
			
#			FII_Logger.LogINFO("Uploading profile data to  "+interestsTable)
			
			self.UploadUserDataIntoBigQuery(projectId, datasetId, interestsTable, interestsSchemaFile, interestsOutputFile)
			
			###For knowledge
			knowledgeTable = FIIConstants.Tables.KNOWLEDGE
			knowledgeOutputFile = os.path.join(FIIDirs.outputDir,FIIConstants.OutputFileName.USER_PROFILE_KNOWLEDGE)
			knowledgeSchemaFile = os.path.join(FIIDirs.schemaDir,FIIConstants.Schema.USER_PROFILE_KNOWLEDGE)
			
#			FII_Logger.LogINFO("Uploading profile data to  "+knowledgeTable)
			
			self.UploadUserDataIntoBigQuery(projectId, datasetId, knowledgeTable, knowledgeSchemaFile, knowledgeOutputFile)
			
			###For rewards
			rewardsTable = FIIConstants.Tables.REWARDS
			rewardsOutputFile = os.path.join(FIIDirs.outputDir,FIIConstants.OutputFileName.USER_PROFILE_REWARDS)
			rewardsSchemaFile = os.path.join(FIIDirs.schemaDir,FIIConstants.Schema.USER_PROFILE_REWARDS)
			
#			FII_Logger.LogINFO("Uploading profile data to  "+rewardsTable)
			
			self.UploadUserDataIntoBigQuery(projectId, datasetId, rewardsTable, rewardsSchemaFile, rewardsOutputFile)
			
#			FII_Logger.LogINFO("Uploading Done!")
			
			FIIVars.uploading = False
			FIIVars.uploaderBusy.notify()
			FIIVars.uploaderBusy.release()
			FIIVars.downloaderBusy.release()
			
		
#service = FII_Service_Uploader()
#service.RunService()

