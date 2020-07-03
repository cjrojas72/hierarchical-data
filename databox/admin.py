from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from databox.models import File_data

# Register your models here.
admin.site.register(File_data, DraggableMPTTAdmin)
