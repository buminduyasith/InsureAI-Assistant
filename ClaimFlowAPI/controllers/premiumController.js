const express = require('express');
const router = express.Router();

router.post('/', (req, res) => {
    const { policy_id, current_coverage, new_coverage } = req.body;

    if (!policy_id || typeof current_coverage !== 'number' || typeof new_coverage !== 'number') {
        return res.status(400).json({ error: 'Missing or invalid required fields.' });
    }

    if (new_coverage <= current_coverage) {
        return res.status(422).json({
            error: "Invalid coverage amounts. 'new_coverage' must be greater than 'current_coverage'.",
        });
    }

    const premium = {
        policy_id,
        current_premium: current_coverage * 0.05,
        new_premium: new_coverage * 0.05,
    };

    return res.status(200).json(premium);
});

module.exports = router;
