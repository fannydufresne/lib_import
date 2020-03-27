"""Tests contracts module."""

from tablib import Dataset

from django.test import TestCase
from import_export.results import Result
from import_export.resources import Resource

import lib_import.contracts as co
from lib_import.resources import ImportModelResource
from tests.utils import TestImportToolsMixin


class TestContracts(
    TestCase,
    TestImportToolsMixin,
):

    def test_InMemoryUploadedFileType(self):
        x = self.create_uploaded_file()
        self.assertEqual(co.InMemoryUploadedFileType(x), None)
        x = 'aaa'
        self.assertRaises(ValueError, co.InMemoryUploadedFileType, x)

    def test_ResultType(self):
        x = Result()
        self.assertEqual(co.ResultType(x), None)
        x = 'aaa'
        self.assertRaises(ValueError, co.ResultType, x)

    def test_DatasetType(self):
        x = Dataset()
        self.assertEqual(co.DatasetType(x), None)
        x = 'aaa'
        self.assertRaises(ValueError, co.DatasetType, x)

    def test_ResourceType(self):
        x = Resource()
        self.assertEqual(co.ResourceType(x), None)
        x = 'aaa'
        self.assertRaises(ValueError, co.ResourceType, x)

    def test_ImportModelResourceSubclass(self):

        class SubClass(ImportModelResource):
            pass

        self.assertEqual(co.ImportModelResourceSubclass(SubClass), None)

        class SubClass(object):
            pass

        self.assertRaises(
            ValueError,
            co.ImportModelResourceSubclass,
            SubClass,
        )
