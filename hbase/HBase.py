import happybase
import time
import csv
import json

BASIC_PROFILE_TABLE_NAME = "datacard_basic_profile"
FULL_PROFILE_TABLE_NAME = "datacard_full_profile"
DATACARD_ROW_COUNT_TABLE_NAME = "datacard_row_count_table"
LAST_CRAWLED_PROFILE_ID_TABLE = "datacard_last_crawled_profile_id"
BASIC_PROFILE_COLUMN_FAMILLY_NAME = "d"
LAST_CRAWLED_PROFILE_ID_COLUMN_FAMILLY_NAME = "l"
BASIC_PROFILE_ROW_STARTS_WITH = "bp_row_"
FULL_PROFILE_COLUMN_FAMILLY_NAME = "f"
FULL_PROFILE_ROW_STARTS_WITH = "fp_row_"
ROW_COUNT_TABLE_COLUMN_FAMILLY_NAME = "r"
BASIC_PROFILE_ROW_COUNT_ROW_NAME = "basic_profile_count_row"
FULL_PROFILE_ROW_COUNT_ROW_NAME = "full_profile_count_row"
LAST_CRAWLED_PROFILE_ID_ROW_NAME = "last_crawled_profile_id_row_name"
CSV_FILE_NAME = "data.csv"


"""These are error codes."""
ERROR_CODES = {
               'NO_ERROR':0,
               'DATABASE_NOT_CONNECTED':1001,
               'VALUE_ERROR':1002,
               'DATA_TYPE_ERROR':1003,
               'INVALID_DATA_TYPE':1004,
               'UNEXPECTED_DATA_TYPE':1005,
               'NOT_FOUND':1006,
               'DATABASE_ERROR':1007,
               'INSERT_FAILED_IN_THE_DATABASE':1008,
               'UPDATE_FAILED_IN_THE_DATABASE':1009,
               'DELETE_FAILED_IN_THE_DATABASE':1010,
               'UNKNOWN_ERROR':1011,
               'TABLE_NOT_FOUND_IN_THE_DATABASE':1012,
               'PARTIALLY_UPDATED':1013,
               'LAST_CRAWLED_PROFILE_ID_READ_FAILED':1014,
               'LAST_ROW_COUNT_READING_FAILED':1015,
               'ROW_COUNT_UPDATE_FAILED':1016,
               'INVALID_COLUMN_NAME':1017
               }


"""Each and Every method should follow the below format as a response."""
RESPONSE_FORMAT = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }


ALLOWED_COLUMN_NAMES = [
                            "first_name",
                            "last_name",
                            "email",
                            "address",
                            "facebook",
                            "linkedin",
                            "twitter",
                            "google_plus"
                        ]


