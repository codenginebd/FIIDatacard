import sys
import simplejson as json
class Utility:
	def __init__(self):
		print "Initializing Utility..."
	def JSONEncode(self,data):
		jsonData = json.loads(data)
		return jsonData
	def JSONDecode(self,data):
		pass
	def JSONDecode(self,data,delimiter):
		dumpedData = json.dumps(data,sort_keys=True,indent=4*' ')
		return delimiter.join([l.rstrip() for l in dumpedData.splitlines()])
		