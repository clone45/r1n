// controllers/roleController.js
const Role = require('../models/Role');

exports.getRoles = async (req, res) => {
    try {
        const roles = await Role.find();

        // Transform _id to id
        const transformedRoles = roles.map(role => {
            const roleObj = role.toObject(); // Convert to plain JavaScript object if needed
            roleObj.id = roleObj._id.toString(); // Convert ObjectId to string and assign to id
            delete roleObj._id; // Remove the original _id property
            return roleObj;
        });

        res.json(transformedRoles);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Server error' });
    }
}
