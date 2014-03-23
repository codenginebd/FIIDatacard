#!/usr/bin/env python

from flask import Flask,jsonify
from flask import make_response
from hbase import *
from flask.globals import request
from flask import url_for
from test.test_xml_etree import methods
import json

app = Flask(__name__)
#app.config['SERVER_NAME'] = 'localhost'
hbase = HBase()

@app.route('/api/1.0/full_profile/<int:start>/<int:limit>',methods = ['GET'])
def GetFullProfile(start,limit):
	try:
		fullProfileResponse = hbase.DownloadFullProfile(start = start,count = limit)
		if fullProfileResponse is not None and type(fullProfileResponse) is dict:
			currentResponseLength = 0
			if type(fullProfileResponse.get('data')) is list:
				currentResponseLength = len(fullProfileResponse.get('data'))
			if currentResponseLength > 0 and currentResponseLength == limit:
				fullProfileResponse['next_url'] = url_for('GetFullProfile',start=start+currentResponseLength,limit=limit,_external = True)
		return jsonify(fullProfileResponse)
	except Exception,exp:
		return jsonify({'error':'An error occured while processing your request.','message':str(exp)})
	
@app.route('/api/1.0/basic_profile/upload/',methods = ['POST'])
def UploadBasicProfile():
	sampleDataFormat = {"data": [{"first_name":"First Name","last_name":"Last Name","email":"somename@yahoo.com","facebook":"https://www.facebook.com/facebook_user_name/","linkedin":"https://www.linkedin.com/profile/view?id=1234560&authType=NAME_SEARCH&authToken=Xu6Q&trk=api*a231405*s2393+07*","twitter":"https://twitter.com/twitter_name"}]}
	try:
		if not request.json:
			return jsonify({'error':'No data sent to upload.'})
		else:
			dictData = request.json
			if dictData.get('data') is not None and type(dictData.get('data')) is list:
				uploadResponse = hbase.UploadBasicProfileBatchData(dictData.get('data'))
				return jsonify(uploadResponse)
			else:
				return jsonify({'error':'data format error. The data sent to upload is not correctly formatted.','suggested_format':sampleDataFormat})
	except Exception,exp:
		return jsonify({'error':'An error occured while processing the request.','message':str(exp)})
	
@app.route('/api/1.0/column_names',methods = ['GET'])
def GetAllowedColumnNames():
	return jsonify(hbase.GetAllowedColumnNames())

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'The resource you requested was not found','error_code':404 } ), 404)
   
if __name__ == '__main__':
    app.run(debug = True)