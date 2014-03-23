from facebook import *
import urllib2

#browser = WebBrowser()
#browser.OpenURL("https://www.facebook.com")
#browser.LoginFacebook({"email":"sohel_buet065@yahoo.com","password":"lapsso065CommlinkCommlink"})
#
#parser = FII_FBParser()
#
#graph = FBGraph()
#
#response = graph.SearchUserByEmail(browser,parser,"sohel_buet065@yahoo.com","hajhskjhakshkj")
#
#jsonResponse = Utility().JSONEncode(response)
#
#if jsonResponse.get("error") is not None:
#    error = jsonResponse.get("error")
#    errorType = error.get("type")
#    if errorType == "OAuthException":
#        print "TOKEN_EXPIRED"

#print encodedJSON.get("error").get("type") == "OAuthException"

#html_doc = """
#<html><head><title>The Dormouse's story</title></head>
#
#<p class="title"><b>The Dormouse's story</b></p>
#
#<p class="story">Once upon a time there were three little sisters; and their names were
#<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
#<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
#<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
#and they lived at the bottom of a well.</p>
#<div class="eEmMnd fNFtPe xBhTpc eEmMnd"><div class="MLtShf"><div class="vdgRCc"><div class="ZMDitf">Work</div></div></div><div class="A4Urud">
#<div class="pfqkd f7g5be"><div class="D0cs5d"><div class="cHz88d">Occupation</div><div class="umCUbe jMjfWb">What do you do?</div></div>
#<div class="D0cs5d"><div class="cHz88d">Skills</div><div class="umCUbe jMjfWb">What are your skills?</div></div><div class="D0cs5d">
#<div class="cHz88d FQRMI">Employment</div><div class="umCUbe"><ul class="HC"><li class="nT"><div class="CE org">Commlink Info Tech Ltd.</div>
#<div class="EC">Software Engineer, 2012 - present</div>
#</li></ul></div></div></div><div><div class="ZwXCke"><span role="button" class="a-n lKU0qc Ataqc" tabindex="0">Edit</span></div></div></div></div>
#<p class="story">...</p>
#"""
#
#from bs4 import BeautifulSoup
#soup = BeautifulSoup(html_doc)
#divsWithClasseEmMnd = soup.findAll("div", {"class":"eEmMnd"})
#experienceDiv = None
#for eachDiv in divsWithClasseEmMnd:
#    titleContainer = eachDiv.find("div",{"class":"ZMDitf"})
#    if titleContainer is not None:
#        if titleContainer.text == "Work":
#            experienceDiv = eachDiv
#            break
#if experienceDiv is not None:
#    contentRows = soup.findAll("div", {"class":"D0cs5d"})
#    experiences = []
#    for eachRow in contentRows:
#        experienceTitle = eachRow.find("div",{"class":"cHz88d"})
#        experienceBody = eachRow.find("div",{"class":"umCUbe"})
#        expTitle,expBody = "",""
#        if experienceTitle is not None:
#            expTitle = experienceTitle.text
#        if experienceBody is not None:
#            expBody = experienceBody.text
#        if expTitle != "" and expBody != "":
#            experiences.append({"title":expTitle,"body":expBody})
##    print experiences
#d = soup.find("div",{"class":"eEmMnd"})
#print d
#dataArray = []
#for i in range(10):
#    dataArray.append(i*i)
#tempArray = dataArray
#start,chunk_size = 0,50
#chunks = []
#while len(tempArray) > 0:
#    chunk = tempArray[start:chunk_size]
##    start = chunk_size
#    chunk_size = chunk_size
#    tempArray = tempArray[chunk_size:]
#    chunks.append(chunk) 
#print chunks

data = {"data1": [{"first_name":"Md Shariful Islam","last_name":"Sohel","email":"somenameyahoo.com","facebook":"https://www.facebook.com/sharifulislamsohel/","linkedin":"https://www.linkedin.com/profile/view?id=36379560&authType=NAME_SEARCH&authToken=Xu6Q&trk=api*a231405*s2393+07*","twitter":"https://twitter.com/codenginebd"}]}
req = urllib2.Request("http://127.0.0.1:5000/api/1.0/basic_profile/upload/", data=json.dumps(data),headers={"Content-Type": "application/json"})
print urllib2.urlopen(req).read()
