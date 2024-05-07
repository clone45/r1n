from pymongo import MongoClient
import logging
from src.logging.logging_config import setup_papertrail_logging

class PresenceRepository:
    def __init__(self, db_uri='mongodb://localhost:27017/', db_name='r1n_framework'):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db.presence

        setup_papertrail_logging('PresenceRepository')
        self.logger = logging.getLogger('PresenceRepository')

    def get(self, uuid):
        """Retrieve a presence record by its UUID."""
        try:
            presence = self.collection.find_one({"uuid": uuid}, {'_id': 0})
            return presence
        except Exception as e:
            self.logger.error(f"Failed to find presence by UUID {uuid}: {e}")
            return None

    def list_all(self):
        """List all presence records in the collection."""
        try:
            presences = list(self.collection.find({}, {'_id': 0}))
            return presences
        except Exception as e:
            self.logger.error("Failed to list presence records: {e}")
            return None

    def find_by_agent_instance_uuid(self, agent_instance_uuid):
        """Retrieve a presence record by its agent instance UUID."""
        try:
            presence = self.collection.find_one({"agent_instance_uuid": agent_instance_uuid}, {'_id': 0})
            return presence
        except Exception as e:
            self.logger.error(f"Failed to find presence by agent instance UUID {agent_instance_uuid}: {e}")
            return None

    def add(self, data):
        """Insert a new presence record into the MongoDB collection."""
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            self.logger.error(f"Failed to add presence record: {e}")
            return None

    def update(self, uuid, updates):
        """Update a presence record by its UUID with the given update data."""
        try:
            result = self.collection.update_one({"uuid": uuid}, {"$set": updates})
            return result.modified_count
        except Exception as e:
            self.logger.error(f"Failed to update presence {uuid}: {e}")
            return None

    def delete(self, uuid):
        """Delete a presence record by its UUID."""
        try:
            result = self.collection.delete_one({"uuid": uuid})
            return result.deleted_count
        except Exception as e:
            self.logger.error(f"Failed to delete presence {uuid}: {e}")
            return None

    def delete_all(self):
        """Delete all presence records in the collection."""
        try:
            result = self.collection.delete_many({})
            return result.deleted_count
        except Exception as e:
            self.logger.error("Failed to delete all presence records: {e}")
            return None


