# fmt: off
import unittest

from app.core.settings.app import AppSettings
from app.core.settings.base import EnvTypes
from app.core.settings.development import AppDevSettings
from app.core.settings.production import AppProdSettings
from app.core.settings.staging import AppStagingSettings


class TestProdDevStagingSettings(unittest.TestCase):
    def setUp(self):
        self.app_settings = AppSettings()
        self.app_prod_settings = AppProdSettings()
        self.app_dev_settings = AppDevSettings()
        self.app_test_settings = AppStagingSettings()
        self.expected = {
            "app_env": EnvTypes.PROD,
            "title": "iWitness - Backend Production Environment Settings",
            "description": "A backend application powered by FastAPI, AsyncPG, and PostgresQL.",
            "version": "0.0.0",
            "debug": False,
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "openapi_url": "/openapi.json",
            "api_prefix": "/api",
            "openapi_prefix": "",
            "jwt_token_prefix": "Token",
            "allowed_hosts": ["*"],
            "logging_level": 20,
            "loggers": ("uvicorn.asgi", "uvicorn.access"),
            "max_connection_count": 10,
            "min_connection_count": 10,
        }

    def test_create_app_prod_settings(self):

        self.assertTrue(
            issubclass(
                type(self.app_prod_settings),
                type(self.app_settings),
            )
        )
        self.assertEqual(self.expected, self.app_prod_settings.dict(exclude={"secret_key", "database_url"}))
        self.assertEqual(True, self.app_prod_settings.Config.validate_assignment)

    def test_create_app_dev_settings(self):

        self.expected["app_env"] = EnvTypes.DEV
        self.app_dev_settings.app_env = self.expected["app_env"]
        self.expected["title"] = "iWitness - Backend Development Environment Settings"
        self.expected["debug"] = True

        self.assertTrue(
            issubclass(
                type(self.app_dev_settings),
                type(self.app_settings),
            )
        )
        self.assertEqual(self.expected, self.app_dev_settings.dict(exclude={"secret_key", "database_url"}))
        self.assertEqual(True, self.app_dev_settings.Config.validate_assignment)

    def test_create_app_test_settings(self):

        self.expected["app_env"] = EnvTypes.TEST
        self.app_test_settings.app_env = self.expected["app_env"]
        self.expected["title"] = "iWitness - Backend Test Environment Settings"
        self.expected["debug"] = True

        self.assertTrue(
            issubclass(
                type(self.app_test_settings),
                type(self.app_settings),
            )
        )
        self.assertEqual(self.expected, self.app_test_settings.dict(exclude={"secret_key", "database_url"}))
        self.assertEqual(True, self.app_test_settings.Config.validate_assignment)
