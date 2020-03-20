"""Defines how model instances can be imported or exported."""

import logging

from import_export import resources


logger = logging.getLogger(__name__)


class ImportModelResource(resources.ModelResource):
    """Describes how who instances can be imported or exported."""

    def skip_row(self, instance, original):
        if self.skip_update:
            skip = True
            import_id_fields = [
                self.fields[f] for f in self.get_import_id_fields()
            ]
            for field in import_id_fields:
                if field.get_value(instance) != field.get_value(original):
                    skip = False
        else:
            skip = super().skip_row(instance, original)
        logger.debug('END skip_row')
        return skip

    def __init__(self, skip_update=False):
        self.skip_update = skip_update
        super().__init__()
