// roleRoutes.js
const express = require('express');
const router = express.Router();
const roleController = require('../controllers/roleController');

router.get('/roles', roleController.getRoles);
// router.put('/roles/:id', roleController.updateRole);
// router.delete('/roles/:id', roleController.deleteRole);
// router.post('/roles', roleController.createRole);

module.exports = router;