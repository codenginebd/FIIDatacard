from bigquery import *
class BigQueryUploader:
	def __init__(self):
		self.bigQueryInstance = BigQuery()
		print "Initializing BigQuery Uploader..."
	def Upload(self,tableSchemaReference,sourceDataFileReference,bigQueryInfo):
		try:
			projectId,datasetId,tableId = bigQueryInfo["project_id"],bigQueryInfo["dataset_id"],bigQueryInfo["table_id"]
			self.bigQueryInstance.Upload(projectId,datasetId,tableId,tableSchemaReference,sourceDataFileReference)
			print "Done Uploading!"
		except Exception,e:
			print "There was a problem while uploading was being processed."
		
		
		
		