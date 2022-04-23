-- name: create-new-journalist<!
INSERT INTO journalists (first_name, last_name, profile_picture, banner, bio, address, postal_code, state, country, office_phone_number, mobile_phone_number, user_id)
VALUES (:first_name, :last_name, :profile_picture, :banner, :bio, :address, :postal_code, :state, :country, :office_phone_number, :mobile_phone_number, :user_id)
RETURNING
    id, created_at, updated_at;


-- name: read-journalist-by-user-id^
SELECT  id,
        first_name,
        last_name,
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
FROM journalists
WHERE user_id = :user_id
LIMIT 1;


-- name: update-journalist-by-id<!
UPDATE
    journalists
SET first_name      = :new_first_name,
    last_name       = :new_last_name,
    profile_picture = :new_profile_picture,
    banner          = :new_banner,
    bio             = :new_bio,
    address         = :new_address,
    postal_code     = :new_postal_code,
    state           = :new_state,
    country         = :new_country,
    office_phone_number = :new_office_phone_number,
    mobile_phone_number = :new_mobile_phone_number
WHERE id = :id
RETURNING
    updated_at;
