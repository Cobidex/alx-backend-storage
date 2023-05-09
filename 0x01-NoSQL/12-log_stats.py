#!/usr/bin/env python3
"""Provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    logs = client.logs.nginx

    # x logs where x is the number of documents in this collection
    print("{} logs".format(logs.count_documents({})))

    # Methods:
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = logs.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    # method=GET, path=/status
    count = logs.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(count))
