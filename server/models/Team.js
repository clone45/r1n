// models/Team.js
const mongoose = require('mongoose');

const teamSchema = new mongoose.Schema({
    name: { type: String, required: true },
    uuid: { type: String, required: true, unique: true },
    description: String,
    logo: String,
    profile_uuids: [String]
});

const Team = mongoose.model('Team', teamSchema);

module.exports = Team;
