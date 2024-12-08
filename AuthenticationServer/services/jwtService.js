
var jwt = require('jsonwebtoken');

const createJwtToken = (payload) => {
    const options = { expiresIn: '8h' }; 
    return jwt.sign(payload, process.env.JWT_KeySECRET_KEY, options);
}

const verifyJwtToken = (token) => {
    try {
        const decoded = jwt.verify(token, process.env.JWT_KeySECRET_KEY);
        return decoded;
    } catch (error) {
        if (error.name === 'TokenExpiredError') {
            throw new Error('Token has expired');
        }
        throw new Error('Invalid token');
    }
};

module.exports = {
    createJwtToken,
    verifyJwtToken
}