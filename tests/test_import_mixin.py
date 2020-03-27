"""Tests for the import mixin."""
import io
from tablib import Dataset

from django.http import HttpRequest
from hypothesis import given
from hypothesis.extra.django import TestCase
import hypothesis.strategies as st
from import_export.results import Result

from example.resources import ExampleModelResource
from example.views import ExampleImportView
from lib_import.exceptions import ImportError
from lib_import.resources import ImportModelResource
from lib_import.views import ImportMixin, ImportView
from tests.utils import TestImportToolsMixin


class TestImportMixin(
        TestCase,
        ImportMixin,
        TestImportToolsMixin
):

    def setUp(self):
        self.request = HttpRequest()

    def test_get_filename_without_file(self):
        """Tests that if no file in request an ImportError is raised."""
        self.assertRaises(
            ImportError,
            self.get_filename,
            self.request
        )

    def test_get_filename_one_file(self):
        """Tests that 1 file in request, correct filename is returned."""
        file_name = "file_name"
        self.request.FILES[file_name] = self.create_uploaded_file()
        filename = self.get_filename(self.request)
        self.assertEqual(filename, file_name)

    def test_get_filename_several_file(self):
        """Tests that if several files in request, ImportError is raised."""
        file_name1 = "file_name1"
        file_name2 = "file_name2"
        self.request.FILES[file_name1] = self.create_uploaded_file()
        self.request.FILES[file_name2] = self.create_uploaded_file()
        self.assertRaises(
            ImportError,
            self.get_filename,
            self.request
        )

    def test_get_file_present(self):
        """If filename is in file returns input_file."""
        file_name = "file_name"
        created_file = self.create_uploaded_file(
            name=file_name
        )
        self.request.FILES[file_name] = created_file
        input_file = self.get_file(self.request, file_name)
        self.assertEqual(input_file, created_file)

    def test_get_file_absent(self):
        """If filename is not in FILES, raises an error."""
        self.assertRaises(
            ImportError,
            self.get_file,
            self.request,
            'absent_file'
        )

    def test_file_to_dataset_correct(self):
        """If input file can be decoded returns correct dataset."""
        dataset = Dataset()
        dataset.append_col(['row1', 'row2'])
        dataset.headers = ['col1']
        encoded_dataset = dataset.export('csv').encode('utf-8')

        bio = io.BytesIO(encoded_dataset)
        uploaded_file = self.create_uploaded_file(
            file=bio,
        )
        uploaded_dataset, error_msg = self.file_to_dataset(uploaded_file)

        self.assertEqual(
            uploaded_dataset.dict,
            dataset.dict,
        )
        self.assertEqual(
            uploaded_dataset.headers,
            dataset.headers,
        )
        self.assertIsNone(error_msg)

    def test_file_to_dataset_incorrect(self):
        """If input file is not correctly decoded, returns an error."""
        dataset = Dataset()
        dataset.append_col(['row1', 'row2'])
        dataset.headers = ['col1']
        encoded_dataset = dataset.export('csv').encode('utf-16')

        bio = io.BytesIO(encoded_dataset)
        uploaded_file = self.create_uploaded_file(
            file=bio,
        )
        uploaded_dataset, error_msg = self.file_to_dataset(uploaded_file)

        self.assertIsNone(uploaded_dataset)
        self.assertIsNotNone(error_msg)

    @given(skip_update=st.booleans())
    def test_initialize_resource(self, skip_update):
        """Resource.skip_update is set to skip_update."""
        resource = ImportModelResource(skip_update=skip_update)
        self.assertEqual(resource.skip_update, skip_update)

    def test_import_file(self):
        file_name = "file_name"
        dataset = self.create_input_dataset()
        file = self.encode_dataset_to_bio(dataset)
        self.request.FILES[file_name] = self.create_uploaded_file(
            field_name=file_name,
            file=file,
        )

        resource_class = ExampleModelResource
        skip_update = True

        result, error_msg = self.import_file(
            self.request,
            resource_class,
            skip_update
        )
        self.assertIsNotNone(result)
        self.assertIsNone(error_msg)

    def test_adapt_context(self):
        result = Result()
        result.totals['new'] = 1
        result.totals['update'] = 2
        result.totals['delete'] = 3
        result.totals['skip'] = 4
        result.totals['error'] = 5
        result.totals['invalid'] = 6
        error_msg = "lalala"
        context = self.adapt_context(result, error_msg)

        self.assertEqual(
            context,
            {
                'new_rows': 1,
                'update_rows': 2,
                'delete_rows': 3,
                'skip_rows': 4,
                'error_rows': 5,
                'invalid_rows': 6,
                'error_msg': error_msg
            }
        )


class TestImportView(
        TestCase,
        ImportView,
        TestImportToolsMixin
):

    def setUp(self):
        self.request = HttpRequest()

    def test_set_skip_update(self):
        self.request.POST['import_type'] = 'create_only'
        skip_update = self.set_skip_update(self.request)
        self.assertEqual(skip_update, True)

        self.request.POST['import_type'] = 'blabla'
        skip_update = self.set_skip_update(self.request)
        self.assertEqual(skip_update, False)

    def test_post(self):
        request = HttpRequest()
        request.POST['import_type'] = 'create_only'
        file_name = "file_name"
        dataset = self.create_input_dataset()
        file = self.encode_dataset_to_bio(dataset)
        request.FILES[file_name] = self.create_uploaded_file(
            field_name=file_name,
            file=file,
        )
        import_view = ExampleImportView()
        import_view.post(request=request)
