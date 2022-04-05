import unittest

from pydantic import PostgresDsn

from app.core.settings.app_base_settings import EnvTypes
from app.core.settings.app_dev_settings import AppDevSettings
from app.core.settings.app_prod_settings import AppProdSettings
from app.core.settings.app_settings import AppSettings
from app.core.settings.app_test_settings import AppTestSettings


class TestAllAppSettingsChildClasses(unittest.TestCase):
    def setUp(self):
        self.app_settings = AppSettings()
        self.app_prod_settings = AppProdSettings()
        self.app_dev_settings = AppDevSettings()
        self.app_test_settings = AppTestSettings()
        self.expected = {
            "app_env": EnvTypes.PROD,
            "title": "iWitness - Backend Production Environment Settings",
            "description": "A backend project with FastAPI for iWitness web application.",
            "version": "0.0.0",
            "debug": False,
            "database_url": PostgresDsn(
                "postgresql+asyncpg://postgres:postgres@localhost:5432/iW_prod",
                scheme="postgresql+asyncpg",
                user="postgres",
                password="postgres",
                host="localhost",
                host_type="int_domain",
                port="5432",
                path="/iW_prod",
            ),
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "openapi_url": "/openapi.json",
            "api_prefix": "/api",
            "openapi_prefix": "",
            "jwt_token_prefix": "Token",
            "allowed_hosts": ["*"],
        }

    def test_create_app_prod_settings(self):

        self.assertTrue(
            issubclass(
                type(self.app_prod_settings),
                type(self.app_settings),
            )
        )
        self.assertEqual(self.expected, self.app_prod_settings.dict(exclude={"secret_key"}))
        self.assertEqual("env/prod_env/prod.env", self.app_prod_settings.Config.env_file)
        self.assertEqual(True, self.app_prod_settings.Config.validate_assignment)

    def test_create_app_dev_settings(self):

        self.expected["app_env"] = EnvTypes.DEV
        self.app_dev_settings.app_env = self.expected["app_env"]
        self.expected["title"] = "iWitness - Backend Development Environment Settings"
        self.expected["debug"] = True
        self.expected["database_url"] = PostgresDsn(
            "postgresql+asyncpg://postgres:postgres@localhost:5432/iW_dev",
            scheme="postgresql+asyncpg",
            user="postgres",
            password="postgres",
            host="localhost",
            host_type="int_domain",
            port="5432",
            path="/iW_dev",
        )

        self.assertTrue(
            issubclass(
                type(self.app_dev_settings),
                type(self.app_settings),
            )
        )
        self.assertEqual(self.expected, self.app_dev_settings.dict(exclude={"secret_key"}))
        self.assertEqual("env/dev_env/dev.env", self.app_dev_settings.Config.env_file)
        self.assertEqual(True, self.app_dev_settings.Config.validate_assignment)

    def test_create_app_test_settings(self):

        self.expected["app_env"] = EnvTypes.TEST
        self.app_test_settings.app_env = self.expected["app_env"]
        self.expected["title"] = "iWitness - Backend Test Environment Settings"
        self.expected["debug"] = True
        self.expected["database_url"] = "sqlite+aiosqlite:///iW_test.sqlite3"

        self.assertTrue(
            issubclass(
                type(self.app_test_settings),
                type(self.app_settings),
            )
        )
        self.assertEqual(self.expected, self.app_test_settings.dict(exclude={"secret_key"}))
        self.assertEqual("env/test_env/test.env", self.app_test_settings.Config.env_file)
        self.assertEqual(True, self.app_test_settings.Config.validate_assignment)
