#!/usr/bin/env python3
""" provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient

if __name__ == "__main__":
    """ Provides ngnx stats """
    my_client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = my_client.logs.nginx

    my_logs = nginx_collection.count_documents({})
    print(f'{my_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        num = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {num}')

    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{status_check} status check')
