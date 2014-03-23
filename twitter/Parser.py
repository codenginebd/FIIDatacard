import re, os,sys
import htmlentitydefs
from htmlentitydefs import codepoint2name
class FIIParser(object):
	def __init__(self):
		pass
	def unescape(self,text):
		def fixup(m):
			text = m.group(0)
			if text[:2] == "&#":
				# character reference
				try:
					if text[:3] == "&#x":
						return unichr(int(text[3:-1], 16))
					else:
						return unichr(int(text[2:-1]))
				except Exception,e:
					return ""
			else:
				# named entity
				try:
					if text[1:-1] == "amp":
						text = "&amp;amp;"
					elif text[1:-1] == "gt":
					    text = "&amp;gt;"
					elif text[1:-1] == "lt":
					    text = "&amp;lt;"
					else:
						print text[1:-1]
						text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
				except Exception,e:
					return ""
			return text # leave as is
		textResult = ""
		try:
			textResult = re.sub("&#?\w+;", fixup, text)
		except Exception,e:
			pass
		return textResult
    
	def Parse(self,page,regex):
		results = []
		result = re.findall(regex,page,flags=re.MULTILINE | re.UNICODE | re.X | re.DOTALL | re.IGNORECASE)
		if result is not None:
			for aResult in result:
				results.append(aResult)
		return results
	def ParseSingle(self,page,regex):
		compiledRegex = re.compile(regex,flags=re.MULTILINE | re.UNICODE | re.X | re.DOTALL | re.IGNORECASE)
		match = compiledRegex.search(page)
		matchedText = None
		if match:
			#print match.group(1)
			matchedText = match.group(0)
		return matchedText
	def AddSlashes(self,string,doubleQuote = False):
		newString = ""
		if doubleQuote is True:
			newString = string.replace('"',r'\"')
		else:
			newString = string.replace("'",r"\'")
		return newString
		
	def SearchIfExists(self,page,pattern):
		compiledRegex = re.compile(pattern)
		match = compiledRegex.search(page)
		matched = None
		if match:
			matched = "Not None"
		return matched
	def ParseAndReplace(self,page,pattern,replacingStr):
		result = re.sub(pattern,replacingStr,page,flags=re.MULTILINE | re.UNICODE | re.X | re.DOTALL | re.IGNORECASE)
		return result
	def ParseAccessToken(self,page):
		tokens = self.Parse(page,"<code>(.+?)</code>")
		userToken = None
		if len(tokens) > 0:
			userToken = tokens[0]
			userToken = self.ParseAndReplace(userToken,"<(.+?)>","")
		return userToken
	def ParseSearchResponse(self,page):
		results = self.Parse(page,r"<pre(.+?)</pre>")
		result = None
		if len(results) > 0:
			result = results[0]
		#print "result"+str(result)
		if result is not None:
			result = self.ParseAndReplace(result,"(.+?)>","")
		return self.unescape(result)