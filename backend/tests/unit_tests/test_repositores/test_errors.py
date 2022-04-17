import pytest

from app.db.errors import EntityDoesNotExist


def test_raise_entity_does_not_exist_correctly():
    def my_entity_error():
        raise EntityDoesNotExist("User with id 1 does not exist!")

    with pytest.raises(Exception, match="User with id 1 does not exist!"):
        my_entity_error()
