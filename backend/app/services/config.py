import decouple


class SecuritySettings:

    ALGORITHM_LAYER_1 = decouple.config("ALGORITHM_LAYER_1", cast=str)
    ALGORITHM_LAYER_2 = decouple.config("ALGORITHM_LAYER_2", cast=str)
    ALGORITHM_JWT = decouple.config("ALGORITHM_JWT", cast=str)

    SECRET_KEY_LAYER_1 = decouple.config("SECRET_KEY_LAYER_1", cast=str)
    SECRET_KEY_JWT = decouple.config("SECRET_KEY_JWT", cast=str)

    JWT_SUBJECT = decouple.config("JWT_SUBJECT", cast=str)
    ACCESS_TOKEN_EXPIRE_MINUTES = (
        decouple.config("MIN", cast=int) * decouple.config("HOUR", cast=int) * decouple.config("DAY", cast=int)
    )

    def __str__(self):
        return "Security Settings for Services"
