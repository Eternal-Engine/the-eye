import unittest

from pydantic import BaseSettings

from app.core.config import Settings, get_settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.pydantic_base_settings = BaseSettings()
        self.settings = Settings()
        self.settings_from_get_settings = get_settings()

    def test_create_settings(self):

        settings = self.settings
        pydantic_base_settings = self.pydantic_base_settings
        self.assertTrue(
            issubclass(
                type(settings),
                type(pydantic_base_settings),
            )
        )
        self.assertEqual("Application Settings", settings.__str__())
        self.assertEqual("dev", settings.ENV)
        self.assertEqual("sqlite:///iW_dev.sqlite3", settings.database_url)

        # Settings attributes for FastAPI setup
        self.assertEqual("iWitness - Backend Development Application", settings.title),
        self.assertEqual(
            "A backend project with FastAPI for iWitness web application.",
            settings.description,
        ),
        self.assertEqual("0.0.0", settings.version),
        self.assertEqual(True, settings.debug),
        self.assertEqual("/docs", settings.docs_url),
        self.assertEqual("", settings.openapi_prefix),
        self.assertEqual("openapi.json", settings.openapi_url),
        self.assertEqual("/redoc", settings.redoc_url)

    def test_retrieve_settings_from_get_settings(self):

        settings = self.settings
        settings_from_get_settings = self.settings_from_get_settings
        expected = {
            "title": "iWitness - Backend Development Application",
            "description": "A backend project with FastAPI for iWitness web application.",
            "version": "0.0.0",
            "debug": True,
            "docs_url": "/docs",
            "openapi_prefix": "",
            "openapi_url": "openapi.json",
            "redoc_url": "/redoc",
        }
        self.assertIsInstance(settings_from_get_settings, type(settings))
        self.assertEqual(settings_from_get_settings, settings)
        self.assertEqual(expected, settings_from_get_settings.fastapi_kwargs)
