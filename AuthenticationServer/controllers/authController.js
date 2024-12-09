const express = require("express");
const bcrypt = require("bcrypt");
const { getUserByEmail, getUserRoleByUserId } = require("../services/userService");
const {createJwtToken} = require("../services/jwtService")
const router = express.Router();

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

    var roledata = await getUserRoleByUserId(user.id);
    const payload = {
        id:user.id,
        name:user.first_name,
        email:user.email,
        role: roledata.role_name
    }
    var token = createJwtToken(payload)
    return res.status(200).json({token});

});

module.exports = router;
