const express = require("express");
const {createJwtToken, verifyJwtToken} = require("../services/jwtService")
const router = express.Router();

router.get('/introspect', (req, res) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
        return res.status(400).json({ error: 'Token is required' });
    }
    try {
        const claims = verifyJwtToken(token);
        res.status(200).json({ success: true, claims });
    } catch (error) {
        res.status(401).json({ success: false, error: error.message });
    }
});

module.exports = router;
