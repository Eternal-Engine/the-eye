-- name: create-new-journalist<!
INSERT INTO journalists (first_name, last_name, profile_picture, bio, user_id)
VALUES (:first_name, :last_name, :profile_picture, :bio, :user_id)
RETURNING
    id, created_at, updated_at;


-- name: read-journalist-by-user-id^
SELECT  id,
        first_name,
        last_name,
        profile_picture,
        bio,
        user_id,
        created_at,
        updated_at
FROM journalists
WHERE user_id = :user_id
LIMIT 1;


-- name: update-journalist-by-id<!
UPDATE
    journalists
SET first_name      = :new_first_name,
    last_name       = :new_last_name,
    profile_picture = :new_profile_picture,
    bio             = :new_bio
WHERE id = :id
RETURNING
    updated_at;
