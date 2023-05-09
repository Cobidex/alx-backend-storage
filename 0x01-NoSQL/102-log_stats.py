#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def log_stats():
    """
    Provides some stats about Nginx logs stored in MongoDB
    """
    client = MongoClient('mongodb://localhost:27017/')
    logs_collection = client.logs.nginx

    # Count total number of logs
    total_logs = logs_collection.count_documents({})

    # Count number of logs by method
    methods = logs_collection.aggregate([
        {'$group': {'_id': '$method', 'count': {'$sum': 1}}}
    ])
    method_counts = {method['_id']: method['count'] for method in methods}

    # Count number of status checks
    status_checks = logs_collection.count_documents({'status': {'$regex': '^2.*'}})

    # Find top 10 most present IPs
    top_ips = logs_collection.aggregate([
        {'$group': {'_id': '$ip', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ])

    print(f"{total_logs} logs")

    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_checks} status check")

    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == '__main__':
    log_stats()
