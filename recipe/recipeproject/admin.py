from django.contrib import admin
from .models import recipes,users
# Register your models here.

admin.site.register(recipes)
admin.site.register(users)