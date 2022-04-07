# fmt: off
import unittest

from app.core.settings.app_base_settings import AppBaseSettings, EnvTypes
from app.core.settings.app_settings import AppSettings


class TestAppSettings(unittest.TestCase):
    def setUp(self):
        self.app_base_settings = AppBaseSettings()
        self.app_settings = AppSettings()

    def test_create_app_settings(self):

        self.assertTrue(
            issubclass(
                type(self.app_settings),
                type(self.app_base_settings),
            )
        )
        self.assertEqual(self.app_base_settings.app_env, self.app_settings.app_env)
        self.assertEqual("Application Settings", self.app_settings.__str__())
        self.assertEqual("prod", self.app_settings.app_env.value)
        self.assertEqual("PROD", self.app_settings.app_env.name)
        self.assertEqual("iWitness - Backend Production Environment Settings", self.app_settings.title),
        self.assertEqual(
            "A backend project with FastAPI for iWitness web application.",
            self.app_settings.description,
        ),
        self.assertEqual("0.0.0", self.app_settings.version),
        self.assertEqual(False, self.app_settings.debug),
        self.assertEqual("/docs", self.app_settings.docs_url),
        self.assertEqual("/api", self.app_settings.api_prefix),
        self.assertEqual("", self.app_settings.openapi_prefix),
        self.assertEqual("/openapi.json", self.app_settings.openapi_url),
        self.assertEqual("/redoc", self.app_settings.redoc_url)
        self.assertEqual("env/.env.production", self.app_settings.Config.env_file)
        self.assertEqual(True, self.app_settings.Config.validate_assignment)

    def test_retrieve_app_settings_attributes_for_fastapi_setup(self):

        expected = {
            "title": "iWitness - Backend Production Environment Settings",
            "description": "A backend project with FastAPI for iWitness web application.",
            "version": "0.0.0",
            "debug": False,
            "docs_url": "/docs",
            "openapi_prefix": "",
            "api_prefix": "/api",
            "openapi_url": "/openapi.json",
            "redoc_url": "/redoc",
            "app_env": EnvTypes.PROD,
        }

        self.assertEqual(expected, self.app_settings.fastapi_kwargs)
