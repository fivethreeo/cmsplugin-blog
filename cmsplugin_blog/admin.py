from django import forms
from django.contrib import admin
from simple_translation.admin import TranslationAdmin
from cmsplugin_blog.models import Entry, EntryTitle
from cmsplugin_blog.widgets import AutoCompleteTagInput

class EntryForm(forms.ModelForm):
    
    class Meta:
        model = Entry
        widgets = {'tags': AutoCompleteTagInput}
        
    title = forms.CharField()
    slug = forms.SlugField()

class EntryAdmin(TranslationAdmin):
    
    form = EntryForm
    
    prepopulated_fields = {}
        
    list_display = ('description', 'languages', 'is_published')
    list_editable = ('is_published',)
    
    def __init__(self, *args, **kwargs):
        super(EntryAdmin, self).__init__(*args, **kwargs)
        self.prepopulated_fields.update({'slug': ('title',)})
        
admin.site.register(Entry, EntryAdmin)

