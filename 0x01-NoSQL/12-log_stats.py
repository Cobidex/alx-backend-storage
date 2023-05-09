#!/usr/bin/env python3
"""
Provide some stats about Nginx logs stored in MongoDB
"""
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
collection = client.logs.nginx

# number of documents in collection
num_docs = collection.count_documents({})
print("{} logs".format(num_docs))

# number of documents with each HTTP method
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    count = collection.count_documents({"method": method})
    print("    method {}: {}".format(method, count))

# number of documents with method=GET and path=/status
status_check = collection.count_documents({"method": "GET", "path": "/status"})
print("{} status check".format(status_check))
