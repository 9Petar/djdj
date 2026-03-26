from django.contrib import admin
from django.utils.html import format_html
from .models import Guest, Room

from django.templatetags.static import static

admin.site.site_header = format_html(
    '<img src="{}" height="40" style="vertical-align:middle;"> Staff Admin',
    static('logo/file2.png')
)

admin.site.site_title = "Hotel Staff Admin Portal"
admin.site.index_title = "Welcome to the Hotel Staff Administration"


# Register your models here.
admin.site.register(Guest)
admin.site.register(Room)
