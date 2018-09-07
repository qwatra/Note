from django.contrib import admin
from mynoteapp.models import Note, Category

# Register your models here.
admin.site.register(Note)
admin.site.register(Category)