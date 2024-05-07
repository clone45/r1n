from pymongo import MongoClient
import logging
from src.logging.logging_config import setup_papertrail_logging

class RolesRepository:
    def __init__(self, db_uri='mongodb://localhost:27017/', db_name='r1n_framework'):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db.roles

        setup_papertrail_logging('RolesRepository')
        self.logger = logging.getLogger('RolesRepository')

    def add(self, data):
        """Insert a new role into the MongoDB collection."""
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            self.logger.error(f"Failed to add role: {e}")
            return None
    
    def get(self, uuid):
        """Retrieve a role by its UUID."""
        try:
            role = self.collection.find_one({"uuid": uuid}, {'_id': 0})
            return role
        except Exception as e:
            self.logger.error(f"Failed to find role by UUID {uuid}: {e}")
            return None
    
    def update(self, uuid, updates):
        """Update a role by its UUID with the given update data."""
        try:
            result = self.collection.update_one({"uuid": uuid}, {"$set": updates})
            return result.modified_count
        except Exception as e:
            self.logger.error(f"Failed to update role {uuid}: {e}")
            return None
    
    def delete(self, uuid):
        """Delete a role by its UUID."""
        try:
            result = self.collection.delete_one({"uuid": uuid})
            return result.deleted_count
        except Exception as e:
            self.logger.error(f"Failed to delete role {uuid}: {e}")
            return None
    
    def list_all(self):
        """List all roles in the collection."""
        try:
            roles = list(self.collection.find({}, {'_id': 0}))
            return roles
        except Exception as e:
            self.logger.error("Failed to list roles: {e}")
            return None
