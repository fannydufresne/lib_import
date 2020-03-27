from django.contrib import admin

import example.models as m

admin.site.register(m.BaseModel)
admin.site.register(m.ExampleModel)
