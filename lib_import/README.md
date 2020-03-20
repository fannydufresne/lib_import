# Lib for making easy imports

This library is based on django-import-export lib.

## Features
The user can select through a form which type of import he would like to perform.

Two types of import are currently possible:
- Import "Create only": All rows wich correspond to new items i.e. one of import_id_fields value is different from existing ones are added. THe other ones are ignored.
- Import "Create and update": All new rows are created and already existing are updated if needed.

## Usage
For a complete example, see folder app.

Add `lib_import` to your `INSTALLED_APPS` setting.

View must be a children of `lib_import.views.ImportView`

It must specify:
- `resource_class`: Class of the resource to call. This resource must be a children of `lib_import.resources.ImportModelResource`
- `template_name`: The name of the template used to render the form (and messages returned after import)
- `form_class`: Class of the form to use in the template. It must inherit from `lib_import.forms.ImportForm`

It can also specify:
- `filename`: name of the imported file (which corresponds to the name of the filefield in the form).
If it is not specified, the first element of the files stored in the request will be taken.
If it is not given and more than one file is stored in the request, a warning is raised as it could take the wrong file.

Example:
```py
# views.py

from lib_import.views import ImportView

class ExampleImportView(ImportView):

    resource_class = ExampleModelResource
    template_name = 'form_view.html'
    form_class = ExampleForm
```

## Rendering
After import, the number hove rows which have been created, modified, skipped... is returned in the context. You can use this to display relevant error messages.

Content of the context:
- new_rows
- updated_rows
- delete_rows
- skip_rows
- error_rows
- invalid_rows