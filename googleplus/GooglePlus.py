#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#

import gflags
import httplib2
import logging
import os
import pprint
import sys

from googleplus import *

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import run


FLAGS = gflags.FLAGS

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = 'gplus_client_secrets.json'

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console <https://code.google.com/apis/console>.

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

# Set up a Flow object to be used if we need to authenticate.
FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/plus.me',
    message=MISSING_CLIENT_SECRETS_MESSAGE)


# The gflags module makes defining command-line options easy for
# applications. Run this program with the '--help' argument to see
# all the flags that it understands.
gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')

class GooglePlus:
    def __init__(self):
        print "Initializing Google Plus..."
        # Set the logging according to the command-line flag
        logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))
        
        
        # If the Credentials don't exist or are invalid run through the native client
        # flow. The Storage object will ensure that if successful the good
        # Credentials will get written back to a file.
        storage = Storage('gplus.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = run(FLOW, storage)
            
        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with our good Credentials.
        http = httplib2.Http()
        self.http = credentials.authorize(http)
        self.service = build("plus", "v1", http=self.http)
        
    """ Method Search, searches for users in Google Plus. It takes   """
    def Search(self,userInfo):
        peoplesList = []
        people_resource = self.service.people()
        people_document = people_resource.search(maxResults=10,query=userInfo["full_name"]).execute(http=self.http)
        if 'items' in people_document:
            for person in people_document['items']:
                peoplesList.append({"id":person.get("id"),"display_name":person.get("displayName"),"profile_link":person.get("url")})
        return peoplesList
#        person = self.service.people().get(userId='me').execute(http=self.http)
#        print person