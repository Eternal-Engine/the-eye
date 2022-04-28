-- name: create-new-article<!
WITH author_subquery AS (
SELECT id, username
FROM users
WHERE username = :author_username
) 
INSERT INTO articles (headline, slug, description, body, is_drafted, author_id)
VALUES (:headline, :slug, :description, :body, :is_drafted, (SELECT id FROM author_subquery))
RETURNING
    id,
    headline,
    slug,
    description,
    body,
    is_drafted, 
    (SELECT username FROM author_subquery) as author_username,
    created_at,
    updated_at;


-- name: read-articles
SELECT  id,
        headline,
        slug,
        description,
        body,
        author_id,
        is_drafted,
        created_at,
        updated_at
FROM articles;


-- name: read-article-by-id^
SELECT  id,
        headline,
        slug,
        description,
        body,
        author_id,
        is_drafted,
        created_at,
        updated_at
FROM articles
WHERE id = :id
LIMIT 1;


-- name: read-article-by-headline^
SELECT  id,
        headline,
        slug,
        description,
        body,
        author_id,
        is_drafted,
        created_at,
        updated_at
FROM articles
WHERE headline = :headline
LIMIT 1;


-- name: update-article-by-id<!
UPDATE
    articles
SET headline    = :headline,
    description = :description,
    body        = :body
WHERE id = :id
RETURNING
    updated_at;


-- name: delete-article-by-id<!
DELETE
FROM articles
WHERE id = :id;

