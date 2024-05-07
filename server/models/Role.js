// models/Role.js
const mongoose = require('mongoose');

const roleSchema = new mongoose.Schema({
    name: { type: String, required: true },
    uuid: { type: String, required: true, unique: true },
    description: { type: String, required: false },
    model: { type: String, required: true },
    tools: [{ type: String }],
});

const Role = mongoose.model('Role', roleSchema);

module.exports = Role;