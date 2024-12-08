
var jwt = require('jsonwebtoken');

const createJwtToken = (payload) => {
    const options = { expiresIn: '8h' }; 
    return jwt.sign(payload, process.env.JWT_KeySECRET_KEY, options);
}

module.exports = {
    createJwtToken
}