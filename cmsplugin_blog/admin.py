from django.contrib import admin
from simple_translation.admin import TranslationAdmin
from cmsplugin_blog.models import Entry, EntryTitle

class EntryAdmin(TranslationAdmin):
        
    list_display = ('description', 'languages', 'is_published')
    list_editable = ('is_published',)

admin.site.register(Entry, EntryAdmin)

