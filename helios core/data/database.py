"""
Database Module
================
MongoDB connection and data operations for Helios.

Note: This module is optional. The standalone main.py works without it.
"""

from pymongo import MongoClient
import pandas as pd

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "heliosDB"
COLLECTION_NAME = "energy_data"


def get_collection():
    """
    Get MongoDB collection for energy data.

    Returns:
        MongoDB collection object, or None if connection fails
    """
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()  # Test connection
        db = client[DB_NAME]
        return db[COLLECTION_NAME]
    except Exception as e:
        print(f"Warning: MongoDB not available - {e}")
        return None


def save_results(df, collection=None):
    """
    Save simulation results to MongoDB.

    Args:
        df: pandas DataFrame with simulation results
        collection: MongoDB collection (optional, uses default if None)
    """
    if collection is None:
        collection = get_collection()

    if collection is None:
        print("Could not save to MongoDB - database not available")
        return

    data = df.to_dict(orient="records")
    collection.insert_many(data)
    print("Data inserted into MongoDB")


def load_data(collection=None):
    """
    Load energy data from MongoDB.

    Args:
        collection: MongoDB collection (optional, uses default if None)

    Returns:
        pandas DataFrame with loaded data, or empty DataFrame if unavailable
    """
    if collection is None:
        collection = get_collection()

    if collection is None:
        return pd.DataFrame()

    data = list(collection.find())

    if len(data) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    if "_id" in df.columns:
        df = df.drop(columns=["_id"])

    return df


def create_connection():
    """Legacy function - use get_collection() instead."""
    return get_collection()