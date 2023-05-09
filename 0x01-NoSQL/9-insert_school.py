#!/usr/bin/env python3
"""
This function inserts a new document into a PyMongo collection based on keyword arguments.
"""

def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into a PyMongo collection based on keyword arguments.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection object to insert the document into.
        **kwargs: The keyword arguments representing the new document to insert.

    Returns:
        The _id of the newly inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
