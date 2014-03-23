import gflags
import httplib2
import logging
import os
import pprint
import sys
import simplejson as json
import time

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run

FLAGS = gflags.FLAGS
CLIENT_SECRETS = 'client_secrets.json'

# Helpful message to display if the CLIENT_SECRETS file is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to download the client_secrets.json file
and save it at:

   %s

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope=[
      'https://www.googleapis.com/auth/devstorage.read_only',
      'https://www.googleapis.com/auth/devstorage.read_write',
      'https://www.googleapis.com/auth/bigquery',
      'https://www.googleapis.com/auth/devstorage.full_control',
    ],
    message=MISSING_CLIENT_SECRETS_MESSAGE)
# The gflags module makes defining command-line options easy for
# applications. Run this program with the '--help' argument to see
# all the flags that it understands.
gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')


class BigQuery:
	def __init__(self):
		print "BigQuery Initializing..."+str(os.getcwd()) 
		# Let the gflags module process the command-line arguments
		
		#try:
		#  argv = FLAGS(argv)
		#except gflags.FlagsError, e:
		#  #print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
		#  sys.exit(1)
		
		# Set the logging according to the command-line flag
		logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))
		
		# If the Credentials don't exist or are invalid, run through the native
		# client flow. The Storage object will ensure that if successful the good
		# Credentials will get written back to a file.
		storage = Storage('sample.dat')
		credentials = storage.get()
		
		if credentials is None or credentials.invalid:
		  credentials = run(FLOW, storage)
		
		# Create an httplib2.Http object to handle our HTTP requests and authorize it
		# with our good Credentials.
		self.http = httplib2.Http()
		self.http = credentials.authorize(self.http)
		
		self.service = build('bigquery', 'v2', http=self.http)
		print "BigQuery Initialization has been Done." 
	###The following method will Read data from BigQuery specified by the query parameter.
	###Parameter description: projectId is the id of the project,datasetId is the id of the dataset that contains tables.
	###query is the query to execute
	###timeout is a optional parameter in milliseconds
	def ReadDataSync(self,projectId,datasetId,query,timeout=0):
		records = []
		try:
			jobCollection = self.service.jobs()
			queryData = {'query':query,'timeoutMs':timeout}
			queryReply = jobCollection.query(projectId=projectId,body=queryData).execute()
			jobReference=queryReply['jobReference']
			while(not queryReply['jobComplete']):
				print 'Job not yet complete...'
				queryReply = jobCollection.getQueryResults(projectId=jobReference['projectId'],jobId=jobReference['jobId'],timeoutMs=timeout).execute()
			if queryReply.get("rows") is not None:
				data = queryReply.get("rows")
				for eachRow in data:
					if eachRow.get("f") is not None:
						rowData = eachRow.get("f")
						records.append(rowData)
						#print eachRow['f']
		except Exception,e:
			print str(e)
		return records
	###This function uploads the data into Google BigQuery in table specified in the tableId parameter
	###tableSchemaSource is the source file containing the json schema of the target table
	###dataSource parameter holds the data in the exact for of the table specified in tableSchemaSource
	###The tableSchemaSource must match the format of the target table to store.
	###e.g. dataSource and tableSchemaSourceFile parameter both holds the opened file reference to the data and schema file
	def Upload(self,projectId,datasetId,tableId,tableSchemaSourceFile,dataSourceFile):
		url = "https://www.googleapis.com/upload/bigquery/v2/projects/" + projectId + "/jobs"
		#print url
		schema = tableSchemaSourceFile ###tableSchemaSourceFile is the reference to the open file. The file mode is preferably r
		dataFile = dataSourceFile ###dataSourceFile is also the reference to the open file. The file mode is preferably r
		# Create the body of the request, separated by a boundary of xxx
		newSource = ('--xxx\n' +
			'Content-Type: application/json; charset=UTF-8\n' +'\n'+
			'{\n' +
			'   "configuration": {\n' +
			'     "load": {\n' +
			'       "sourceFormat": "NEWLINE_DELIMITED_JSON",\n'
			'       "schema": {\n'
			'         "fields": ' + schema.read() + '\n' +
			'      },\n' +
			'      "destinationTable": {\n' +
			'        "projectId": "' + projectId + '",\n' +
			'        "datasetId": "' + datasetId + '",\n' +
			'        "tableId": "' + tableId + '"\n' +
			'      }\n' +
			'    }\n' +
			'  }\n' +
			'}\n' +
			'--xxx\n' +
			'Content-Type: application/octet-stream\n' +
			'\n')
		# Append data from the specified file to the request body
		newSource += dataFile.read()
		# Signify the end of the body
		newSource += ('\n--xxx--\n')
		headers = {'Content-Type': 'multipart/related; boundary=xxx'}
		#print "New Source: "+newSource
		#http = httplib2.Http()
		resp, content = self.http.request(url, method="POST", body=newSource, headers=headers)
		print resp
		if resp.status == 200:
			jsonResponse = json.loads(content)
			jobReference = jsonResponse['jobReference']['jobId']
			while True:
				jobCollection = self.service.jobs()
				getJob = jobCollection.get(projectId=projectId, jobId=jobReference).execute()
				print getJob
				currentStatus = getJob['status']['state']
				if 'DONE' == currentStatus:
					print "Done Uploading!"
					return
				else:
					print 'Waiting to upload...'
					print 'Current status: ' + currentStatus
					print time.ctime()
					time.sleep(10)
			
		