
import logging

from lib_import.views import ImportView

from example.resources import ExampleModelResource
from example.forms import ExampleForm

logger = logging.getLogger(__name__)


class ExampleImportView(ImportView):

    resource_class = ExampleModelResource
    template_name = 'form_view.html'
    form_class = ExampleForm
