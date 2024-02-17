from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
load_dotenv()

# Password for the 'elastic' user generated by Elasticsearch
ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD")

# Create the client instance
client = Elasticsearch(
    hosts=["https://localhost:9200"],
    verify_certs=False, # TODO: Add links to certs
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

# Successful response!
print(client.info())
