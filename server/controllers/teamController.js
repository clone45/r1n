// controllers/teamController.js
const Team = require('../models/Team');
const { v4: uuidv4 } = require('uuid');

exports.getTeams = async (req, res) => {
    try {
        const teams = await Team.aggregate([
            {
                $lookup: {
                    from: 'profiles', // Ensure your profiles collection is named correctly
                    localField: 'profile_uuids',
                    foreignField: 'uuid',
                    as: 'profiles'
                }
            },
            {
                $lookup: {
                    from: 'roles', // This should match your MongoDB collection name for roles
                    localField: 'profiles.role_uuid',
                    foreignField: 'uuid',
                    as: 'roleDetails'
                }
            },
            {
                $addFields: {
                    'id': { '$toString': '$_id' }, // Convert _id to string and name it id
                    'profiles': {
                        '$map': {
                            'input': '$profiles',
                            'as': 'profile',
                            'in': {
                                'id': {'$toString': '$$profile._id'},
                                'name': '$$profile.name',
                                'email': '$$profile.email', // Include if email is part of your schema
                                'role': { // Embed the role details from roleDetails array
                                    '$arrayElemAt': [
                                        '$roleDetails',
                                        {'$indexOfArray': ['$roleDetails.uuid', '$$profile.role_uuid']}
                                    ]
                                },
                                'avatar': '$$profile.avatar',
                                'description': '$$profile.description',
                                'welcome_message': '$$profile.welcome_message'
                            }
                        }
                    }
                }
            },
            {
                $project: {
                    _id: 0, // Exclude MongoDB default _id from final output
                    id: 1, // Include the new id
                    name: 1,
                    uuid: 1,
                    description: 1,
                    logo: 1,
                    profiles: 1,
                    profile_uuids: 1
                    // Do not mention roleDetails here
                }
            }
        ]);

        res.json(teams);
    } catch (error) {
        console.error("Error fetching teams with profiles and roles:", error);
        res.status(500).send("Failed to fetch teams with profiles and roles");
    }
};

exports.createTeam = async (req, res) => {
    try {

        // Check if uuid is provided, if not, assign a new one
        if (!req.body.uuid) {
            req.body.uuid = uuidv4();  // Assign a new UUID
        }

        const newTeam = new Team(req.body);
        const savedTeam = await newTeam.save();

        // Yes, we are repeating the aggregation here. This is to ensure the response includes profile details, because
        // that's how the client expects the data.
        const teamWithProfiles = await Team.aggregate([
            { $match: { _id: savedTeam._id } }, // Match the newly saved team
            {
                $lookup: {
                    from: 'profiles', // This should match your MongoDB collection name for profiles
                    localField: 'profile_uuids',
                    foreignField: 'uuid',
                    as: 'profiles'
                }
            },
            {
                $addFields: {
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
                }
            },
            {
                $project: {
                    _id: 0,
                    id: 1,
                    name: 1,
                    uuid: 1,
                    description: 1,
                    logo: 1,
                    profile_uuids: 1,
                    profiles: 1
                }
            }
        ]);

        if (teamWithProfiles.length > 0) {
            res.json(teamWithProfiles[0]); // Send back the first (and should be only) team with its profiles
        }
    }
    catch (error) {
        console.error('Error creating team with profiles:', error);
        res.status(500).send(error.message);
    }

};


exports.updateTeam = async (req, res) => {
    try {
        // First, update the team
        const updatedTeam = await Team.findByIdAndUpdate(req.params.id, req.body, { new: true });
        if (!updatedTeam) {
            return res.status(404).send('Team not found');
        }

        // Then, perform aggregation to include profile details
        const teamWithProfiles = await Team.aggregate([
            { $match: { _id: updatedTeam._id } }, // Match the updated team
            {
                $lookup: {
                    from: 'profiles', // This should match your MongoDB collection name for profiles
                    localField: 'profile_uuids',
                    foreignField: 'uuid',
                    as: 'profiles'
                }
            },
            {
                $addFields: {
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
                }
            },
            {
                $project: {
                    _id: 0,
                    id: 1,
                    name: 1,
                    uuid: 1,
                    description: 1,
                    logo: 1,
                    profile_uuids: 1,
                    profiles: 1
                }
            }
        ]);

        if (teamWithProfiles.length > 0) {
            res.json(teamWithProfiles[0]); // Send back the first (and should be only) team with its profiles
        } else {
            throw new Error('Team with profiles not found after update.');
        }
    } catch (error) {
        console.error('Error updating team with profiles:', error);
        res.status(500).send(error.message);
    }
};

exports.deleteTeam = async (req, res) => {
    try {
        const deletedTeam = await Team.findByIdAndDelete(req.params.id);
        if (!deletedTeam) {
            return res.status(404).send('Team not found');
        }
        res.send('Team deleted successfully');
    } catch (error) {
        console.error('Error deleting team:', error);
        res.status(500).send(error.message);
    }
};