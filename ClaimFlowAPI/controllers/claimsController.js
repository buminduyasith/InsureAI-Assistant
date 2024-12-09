const express = require('express');
const router = express.Router();

const claims = [
    { claim_id: '98765', status: 'In Review', last_updated: '2024-12-01' },
];

router.get('/', (req, res) => {
    const { claim_id } = req.query;

    if (!claim_id) {
        return res.status(400).json({ error: 'claim_id is required' });
    }

    const claim = claims.find((c) => c.claim_id === claim_id);
    if (claim) {
        return res.status(200).json(claim);
    }

    return res.status(404).json({ error: 'Claim not found', claim_id });
});

router.post('/', (req, res) => {
    const { policy_id, damage_description, vehicle, photos } = req.body;

    if (!policy_id || !damage_description || !vehicle) {
        return res
            .status(400)
            .json({ error: 'Missing required fields: policy_id, damage_description, vehicle' });
    }

    const newClaim = {
        claim_id: Math.floor(Math.random() * 100000).toString(),
        message: 'Claim submitted successfully.',
    };

    claims.push({ ...newClaim, policy_id, damage_description, vehicle, photos });
    return res.status(201).json(newClaim);
});

module.exports = router;