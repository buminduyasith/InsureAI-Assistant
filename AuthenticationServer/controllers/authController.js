const express = require("express");
const bcrypt = require("bcrypt");
const { getUserByEmail } = require("../services/userService");
const router = express.Router();
var jwt = require('jsonwebtoken');

router.post("/login", async (req, res, next) => {
    var email = req.body.email;
    var password = req.body.password;

    if (!email || !password) {
        res.status(400);
        return  next(new Error("Email and password are required."))
    }

    var user = await getUserByEmail(email);
    if (!user) {
        res.status(401);
        return  next(new Error("Invalid email or password."))
    }

    const isMatched = bcrypt.compareSync(password, user.password);
    if (!isMatched) {
        res.status(401);
        return  next(new Error("Invalid email or password."))
    }

    const payload = {
        id:user.id,
        name:user.first_name,
        email:user.email,
    }

    const options = { expiresIn: '1h' }; 
    const token = jwt.sign(payload, process.env.JWT_KeySECRET_KEY, options);
    return res.status(200).json({token});
});

module.exports = router;
