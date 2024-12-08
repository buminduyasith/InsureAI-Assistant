CREATE TABLE Users (
    id UUID PRIMARY KEY,            -- UUID for the user ID
    first_name VARCHAR(50) NOT NULL,  -- VARCHAR for the first name
    last_name VARCHAR(50) NOT NULL,   -- VARCHAR for the last name
    email VARCHAR(100) NOT NULL UNIQUE, -- VARCHAR for the email
    password TEXT NOT NULL,          -- TEXT for storing hashed passwords
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the record was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for when the record was last updated
);

CREATE TABLE Roles (
    id UUID PRIMARY KEY,          -- UUID for the role ID
    name VARCHAR(50) NOT NULL UNIQUE, -- VARCHAR for the role name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the record was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for when the record was last updated
);

CREATE TABLE UserRoles (
    user_id UUID REFERENCES Users(id) ON DELETE CASCADE,  -- Foreign key to the Users table
    role_id UUID REFERENCES Roles(id) ON DELETE CASCADE,  -- Foreign key to the Roles table
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the record was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Timestamp for when the record was last updated
    PRIMARY KEY (user_id, role_id) -- Composite primary key to ensure a user can only have one role per table entry
);