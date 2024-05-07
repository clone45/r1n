from pymongo import MongoClient
import logging
from src.logging.logging_config import setup_papertrail_logging

class TeamsRepository:
    def __init__(self, db_uri='mongodb://localhost:27017/', db_name='r1n_framework'):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db.teams

        setup_papertrail_logging('TeamsRepository')
        self.logger = logging.getLogger('TeamsRepository')

    def add(self, data):
        """Insert a new team into the MongoDB collection."""
        try:
            result = self.collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            self.logger.error(f"Failed to add team: {e}")
            return None
    
    def get(self, uuid):
        """Retrieve a team by its UUID."""
        try:
            team = self.collection.find_one({"uuid": uuid}, {'_id': 0})
            return team
        except Exception as e:
            self.logger.error(f"Failed to find team by UUID {uuid}: {e}")
            return None
    
    def update(self, uuid, updates):
        """Update a team by its UUID with the given update data."""
        try:
            result = self.collection.update_one({"uuid": uuid}, {"$set": updates})
            return result.modified_count
        except Exception as e:
            self.logger.error(f"Failed to update team {uuid}: {e}")
            return None
    
    def delete(self, uuid):
        """Delete a team by its UUID."""
        try:
            result = self.collection.delete_one({"uuid": uuid})
            return result.deleted_count
        except Exception as e:
            self.logger.error(f"Failed to delete team {uuid}: {e}")
            return None
    
    def list_all(self):
        """List all teams in the collection."""
        try:
            teams = list(self.collection.find({}, {'_id': 0}))
            return teams
        except Exception as e:
            self.logger.error("Failed to list teams: {e}")
            return None

    def list_teams_and_profiles(self):
        try:
            pipeline = [
                {'$lookup': {
                    'from': 'profiles',
                    'localField': 'profile_uuids',
                    'foreignField': 'uuid',
                    'as': 'profiles'
                }},
                {'$addFields': {
                    'id': {'$toString': '$_id'},
                    'profiles': {
                        '$map': {
                            'input': '$profiles',
                            'as': 'profile',
                            'in': {
                                'id': {'$toString': '$$profile._id'},
                                'name': '$$profile.name',
                                'email': '$$profile.email',
                                'role_uuid': '$$profile.role_uuid',
                                'avatar': '$$profile.avatar',
                                'description': '$$profile.description',
                                'welcome_message': '$$profile.welcome_message'
                            }
                        }
                    }
                }},
                {'$project': {
                    '_id': 0,
                    'name': 1,
                    'uuid': 1,
                    'description': 1,
                    'logo': 1,
                    'profile_uuids': 1,
                    'id': 1,
                    'profiles': 1
                }}
            ]
            result = list(self.collection.aggregate(pipeline))
            return result if result else None
        except Exception as e:
            self.logger.error(f"Failed to load teams and profiles: {str(e)}")
            return None
