-- name: create-new-user<!
INSERT INTO users (username, email, salt, hashed_password, is_publisher, is_verified, is_active)
VALUES (:username, :email, :salt, :hashed_password, :is_publisher, :is_verified, :is_active)
RETURNING
    id, created_at, updated_at;


-- name: read-users
SELECT id,
       username,
       email,
       is_publisher,
       is_verified,
       is_active
FROM users;


-- name: read-user-by-id^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       is_publisher,
       is_verified,
       is_active,
       created_at,
       updated_at
FROM users
WHERE id = :id
LIMIT 1;


-- name: read-user-by-username^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       is_publisher,
       is_verified,
       is_active,
       created_at,
       updated_at
FROM users
WHERE username = :username
LIMIT 1;


-- name: read-user-by-email^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       is_publisher,
       is_verified,
       is_active,
       created_at,
       updated_at
FROM users
WHERE email = :email
LIMIT 1;


-- name: update-user-by-id<!
UPDATE
    users
SET username        = :new_username,
    email           = :new_email,
    salt            = :new_salt,
    hashed_password = :new_password,
    is_publisher    = :new_is_publisher
WHERE id = :id
RETURNING
    updated_at;


-- name: update-user-by-username<!
UPDATE
    users
SET username        = :new_username,
    email           = :new_email,
    salt            = :new_salt,
    hashed_password = :new_password,
    is_publisher    = :new_is_publisher
WHERE username = :username
RETURNING
    updated_at;


-- name: delete-user-by-id<!
DELETE
FROM users
WHERE id = :id;


-- name: delete-user-by-username<!
DELETE
FROM users
WHERE username = :username;


-- name: delete-user-by-email<!
DELETE
FROM users
WHERE email = :email;
