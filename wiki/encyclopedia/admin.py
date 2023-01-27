from django.contrib import admin

from .models import User, Author
# Register your models here.

admin.site.register(User)
admin.site.register(Author)
