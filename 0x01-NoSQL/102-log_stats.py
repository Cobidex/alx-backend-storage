#!/usr/bin/env python3
"""
This script performs various operations on a MongoDB database
using pymongo
"""

from pymongo import MongoClient

if __name__ == "__main__":
    """ Prints statistics about Nginx logs stored in MongoDB. """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    n_logs = nginx_collection.count_documents({})
    print(f'{n_logs} logs')

    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('HTTP methods:')
    for method in http_methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\t{method}: {count}')

    status_checks = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{status_checks} status checks')

    top_ip_counts = nginx_collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    print("IPs with highest request count:")
    for top_ip in top_ip_counts:
        ip = top_ip.get("ip")
        count = top_ip.get("count")
        print(f'\t{ip}: {count}')
