def http_400_details(username: str = None, email: str = None) -> str:

    if username:
        return f"The username {username} is taken! Be creative and choose another one!"
    if email:
        return f"The email {email} is taken! Be creative and choose another one!"
    return "Login failed! Re-check heck your email and password!"


HTTP_300_DETAILS = "Unable to validate credentials; Check the JWT token or login credentials!"


def http_404_details(id: int = None, username: str = None) -> str:

    id_msg = f"Either the user with ID {id} "
    username_msg = f"Either the username {username} "
    main_msg = "doesn't exist, has been deleted, or you are not authorized; Check your JWToken for authorization!"

    if id:
        return id_msg + main_msg

    return username_msg + main_msg
