--CREATE EXTENSION IF NOT EXISTS "uuid-ossp";  -- enable uuid generation

INSERT INTO Roles (id, name)
VALUES ('d069c5b7-52f6-434d-b04d-190ef34a55ce', 'Admin'), ('5bcd7efd-33dd-4f1e-8b8a-560aef9406de', 'User');

INSERT INTO users (id, first_name, last_name, email, password, created_at, updated_at)
VALUES (uuid_generate_v4(), 'bumindu', 'yasith', 'bumindu@gmail.com', '$2b$10$TX2CGcXsFnP97dJhp.uiYejfH4SwaI60Q19Fc445Fp5dpcTuvWn3.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


INSERT INTO users (id, first_name, last_name, email, password, created_at, updated_at)
VALUES (uuid_generate_v4(), 'John', 'smith', 'john@gmail.com', '$2b$10$TX2CGcXsFnP97dJhp.uiYejfH4SwaI60Q19Fc445Fp5dpcTuvWn3.', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Link admin user with the Admin role
INSERT INTO userroles (user_id, role_id)
VALUES ((SELECT id FROM users WHERE email = 'bumindu@gmail.com'), (SELECT id FROM roles WHERE name = 'Admin'));

INSERT INTO userroles (user_id, role_id)
VALUES ((SELECT id FROM users WHERE email = 'john@gmail.com'), (SELECT id FROM roles WHERE name = 'User'));