from django.utils.translation import ugettext_lazy as _, get_language

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.utils import get_language_from_request

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
            try:
                language = get_language_from_request(context["request"])
            except KeyError:
                language = get_current_language()
            qs = qs.filter(entrytitle__language=language)
            
        latest = qs[:instance.limit]
        context.update({
            'instance': instance,
            'latest': latest,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(CMSLatestEntriesPlugin)
