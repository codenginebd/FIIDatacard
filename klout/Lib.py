import sys
import simplejson as json
from LinkedInParser import *
class LIUtility:
	def __init__(self):
		print "Initializing LinkedIn Utility..."
	def JSONEncode(self,data):
		jsonData = json.loads(data)
		return jsonData
	def JSONDecode(self,data):
		pass
	def JSONDecode(self,data,delimiter):
		dumpedData = json.dumps(data,sort_keys=True,indent=4*' ')
		return delimiter.join([l.rstrip() for l in dumpedData.splitlines()])
	def MakeVariableFormattedNameFromString(self,string): ### e.g. Charle's Marriage
		lowerName = string.lower()  ### charle's marriage
		quotedFreeName = lowerName.replace("'","") ###Replace all quote characters. e.g charles marriage
		hiphenFreeName = quotedFreeName.replace("-","") ###Replace all quote characters. e.g charles marriage
		spaceFreeName = hiphenFreeName.replace(" ","_") ###Replace all spaces using underscore. e.g charles_marriage
		variableFormattedName = spaceFreeName
		return variableFormattedName
	def EscapeURL(self,url):  ###http%3A%2F%2Fdeveloper%2Eforce%2Ecom%2Fmvp_profile_andyb
		map = {"%3A":":","%2F":"/","%2E":"."}
		url = url.replace("%3A",map.get("%3A"))
		url = url.replace("%2F",map.get("%2F"))
		url = url.replace("%2E",map.get("%2E"))
		return url
		