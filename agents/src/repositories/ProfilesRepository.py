from pymongo import MongoClient
import logging
from src.logging.logging_config import setup_papertrail_logging

class ProfilesRepository:
    def __init__(self, db_uri='mongodb://localhost:27017/', db_name='r1n_framework'):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db.profiles

        setup_papertrail_logging('ProfilesRepository')
        self.logger = logging.getLogger('ProfilesRepository')

    def add(self, data):
        """Insert a new profile into the MongoDB collection."""
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            self.logger.error(f"Failed to add profile: {e}")
            return None
    
    def get(self, uuid):
        """Retrieve a profile by its UUID."""
        try:
            profile = self.collection.find_one({"uuid": uuid}, {'_id': 0})
            return profile
        except Exception as e:
            self.logger.error(f"Failed to find profile by UUID {uuid}: {e}")
            return None
    
    def update(self, uuid, updates):
        """Update a profile by its UUID with the given update data."""
        try:
            result = self.collection.update_one({"uuid": uuid}, {"$set": updates})
            return result.modified_count
        except Exception as e:
            self.logger.error(f"Failed to update profile {uuid}: {e}")
            return None
    
    def delete(self, uuid):
        """Delete a profile by its UUID."""
        try:
            result = self.collection.delete_one({"uuid": uuid})
            return result.deleted_count
        except Exception as e:
            self.logger.error(f"Failed to delete profile {uuid}: {e}")
            return None
    
    def list_all(self):
        """List all profiles in the collection."""
        try:
            profiles = list(self.collection.find({}, {'_id': 0}))
            return profiles
        except Exception as e:
            self.logger.error("Failed to list profiles: {e}")
            return None
