from django import template
from cms.utils import get_language_from_request
from cmsplugin_blog.models import Entry, EntryTitle

register = template.Library()

def get_entry_title(entry, request):
    language = get_language_from_request(request)
    try:
        title = entry.entrytitle_set.filter(language=language)[0]
    except IndexError:
        title = entry.entrytitle_set.all()[0]
    return title
register.filter(get_entry_title)

import datetime
from django import template


@register.inclusion_tag('cmsplugin_blog/month_links_snippet.html', takes_context=True)
def render_month_links(context):
    request = context["request"]
    language = get_language_from_request(request)
    return {
        'dates': Entry.objects.filter(entrytitle__language=language).dates('pub_date', 'month'),
    }