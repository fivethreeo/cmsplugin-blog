from django.utils.translation import ugettext_lazy as _

from tagging.models import TaggedItem
from tagging.utils import get_tag_list

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.utils import get_language_from_request

from simple_translation.utils import get_translation_filter_language

from cmsplugin_blog.models import LatestEntriesPlugin, Entry

class CMSLatestEntriesPlugin(CMSPluginBase):
    """
        Plugin class for the latest entries
    """
    model = LatestEntriesPlugin
    name = _('Latest entries')
    render_template = "cmsplugin_blog/latest_entries.html"
    
    def render(self, context, instance, placeholder):
        """
            Render the latest entries
        """
        qs = Entry.published.all()
        
        if instance.current_language_only:
            language = get_language_from_request(context["request"])
            kw = get_translation_filter_language(Entry, language)
            qs = qs.filter(**kw)
            
        if instance.tagged:
            tags = get_tag_list(instance.tagged)
            qs  = TaggedItem.objects.get_by_model(qs , tags)
            
        latest = qs[:instance.limit]
        
        context.update({
            'instance': instance,
            'latest': latest,
            'object_list': latest,
            'placeholder': placeholder
        })
        return context

plugin_pool.register_plugin(CMSLatestEntriesPlugin)
