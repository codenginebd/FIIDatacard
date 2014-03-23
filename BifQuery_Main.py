from bigquery import *
def main():

  bigQuery = BigQuery()
  
  try:

    print "Success! Now add code here."
    #listTables(service, "fiibigdata", "fii_datacard")
    #runSyncQuery (service, "fiibigdata", "fii_datacard", timeout=0)
    query = "select id,first_name,last_name,email from [fii_datacard.user_base] limit 100"
    #records = bigQuery.ReadDataSync("fiibigdata","fii_datacard",query)
    tableSchemaSourceFile = open("table_schema.json","r")
    #print "tableSchema "+str(tableSchemaSourceFile.read())
    dataSourceFile = open("data.json","r")
    #print "Data "+str(dataSourceFile.read())
    bigQuery.Upload("fiibigdata","fii_datacard","user_base_fb",tableSchemaSourceFile,dataSourceFile)
    #print "Done! with "+str(len(records))


    # For more information on the BigQuery API API you can visit:
    #
    #   https://developers.google.com/bigquery/docs/overview
    #
    # For more information on the BigQuery API API python library surface you
    # can visit:
    #
    #   https://google-api-client-libraries.appspot.com/documentation/bigquery/v2/python/latest/
    #
    # For information on the Python Client Library visit:
    #
    #   https://developers.google.com/api-client-library/python/start/get_started

  except AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")
  except Exception,e:
      print str(e)

if __name__ == '__main__':
  main()
