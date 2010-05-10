from django import template
from cms.utils import get_language_from_request
from cmsplugin_blog.models import Entry, EntryTitle

register = template.Library()

@register.inclusion_tag('cmsplugin_blog/month_links_snippet.html', takes_context=True)
def render_month_links(context):
    request = context["request"]
    language = get_language_from_request(request)
    return {
        'dates': Entry.objects.filter(entrytitle__language=language).dates('pub_date', 'month'),
    }