# import jwt
# import pytest
# import datetime

# from app.models.domain import users as users_domain
# from app.services.jwt import (
#     ALGORITHM,
#     create_access_token,
#     generate_jwt_token,
#     get_username_from_token,
# )


# def test_creating_jwt_token() -> None:

#     token = generate_jwt_token(
#         jwt_content={"content": "payload"},
#         secret_key="SECRET_JWT",
#         expires_delta=datetime.timedelta(minutes=1),
#     )
#     parsed_payload = jwt.decode(token, "SECRET_JWT", algorithms=[ALGORITHM])

#     assert parsed_payload["content"] == "payload"


# def test_creating_token_for_user(test_user: users_domain.UserInDB) -> None:

#     token = create_access_token(user=test_user, secret_key="SECRET_JWT")
#     parsed_payload = jwt.decode(token, "SECRET_JWT", algorithms=[ALGORITHM])

#     assert parsed_payload["username"] == test_user.username


# def test_retrieving_token_from_user(test_user: users_domain.UserInDB) -> None:

#     token = create_access_token(user=test_user, secret_key="SECRET_JWT")
#     username = get_username_from_token(token, "SECRET_JWT")

#     assert username == test_user.username


# def test_error_when_wrong_token() -> None:

#     with pytest.raises(ValueError):

#         get_username_from_token("JWT_TOKEN", "SECRET_KEY")


# def test_error_when_wrong_token_shape() -> None:
#     token = generate_jwt_token(
#         jwt_content={"content": "payload"},
#         secret_key="SECRET_JWT",
#         expires_delta=datetime.timedelta(minutes=1),
#     )
#     with pytest.raises(ValueError):
#         get_username_from_token(token, "SECRET_JWT")
