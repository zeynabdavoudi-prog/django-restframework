from django.contrib import admin
from .models import *

admin.site.register(Category)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'status',  'created_date', 'published_date']
