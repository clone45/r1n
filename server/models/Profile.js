// models/Profile.js
const mongoose = require('mongoose');

const profileSchema = new mongoose.Schema({
    name: { type: String, required: true },
    uuid: { type: String, required: true, unique: true },
    role_uuid: { type: String, required: true },
    avatar: String,
    description: String,
    welcome_message: String,
    assistant_id: String,
    vector_stores: [String]
});

const Profile = mongoose.model('Profile', profileSchema);

module.exports = Profile;