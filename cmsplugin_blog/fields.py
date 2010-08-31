from django.db import models
from django.conf import settings

from cms.models import Placeholder

def _get_attached_field(self):
    from cms.models import CMSPlugin
    if not hasattr(self, '_attached_field_cache'):
        self._attached_field_cache = None
        for rel in self._meta.get_all_related_objects() + self._meta.get_all_related_many_to_many_objects():
            if isinstance(rel.model, CMSPlugin):
                continue
            field = getattr(self, rel.get_accessor_name())
            if field.count():
                self._attached_field_cache = rel.field
    return self._attached_field_cache
        
class M2MPlaceholderField(models.ManyToManyField):
    
    def __init__(self, *args, **kwargs):
        
        if 'actions' in kwargs:
            self.actions = kwargs.pop('actions')
            
        if 'placeholders' in kwargs:
            self.placeholders = kwargs.pop('placeholders')
            
        kwargs['editable'] = False
        super(M2MPlaceholderField, self).__init__(Placeholder, *args, **kwargs)
        
    def contribute_to_related_class(self, cls, related):
        setattr(cls, '_get_attached_field', _get_attached_field)
        super(M2MPlaceholderField, self).contribute_to_related_class(cls, related)

if "south" in settings.INSTALLED_APPS:
        
    from south.modelsinspector import add_introspection_rules
    
    rules = [
        (
            (M2MPlaceholderField, ),
            [],
            {
                "editable": ["editable", {"default": True}],
            },
        ),
    ]
    
    add_introspection_rules(rules, ["^cmsplugin_blog\.fields",])
    