#!/usr/bin/env python3

""" This script uses pymongo to perform MongoDB operations in Python """

from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Returns a sorted list of students based on their average score

    :param mongo_collection: pymongo collection object
    :return: a list of dictionaries containing the name
    and average score of each student
    """
    top_students = mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return top_students
