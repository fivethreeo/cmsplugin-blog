from django.utils.translation import ugettext_lazy as _

from pygments import highlight, styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import PygmentsPlugin
from django.utils.translation import ugettext as _

class CMSPygmentsPlugin(CMSPluginBase):
    model = PygmentsPlugin
    name = _("Pygments")
    render_template = "cmsplugin_blog/plugins/pygments.html"

    def render(self, context, instance, placeholder):
        style = styles.get_style_by_name('emacs')
        formatter = HtmlFormatter(linenos=True, style=style)
        html = highlight(instance.code,
			get_lexer_by_name(instance.code_language), formatter
		)
        css = formatter.get_style_defs()
        context.update({'pygments_html': html, 'css': css,
                                        'object':instance,
                                        'placeholder':placeholder})
        return context

plugin_pool.register_plugin(CMSPygmentsPlugin)

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
            from cms.utils import get_language_from_request
            language = get_language_from_request(context["request"])
            qs = qs.filter(entrytitle__language=language)
            
        latest = qs[:instance.limit]
        context.update({
            'instance': instance,
            'latest': latest,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(CMSLatestEntriesPlugin)
