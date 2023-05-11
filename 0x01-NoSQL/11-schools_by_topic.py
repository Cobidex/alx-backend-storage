#!/usr/bin/env python3
"""
This function returns the list of schools
in a PyMongo collection that have a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Return the list of schools in a PyMongo collection
    that have a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The collection object to search for schools in.
        topic (str): The topic to search for.

    Returns:
        A list of dictionaries, where each dictionary
        is a school document that has the specified topic.
    """
    schools = mongo_collection.find({"topics": {"$in": [topic]}})
    return list(schools)
