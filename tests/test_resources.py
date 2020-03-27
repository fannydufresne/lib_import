"""Tests lib_import resources."""

from django.test import TestCase

from lib_import.resources import ImportModelResource
from example.models import ExampleModel
from example.resources import ExampleModelResource


class TestImportModelResource(TestCase):

    def test_init(self):
        # True
        resource = ImportModelResource(skip_update=True)
        self.assertEqual(resource.skip_update, True)

        # False
        resource = ImportModelResource(skip_update=False)
        self.assertEqual(resource.skip_update, False)

        # None
        resource = ImportModelResource()
        self.assertEqual(resource.skip_update, False)

    def test_skip_row(self):
        # Creates two objects
        obj1 = ExampleModel.objects.create(name='obj1')
        obj2 = ExampleModel.objects.create(name='obj2')

        # When skip_update is True, update rows are ignored
        resource = ExampleModelResource(skip_update=True)
        skip = resource.skip_row(obj1, obj1)
        self.assertEqual(skip, True)
        skip = resource.skip_row(obj1, obj2)
        self.assertEqual(skip, False)

        # When skip_update is True, update rows are not ignored
        resource = ExampleModelResource(skip_update=False)
        skip = resource.skip_row(obj1, obj1)
        self.assertEqual(skip, False)
        skip = resource.skip_row(obj1, obj2)
        self.assertEqual(skip, False)
