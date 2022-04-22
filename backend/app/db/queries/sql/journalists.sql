-- name: create-new-journalist<!
INSERT INTO journalists (first_name, last_name, profile_picture, bio, user_id)
VALUES (:first_name, :last_name, :profile_picture, :bio, :user_id)
RETURNING
    id, created_at, updated_at;
