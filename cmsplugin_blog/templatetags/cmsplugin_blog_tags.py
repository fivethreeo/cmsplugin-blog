import datetime
from django import template

from tagging.models import Tag

from cms.utils import get_language_from_request
from cmsplugin_blog.models import Entry, EntryTitle
from cms.models import Placeholder

register = template.Library()

@register.inclusion_tag('cmsplugin_blog/month_links_snippet.html', takes_context=True)
def render_month_links(context):
    request = context["request"]
    language = get_language_from_request(request)
    return {
        'dates': Entry.published.filter(entrytitle__language=language).dates('pub_date', 'month'),
    }

@register.inclusion_tag('cmsplugin_blog/tag_links_snippet.html', takes_context=True)
def render_tag_links(context):
    request = context["request"]
    language = get_language_from_request(request)
    filters = dict(is_published=True, pub_date__lte=datetime.datetime.now(), entrytitle__language=language)
    return {
        'tags': Tag.objects.usage_for_model(Entry, filters=filters)
    }
    
@register.filter
def choose_placeholder(placeholders, placeholder):
    try:
        return placeholders.get(slot=placeholder)
    except Placeholder.DoesNotExist:
        return None
    
