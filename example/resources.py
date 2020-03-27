"""Defines how model instances can be imported or exported."""

import logging

from import_export import fields
from import_export.widgets import ForeignKeyWidget

from lib_import.resources import ImportModelResource
import example.models as m

logger = logging.getLogger(__name__)


class ExampleModelResource(ImportModelResource):

    base = fields.Field(
        column_name='base',
        attribute='base',
        widget=ForeignKeyWidget(
            m.BaseModel,
            'name',
        )
    )

    class Meta:
        """Main characteristics."""

        model = m.ExampleModel
        fields = (
            'date',
            'name',
            'base',
        )
        import_id_fields = ('name', )
