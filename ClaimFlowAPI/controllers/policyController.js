const express = require('express');
const router = express.Router();

const policyDetails = [
    { userId: "09cb0a5b-d34a-458e-84a9-cf1c7c8bc53e", policyName: "Gold Plan"},
];

router.get('/', (req, res) => {
    const { user_id } = req.query;

    if (!user_id) {
        return res.status(400).json({ error: 'user id is required' });
    }

    const policy = policyDetails.find((c) => c.userId === user_id);
    if (policy) {
        return res.status(200).json(policy);
    }

    return res.status(404).json({ error: 'No insurance policy found for this user.', user_id });
});

module.exports = router;