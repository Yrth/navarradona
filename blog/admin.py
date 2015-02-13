from django.contrib import admin
from blog.models import *
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField
from adminfiles.admin import FilePickerAdmin

# Register your models here.
class EntryAdmin(FilePickerAdmin):
    adminfiles_fields = ('content_markdown',)
    list_display = ("title","created_date")
    prepopulated_fields = {"slug":("title",)}
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}
    
admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Carousel)