#!/usr/bin/env python3
"""
This function lists all documents in a PyMongo collection.
"""

def list_all(mongo_collection):
    """
    List all documents in a PyMongo collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection object to list documents from.

    Returns:
        A list of documents in the collection. Returns an empty list if there are no documents in the collection.
    """
    documents = list(mongo_collection.find())
    return documents
