-- name: create-new-publisher<!
INSERT INTO publishers (name, profile_picture, banner, bio, address, postal_code, state, country, office_phone_number, mobile_phone_number, user_id)
VALUES (:name, :profile_picture, :banner, :bio, :address, :postal_code, :state, :country, :office_phone_number, :mobile_phone_number, :user_id)
RETURNING
    id, created_at, updated_at;


-- name: read-publishers
SELECT  id,
        name,
        profile_picture,
        banner,
        bio,
        address,
        postal_code,
        state,
        country,
        office_phone_number,
        mobile_phone_number,
        user_id
FROM publishers;


-- name: read-publisher-by-user-id^
SELECT  id,
        name,
        profile_picture,
        banner,
        bio,
        address,
        postal_code,
        state,
        country,
        office_phone_number,
        mobile_phone_number,
        user_id,
        created_at,
        updated_at
FROM publishers
WHERE user_id = :user_id
LIMIT 1;


-- name: update-publisher-by-id<!
UPDATE
    publishers
SET name                = :new_name,
    profile_picture     = :new_profile_picture,
    banner              = :new_banner,
    bio                 = :new_bio,
    address             = :new_address,
    postal_code         = :new_postal_code,
    state               = :new_state,
    country             = :new_country,
    office_phone_number = :new_office_phone_number,
    mobile_phone_number = :new_mobile_phone_number
WHERE id = :id
RETURNING
    updated_at;
