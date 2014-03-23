from bigquery import *
class BigQueryDownloader:
	def __init__(self):
		self.bigQueryInstance = BigQuery()
		print "Initializing BigQuery Downloader..."
	def Download(self,bigQueryInfo):
		try:
			projectId,datasetId,query,timeout = bigQueryInfo["project_id"],bigQueryInfo["dataset_id"],bigQueryInfo["query"],bigQueryInfo["timeout"]
			print "Downloading Started for project FII_Datacard"
			jsonRecords = self.bigQueryInstance.ReadDataSync(projectId,datasetId,query,timeout)
			print "Done Downloading!"
			return jsonRecords
		except Exception,e:
			print "There was a problem while Downloading was being processed."
			return []
			
		
		
		