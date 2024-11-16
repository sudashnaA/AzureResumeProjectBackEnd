import logging
import json
import azure.functions as func
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import os
#HTTP trigger function
# Will increment the cosmodb count value by one when triggered
def main(req: func.HttpRequest, doc:func.DocumentList) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    url = os.environ['FUNCTION_URL']
    key = os.environ['FUNCTION_KEY']

    client = CosmosClient(url, credential=key)
    DATABASE_NAME = 'resumedb'
    database = client.get_database_client(DATABASE_NAME)
    CONTAINER_NAME = 'Visitors'
    container = database.get_container_client(CONTAINER_NAME)
    documentid = "1"

    read_item = container.read_item(item=documentid, partition_key=documentid)
    count = read_item['count'] + 1
    read_item['count'] = count
    container.replace_item(item=read_item, body=read_item)

    return func.HttpResponse(
            f"Visitor count updated to: {count}"   
    ) 