// controllers/profilesController.js

const Profile = require('../models/Profile');
const { v4: uuidv4 } = require('uuid');

exports.getProfiles = async (req, res) => {
    try {
        const profiles = await Profile.aggregate([
            {
                $lookup: {
                    from: 'roles', // Ensure this matches your roles collection name
                    localField: 'role_uuid',
                    foreignField: 'uuid', // This should match the UUID in the roles collection
                    as: 'roleDetails'
                }
            },
            {
                $addFields: {
                    role: { $arrayElemAt: ['$roleDetails', 0] }, // Take the first element from the 'roleDetails' array
                    id: { '$toString': '$_id' } // Convert '_id' to string and assign to 'id'
                }
            },
            {
                $project: {
                    id: 1, // Include the new 'id' field
                    name: 1,
                    role_uuid: 1,
                    uuid: 1,
                    avatar: 1,
                    description: 1,
                    welcome_message: 1,
                    role: 1, // Include the role after adjustments
                    _id: 0 // Explicitly exclude '_id' (This is the only exclusion allowed with other fields being included)
                }
            }
        ]);
        res.json(profiles);
    } catch (error) {
        console.error("profilesController.js::getProfiles: " + error.message);
        res.status(500).send("Failed to fetch profiles with role details");
    }
};

exports.createProfile = async (req, res) => {
    try {
        if (!req.body.uuid) req.body.uuid = uuidv4();  // Ensuring each profile has a unique UUID

        const newProfile = new Profile(req.body);
        const savedProfile = await newProfile.save();

        // Convert the Mongoose document to a plain JavaScript object
        const profileObj = savedProfile.toObject();

        // Rename _id to id
        profileObj.id = profileObj._id.toString();
        delete profileObj._id;  // Remove the original _id property

        res.status(201).send(profileObj);
    } catch (error) {
        console.error("Failed to create profile:", error);
        res.status(400).send(error.message);  // Send the error message back to the client
    }
};

exports.updateProfile = async (req, res) => {
    try {
        const updatedProfile = await Profile.findByIdAndUpdate(req.params.id, req.body, { new: true });
        if (!updatedProfile) {
            return res.status(404).send('Profile not found');
        }
        res.send(updatedProfile);
    } catch (error) {
        res.status(500).send(error.message);
    }
}

exports.deleteProfile = async (req, res) => {
    try {
        const deletedProfile = await Profile.findByIdAndDelete(req.params.id);
        if (!deletedProfile) {
            return res.status(404).send('Profile not found');
        }
        res.send(deletedProfile);
    } catch (error) {
        res.status(500).send(error.message);
    }
}
