from app.services.config import SecurtiySettings


def test_security_settings_construction():

    settings = SecurtiySettings()

    assert isinstance(settings.ACCESS_TOKEN_EXPIRE_MINUTES, int)
    assert isinstance(settings.ALGORITHM_JWT, str)
    assert isinstance(settings.ALGORITHM_LAYER_1, str)
    assert isinstance(settings.SECRET_KEY_LAYER_1, str)
    assert isinstance(settings.ALGORITHM_LAYER_2, str)
    assert isinstance(settings.JWT_SUBJECT, str)
    assert str(settings) == "Security Settings for Services"
