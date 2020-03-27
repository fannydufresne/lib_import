"""Utils for tests."""

import io
from tablib import Dataset

from django.core.files.uploadedfile import InMemoryUploadedFile


class TestImportToolsMixin:
    def create_uploaded_file(
            self,
            file="",
            field_name="",
            name="",
            content_type="",
            size="",
            charset=""):

        return InMemoryUploadedFile(
                file=file,
                field_name=field_name,
                name=name,
                content_type=content_type,
                size=size,
                charset=charset
            )

    def create_input_dataset(self):
        dataset = Dataset()
        dataset.append_col(['name1', 'name2', 'name3'])
        dataset.headers = ['name']

        return dataset

    def encode_dataset_to_bio(self, dataset):
        encoded_dataset = dataset.export('csv').encode('utf-8')
        bio = io.BytesIO(encoded_dataset)
        return bio
