const db = require("./dbService");

async function getUserByEmail(email) {
    const result = await db.query("SELECT * FROM users WHERE email = $1", [email]);
    return result.rows[0];
}

async function getRoleByName(roleName) {
    const result = await db.query("SELECT * FROM roles WHERE role_name = $1", [roleName]);
    return result.rows[0];
}

async function getUserRoleByUserId(userId) {
    const query = `
        SELECT r.name AS role_name
        FROM users u
        JOIN userroles ur ON u.id = ur.user_id
        JOIN roles r ON ur.role_id = r.id
        WHERE u.id = $1
    `;

    const result = await db.query(query, [userId]);
    return result.rows[0];
}
module.exports = {
    getUserByEmail,
    getRoleByName,
    getUserRoleByUserId
};