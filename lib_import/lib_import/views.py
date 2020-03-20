
import logging
from tablib import Dataset

from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView


logger = logging.getLogger(__name__)


class ImportMixin:

    errors = []

    def import_file(self, skip_update):
        """Imports data from dile into database."""

        input_file = self.get_file()
        dataset = self.file_to_dataset(input_file)
        logger.debug('dataset %s', dataset)
        result = self.dataset_to_database(dataset, skip_update)
        return result

    def get_file(self):
        """Extracts file from request."""
        if not self.errors:
            if self.filename is None:
                self.filename = [elm for elm in self.request.FILES][0]
                if len(self.request.FILES) > 1:
                    logger.warning(
                        'Took first file in import but several files were present: %s',
                        self.request.FILES
                    )
            input_file = self.request.FILES[self.filename]
        else:
            input_file = None

        return input_file

    def file_to_dataset(self, input_file):
        """Extracts data from file into a dataset."""
        file_encoding = self.file_encoding()
        file_format = self.file_format()
        if not self.errors:
            try:
                decoded_file = input_file.read().decode(file_encoding)
            except UnicodeDecodeError:
                decoded_file = None
                self.errors.append('UnicodeDecodeError')
                logger.debug('in unicodedecodeerror')
        if not self.errors:
            dataset = Dataset().load(
                decoded_file,
                format=file_format,
            )
        else:
            dataset = None

        return dataset

    def file_encoding(self):
        """Gets file encoding."""

        return 'utf-8'

    def file_format(self):
        """Gets file format."""

        return 'csv'

    def dataset_to_database(self, dataset, skip_update):
        """Saves data from dataset into database."""
        if not self.errors:
            result = self.resource_class(skip_update=skip_update).import_data(
                dataset,
                dry_run=False,
            )
        # TODO : maybe put in a transaction
        else:
            result = None
        return result

    def adapt_context(self, result, context={}):
        if self.errors:
            if 'UnicodeDecodeError' in self.errors:
                logger.info('There is an error in encoding or format')
                context['errors'] = _('import_error_in_encoding_or_format')
        context = self.analyze_errors(
            result,
            context=context,
        )

        return context

    def analyze_errors(self, result, context={}):
        if result is not None:
            context['new_rows'] = result.totals['new']
            context['update_rows'] = result.totals['update']
            context['delete_rows'] = result.totals['delete']
            context['skip_rows'] = result.totals['skip']
            context['error_rows'] = result.totals['error']
            context['invalid_rows'] = result.totals['invalid']
        logger.debug('context %s', context)
        return context


class ImportView(
        FormView,
        ImportMixin
):

    resource_class = None
    filename = None
    template_name = None
    form_class = None

    def post(self, request, *args, **kwargs):

        # Imports file data to database
        import_type = request.POST.get('import_type')
        if import_type == 'create_only':
            skip_update = True
        else:
            skip_update = False
        logger.debug('skip_update %s', skip_update)
        result = self.import_file(skip_update=skip_update)
        self.context = self.adapt_context(result)
        self.context['form'] = self.form_class()
        return super().post(self, request, *args, **kwargs)

    def form_valid(self, form):
        return render(
            self.request,
            self.template_name,
            context=self.context,
        )
