# fmt: off
import unittest

from pydantic import BaseSettings

from app.core.config import Settings, get_settings


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.pydantic_base_settings = BaseSettings()
        self.settings = Settings()
        self.settings_from_get_settings = get_settings()

    def test_create_settings(self):

        self.assertTrue(
            issubclass(
                type(self.settings),
                type(self.pydantic_base_settings),
            )
        )
        self.assertEqual("Application Settings", self.settings.__str__())
        self.assertEqual("dev", self.settings.ENV)
        self.assertEqual("sqlite:///iW_dev.sqlite3", self.settings.database_url)

        # Test settings attributes for rewritting FastAPI default attrs
        self.assertEqual("iWitness - Backend Development Application", self.settings.title),
        self.assertEqual(
            "A backend project with FastAPI for iWitness web application.",
            self.settings.description,
        ),
        self.assertEqual("0.0.0", self.settings.version),
        self.assertEqual(True, self.settings.debug),
        self.assertEqual("/docs", self.settings.docs_url),
        self.assertEqual("", self.settings.openapi_prefix),
        self.assertEqual("/openapi.json", self.settings.openapi_url),
        self.assertEqual("/redoc", self.settings.redoc_url)

    def test_retrieve_settings_from_get_settings(self):

        expected = {
            "title": "iWitness - Backend Development Application",
            "description": "A backend project with FastAPI for iWitness web application.",
            "version": "0.0.0",
            "debug": True,
            "docs_url": "/docs",
            "openapi_prefix": "",
            "openapi_url": "/openapi.json",
            "redoc_url": "/redoc",
        }
        self.assertIsInstance(self.settings_from_get_settings, type(self.settings))
        self.assertEqual(self.settings_from_get_settings, self.settings)
        self.assertEqual(expected, self.settings_from_get_settings.fastapi_kwargs)
