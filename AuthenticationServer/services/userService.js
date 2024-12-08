const db = require("./dbService");

async function getUserByEmail(email) {
    const result = await db.query("SELECT * FROM users WHERE email = $1", [email]);
    return result.rows[0];
}

async function getRoleByName(roleName) {
    const result = await db.query("SELECT * FROM roles WHERE role_name = $1", [roleName]);
    return result.rows[0];
}

module.exports = {
    getUserByEmail,
    getRoleByName
};