class HBase:
    def __init__(self):
        self.connected = False
        try:
            
            """Read configuration file."""
            config = self.ReadConfiguration()
            if config is not None and type(config) is tuple:
                HOST_NAME,PORT = tuple(config)
            else:
                raise Exception("Configuration read failed.")
            
            self.connection = happybase.Connection(HOST_NAME)
            self.connected = True
            self.CreateTables()
            self.basicProfileTable = self.connection.table(BASIC_PROFILE_TABLE_NAME)
            self.fullProfileTable = self.connection.table(FULL_PROFILE_TABLE_NAME)
            self.rowCountHolderTable = self.connection.table(DATACARD_ROW_COUNT_TABLE_NAME)
            self.lastCrawledProfileIdTable = self.connection.table(LAST_CRAWLED_PROFILE_ID_TABLE)
            self.InitializeRowCountTable()
            self.InitializeLastCrawledProfileIdTable()
            print "HBase Initialization has been done."
        except Exception,exp:
            self.connected = False
            
    def ReadConfiguration(self):
        try:
            """Read Configuration.xml file for database host and port name."""
            f = open("Configuration.xml","r")
            contents = f.read()
            f.close()
            
            """Now parse configurations."""
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(contents)
            
            hostName,port = None,None
            
            """Read the host name"""
            hostNameElement = soup.find("property",{"name":"host_name"})
            if hostNameElement is not None:
                hostName = hostNameElement.text.strip()
            portElement = soup.find("property",{"name":"port"})
            if portElement is not None:
                port = portElement.text.strip()
            if hostName is not None and port is not None:
                return (hostName,int(port))
        except Exception,exp:
            return None
        
    def GetAllowedColumnNames(self):
        return {"failure_indication":0,"error_code":0,"message":"successful","data":ALLOWED_COLUMN_NAMES}
        
    def GetTables(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                tableList = self.connection.tables()
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = tableList
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
    
    
    def ResetTables(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                self.connection.disable_table(BASIC_PROFILE_TABLE_NAME)
                self.connection.delete_table(BASIC_PROFILE_TABLE_NAME)
                
                self.connection.disable_table(FULL_PROFILE_TABLE_NAME)
                self.connection.delete_table(FULL_PROFILE_TABLE_NAME)
                
                self.connection.disable_table(DATACARD_ROW_COUNT_TABLE_NAME)
                self.connection.delete_table(DATACARD_ROW_COUNT_TABLE_NAME)
                
                self.connection.disable_table(LAST_CRAWLED_PROFILE_ID_TABLE)
                self.connection.delete_table(LAST_CRAWLED_PROFILE_ID_TABLE)
                
                self.InitializeRowCountTable()
                self.InitializeLastCrawledProfileIdTable()
                
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
    
    def CreateTables(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                basicProfileTableCreatedResponse = self.CreateBasicProfileTable()
                rowCountTableCreatedResponse = self.CreateRowCountHolderTable()
                fullProfileTableCreatedResponse = self.CreateFullProfileTable()
                lastCrawledProfileIdTableCreatedResponse = self.CreateLastCrawledProfileIdTable()
                if basicProfileTableCreatedResponse.get('failure_indication') == 0 and rowCountTableCreatedResponse.get('failure_indication') == 0 and fullProfileTableCreatedResponse.get('failure_indication') == 0 and lastCrawledProfileIdTableCreatedResponse.get('failure_indication') == 0:
                    RESPONSE['failure_indication'] = 0
                    RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                    RESPONSE['message'] = 'Successful'
                    RESPONSE['data'] = ''
                else:
                    RESPONSE['failure_indication'] = 1
                    RESPONSE['error_code'] = ERROR_CODES.get('PARTIALLY_UPDATED')
                    RESPONSE['message'] = 'Some tables might not be created successfully.'
                    RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
    
    def ReadCSVFile(self):
        dataList = []
        with open(CSV_FILE_NAME, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            counter = 0
            for eachRow in reader:
                if counter == 0:
                    counter += 1
                    continue
                dataList.append({BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"id":eachRow[0],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"email":eachRow[1],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"first_name":eachRow[2],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"last_name":eachRow[3],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"title":eachRow[4],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"address_one":eachRow[5],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"address_two":eachRow[6],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"city":eachRow[7],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"state":eachRow[8],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"zip":eachRow[9],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"country":eachRow[10],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"phone_one":eachRow[11],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"phone_two":eachRow[12],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"birth_year":eachRow[13],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"hs_grad_year":eachRow[14],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"highest_education_level":eachRow[15],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"us_citizen":eachRow[16],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"military_affiliation":eachRow[17],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"best_time_to_call":eachRow[18],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"is_valid_email":eachRow[19],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"date_added":eachRow[20],
                                 BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+"date_updated":eachRow[21]})
        return dataList
    
    
    """This method converts each dictionary with the column familly being added."""
    def CheckIfBelongsToAllowedColumnNamesAndAddColumnFamily(self,rowData):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        if type(rowData) is not dict:
            RESPONSE["failure_indication"] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('DATA_TYPE_ERROR')
            RESPONSE['message'] = 'Expected dict found '+str(type(rowData))
            RESPONSE['data'] = rowData
        else:
            modifiedDataDict = {}
            for key,value in rowData.items():
                if not key in ALLOWED_COLUMN_NAMES:
                    RESPONSE["failure_indication"] = 1
                    RESPONSE['error_code'] = ERROR_CODES.get('INVALID_COLUMN_NAME')
                    RESPONSE['message'] = 'Column name invalid. Allowed column names are: '+str(ALLOWED_COLUMN_NAMES)
                    RESPONSE['data'] = rowData
                    break
                else:
                    modifiedDataDict[BASIC_PROFILE_COLUMN_FAMILLY_NAME+":"+key] = value
            if len(modifiedDataDict) == len(rowData):
                RESPONSE["failure_indication"] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = modifiedDataDict
        return RESPONSE
                    
    
    
    def AddColumnFamiliToBasicProfileData(self,data):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        if type(data) is not list:
            RESPONSE["failure_indication"] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('DATA_TYPE_ERROR')
            RESPONSE['message'] = 'Expected list found '+str(type(data))
            RESPONSE['data'] = ''
        else:
            modifiedData = []
            for eachDataRow in data:
                tempDataRowResponse = self.CheckIfBelongsToAllowedColumnNamesAndAddColumnFamily(eachDataRow)
                if tempDataRowResponse.get("failure_indication") == 0:
                    modifiedData.append(tempDataRowResponse.get("data"))
                else:
                    RESPONSE = tempDataRowResponse
                    break
            if len(modifiedData) == len(data):
                RESPONSE["failure_indication"] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = modifiedData
        return RESPONSE
                
                
    def UploadBasicProfileBatchData(self,data):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                if type(data) is not list:
                    RESPONSE['failure_indication'] = 1
                    RESPONSE['error_code'] = ERROR_CODES.get('DATA_TYPE_ERROR')
                    RESPONSE['message'] = 'Expected list found '+str(type(data))
                    RESPONSE['data'] = ''
                else:
                    addColumnFamillyResponse = self.AddColumnFamiliToBasicProfileData(data)
                    if addColumnFamillyResponse.get("failure_indication") == 0:
                        basicProfileTableLastRowCountResponse = self.ReadLastRowCountBasicProfile()
                        if basicProfileTableLastRowCountResponse.get('failure_indication') == 1:
                            RESPONSE['failure_indication'] = 1
                            RESPONSE['error_code'] = ERROR_CODES.get('LAST_ROW_COUNT_READING_FAILED')
                            RESPONSE['message'] = 'Last row count reading failed for basic profile table.'
                            RESPONSE['data'] = ''
                        else:
                            intRowCount = int(basicProfileTableLastRowCount) + 1
                            with self.basicProfileTable.batch() as batch:
                                for eachData in data:
                                    batch.put(BASIC_PROFILE_ROW_STARTS_WITH+str(intRowCount),eachData)
                                    intRowCount += 1
                            rowCountBasicProfileUpdateResponse = self.UpdateRowCountBasicProfileTable(intRowCount)
                            if rowCountBasicProfileUpdateResponse.get('failure_indication') == 0:
                                RESPONSE['failure_indication'] = 0
                                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                                RESPONSE['message'] = 'Successful'
                                RESPONSE['data'] = ''
                            else:
                                RESPONSE['failure_indication'] = 1
                                RESPONSE['error_code'] = ERROR_CODES.get('ROW_COUNT_UPDATE_FAILED')
                                RESPONSE['message'] = 'Row count update failed for basic profile'
                                RESPONSE['data'] = 'Init row count was: '+str(int(basicProfileTableLastRowCount) + 1)+' and end row count was: '+str(intRowCount)
                    else:
                        RESPONSE = addColumnFamillyResponse
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
                
    def CreateLastCrawledProfileIdTable(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        
        try:
            if self.connected is True:
                self.connection.create_table(LAST_CRAWLED_PROFILE_ID_TABLE, {LAST_CRAWLED_PROFILE_ID_COLUMN_FAMILLY_NAME:dict()})
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
    
                
    def CreateBasicProfileTable(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                self.connection.create_table(BASIC_PROFILE_TABLE_NAME, {BASIC_PROFILE_COLUMN_FAMILLY_NAME:dict()})
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
    
    def CreateFullProfileTable(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                self.connection.create_table(FULL_PROFILE_TABLE_NAME, {FULL_PROFILE_COLUMN_FAMILLY_NAME:dict()})
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
    
    
    def InitializeLastCrawledProfileIdTable(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                lastCrawledProfileIdResponse = self.ReadLastCrawledProfileIdTable()
                if lastCrawledProfileIdResponse.get('failure_indication') == 1 and lastCrawledProfileIdResponse.get('error_code') == ERROR_CODES.get('VALUE_ERROR'):
                    self.UpdateLastCrawledProfileId(0)
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
        
        
    def InitializeRowCountTable(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                if self.rowCountHolderTable is not None:
                    basicProfileRowCountResponse = self.ReadLastRowCountBasicProfile()
                    basicProfileRowCountUpdatedResponse,fullProfileRowCountUpdatedResponse = None,None
                    if basicProfileRowCountResponse.get('failure_indication') == 1 and basicProfileRowCountResponse.get('error_code') == ERROR_CODES.get('VALUE_ERROR'):
                        basicProfileRowCountUpdatedResponse = self.UpdateRowCountBasicProfileTable(0)
                    fullProfileRowCountResponse = self.ReadLastRowCountFullProfile()
                    if fullProfileRowCountResponse.get('failure_indication') == 1 and fullProfileRowCountResponse.get('error_code') == ERROR_CODES.get('VALUE_ERROR'):
                        fullProfileRowCountUpdatedResponse = self.UpdateRowCountFullProfileTable(0)
                    
                    if basicProfileRowCountUpdatedResponse is not None and fullProfileRowCountUpdatedResponse is not None:
                        if basicProfileRowCountUpdatedResponse.get('failure_indication') == 0 and fullProfileRowCountUpdatedResponse.get('failure_indication') == 0:
                            RESPONSE['failure_indication'] = 0
                            RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                            RESPONSE['message'] = 'Successful'
                            RESPONSE['data'] = ''
                        elif basicProfileRowCountUpdatedResponse.get('failure_indication') == 1 and fullProfileRowCountUpdatedResponse.get('failure_indication') == 0:
                            RESPONSE['failure_indication'] = 1
                            RESPONSE['error_code'] = ERROR_CODES.get('PARTIALLY_UPDATED')
                            RESPONSE['message'] = 'Full profile row count has been updates but basic profile row count update failed.'
                            RESPONSE['data'] = ''
                        elif basicProfileRowCountUpdatedResponse.get('failure_indication') == 0 and fullProfileRowCountUpdatedResponse.get('failure_indication') == 1:
                            RESPONSE['failure_indication'] = 1
                            RESPONSE['error_code'] = ERROR_CODES.get('PARTIALLY_UPDATED')
                            RESPONSE['message'] = 'Basic profile row count has been updates but full profile row count update failed.'
                            RESPONSE['data'] = ''
                    else:
                        RESPONSE['failure_indication'] = 1
                        RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
                        RESPONSE['message'] = 'Unknown Error Occured.'
                        RESPONSE['data'] = ''
                    
                else:
                    RESPONSE['failure_indication'] = 1
                    RESPONSE['error_code'] = ERROR_CODES.get('TABLE_NOT_FOUND_IN_THE_DATABASE')
                    RESPONSE['message'] = 'Row count table is not found in the database.'
                    RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
            
        
        
    def CreateRowCountHolderTable(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                self.connection.create_table(DATACARD_ROW_COUNT_TABLE_NAME, {ROW_COUNT_TABLE_COLUMN_FAMILLY_NAME:dict()})
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
        
        
    def UpdateRowCountBasicProfileTable(self,rowCount):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                self.rowCountHolderTable.put(BASIC_PROFILE_ROW_COUNT_ROW_NAME, {ROW_COUNT_TABLE_COLUMN_FAMILLY_NAME+':row_count':str(rowCount)})
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
                
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
        
        
    def UpdateRowCountFullProfileTable(self,rowCount):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                self.rowCountHolderTable.put(FULL_PROFILE_ROW_COUNT_ROW_NAME, {ROW_COUNT_TABLE_COLUMN_FAMILLY_NAME+':row_count':str(rowCount)})
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
    
    def UpdateLastCrawledProfileId(self,value):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                self.lastCrawledProfileIdTable.put(LAST_CRAWLED_PROFILE_ID_ROW_NAME, {LAST_CRAWLED_PROFILE_ID_COLUMN_FAMILLY_NAME+':last_crawled_profile_id':str(value)})
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
        
    def ReadLastCrawledProfileIdTable(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                value = None
                row = self.lastCrawledProfileIdTable.row(LAST_CRAWLED_PROFILE_ID_ROW_NAME)
                if row is not None and type(row) is dict:
                    value = row.get(LAST_CRAWLED_PROFILE_ID_COLUMN_FAMILLY_NAME+':last_crawled_profile_id')
                if value is not None:
                    RESPONSE['failure_indication'] = 0
                    RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                    RESPONSE['message'] = 'Successful'
                    RESPONSE['data'] = value
                else:
                    RESPONSE['failure_indication'] = 1
                    RESPONSE['error_code'] = ERROR_CODES.get('VALUE_ERROR')
                    RESPONSE['message'] = 'No data found in the database.'
                    RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
    
    def ReadLastRowCountBasicProfile(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                value = None
                row = self.rowCountHolderTable.row(BASIC_PROFILE_ROW_COUNT_ROW_NAME)
                if row is not None and type(row) is dict:
                    value = row.get(ROW_COUNT_TABLE_COLUMN_FAMILLY_NAME+':row_count')
                if value is not None:
                    RESPONSE['failure_indication'] = 0
                    RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                    RESPONSE['message'] = 'Successful'
                    RESPONSE['data'] = value
                else:
                    RESPONSE['failure_indication'] = 1
                    RESPONSE['error_code'] = ERROR_CODES.get('VALUE_ERROR')
                    RESPONSE['message'] = 'No data found in the database.'
                    RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
        
    def ReadLastRowCountFullProfile(self):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                value = None
                row = self.rowCountHolderTable.row(FULL_PROFILE_ROW_COUNT_ROW_NAME)
                if row is not None and type(row) is dict:
                    value = row.get(ROW_COUNT_TABLE_COLUMN_FAMILLY_NAME+':row_count')
                if value is not None:
                    RESPONSE['failure_indication'] = 0
                    RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                    RESPONSE['message'] = 'Successful'
                    RESPONSE['data'] = value
                else:
                    RESPONSE['failure_indication'] = 1
                    RESPONSE['error_code'] = ERROR_CODES.get('VALUE_ERROR')
                    RESPONSE['message'] = 'No data found in the database.'
                    RESPONSE['data'] = ''
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
        
        
    def UploadSingleFullProfile(self,data,lastCrawledProfileId):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                if type(data) is not dict:
                    RESPONSE['failure_indication'] = 1
                    RESPONSE['error_code'] = ERROR_CODES.get('DATA_TYPE_ERROR')
                    RESPONSE['message'] = 'Expected dictionary found '+type(data)
                    RESPONSE['data'] = ''
                else:
                    dataStr = json.dumps(data)
                    lastRowCountResponse = self.ReadLastRowCountFullProfile()
                    if lastRowCountResponse.get('failure_indication') == 1:
                        RESPONSE['failure_indication'] = 1
                        RESPONSE['error_code'] = ERROR_CODES.get('LAST_ROW_COUNT_READING_FAILED')
                        RESPONSE['message'] = 'Last row count reading failed for full profile table.'
                        RESPONSE['data'] = ''
                    else:
                        lastRowCount = lastRowCountResponse.get('data')
                        currentRowToBeInserted = int(lastRowCount) + 1
                        self.fullProfileTable.put(FULL_PROFILE_ROW_STARTS_WITH+str(currentRowToBeInserted), {FULL_PROFILE_COLUMN_FAMILLY_NAME+':profile':dataStr})
                        self.UpdateRowCountFullProfileTable(currentRowToBeInserted)
                        self.UpdateLastCrawledProfileId(lastCrawledProfileId)
                        RESPONSE['failure_indication'] = 0
                        RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                        RESPONSE['message'] = 'Successful'
                        RESPONSE['data'] = lastRowCount
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
        
    
    def DecomposeIntoArrayOfChunks(self,data):
        if data is None or type(data) is not list or len(data) == 0:
            return None
        start,chunk_size = 0,50
        tempArray = data
        chunks = []
        while len(tempArray) > 0:
            chunk = tempArray[start:chunk_size]
            tempArray = tempArray[chunk_size:]
            chunks.append(chunk)
        return chunks
    
    def LoadDataIntoHBase(self):
        data = self.ReadCSVFile()
        chunks = self.DecomposeIntoArrayOfChunks(data)
        
        for i in range(len(chunks)):
            self.PopulateTableStructureWithBatchData(chunks[i])
        
    def DownloadBasicProfile(self,count=50):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                basicInfoList = []
                usersListToFetch = []
                lastCrawledProfileIdResponse = self.ReadLastCrawledProfileIdTable()
                if lastCrawledProfileIdResponse.get('failure_indication') == 1:
                    RESPONSE['failure_indication'] = 1
                    RESPONSE['error_code'] = ERROR_CODES.get('LAST_CRAWLED_PROFILE_ID_READ_FAILED')
                    RESPONSE['message'] = 'Last crawled profile id read failed.'
                    RESPONSE['data'] = []
                else:
                    start = int(lastCrawledProfileIdResponse.get('data')) + 1
                    for i in range(count):
                        usersListToFetch.append(BASIC_PROFILE_ROW_STARTS_WITH+str(start+i))
                    for key,data in self.basicProfileTable.rows(usersListToFetch):
                        basicInfoList.append(data)
                    RESPONSE['failure_indication'] = 0
                    RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                    RESPONSE['message'] = 'Successful'
                    RESPONSE['data'] = basicInfoList
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = []
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = []
        return RESPONSE
    
    def DownloadFullProfile(self,start=1,count=50):
        RESPONSE = {
                   'failure_indication':1,
                   'error_code':0,
                   'message':None,
                   'data':None
                   }
        try:
            if self.connected is True:
                fullProfiles = []
                userListToFetch = []
                for i in range(count):
                    userListToFetch.append(FULL_PROFILE_ROW_STARTS_WITH+str(start+i))
                for key,data in self.fullProfileTable.rows(userListToFetch):
                    fullProfiles.append(data)
                RESPONSE['failure_indication'] = 0
                RESPONSE['error_code'] = ERROR_CODES.get('NO_ERROR')
                RESPONSE['message'] = 'Successful'
                RESPONSE['data'] = fullProfiles
            else:
                RESPONSE['failure_indication'] = 1
                RESPONSE['error_code'] = ERROR_CODES.get('DATABASE_NOT_CONNECTED')
                RESPONSE['message'] = 'Database is not connected.'
                RESPONSE['data'] = ''
        except Exception,exp:
            RESPONSE['failure_indication'] = 1
            RESPONSE['error_code'] = ERROR_CODES.get('UNKNOWN_ERROR')
            RESPONSE['message'] = 'Exception occured %s' % str(exp)
            RESPONSE['data'] = ''
        return RESPONSE
    


#print HBase().UploadBasicProfileBatchData([{"first_name":"Md Shariful Islam","last_name":"Sohel","email":"codenginebd@gmail.com"},{"first_name":"Md Shariful Islam","last_name_1":"Sohel","email":"codenginebd@gmail.com"}])