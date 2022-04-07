# fmt: off
from backend import app


def test_app_version():

    assert app.__version__ == "0.1.0"
