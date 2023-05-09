#!/usr/bin/env python3
"""
This function updates all topics of a school document in a PyMongo collection based on the school's name.
"""

def update_topics(mongo_collection, name, topics):
    """
    Update all topics of a school document in a PyMongo collection based on the school's name.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection object to update the document in.
        name (str): The name of the school to update.
        topics (list of str): The new list of topics to set for the school.

    Returns:
        The number of documents updated.
    """
    result = mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
    return result.modified_count
