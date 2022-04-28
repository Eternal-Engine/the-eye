-- name: create-new-tag<!
INSERT INTO tags (prefix, hashtag)
VALUES (:prefix, :hashtag)
RETURNING
    id, created_at, update_at

-- name: read-tags
SELECT  id,
        hashtag
FROM tags

-- name: read-tag-by-hashtag^
SELECT  id,
        hashtag
FROM tags
WHERE hashtag = :hashtag

