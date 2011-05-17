from django import forms
from django.conf import settings
from django.utils import simplejson
from django.utils.safestring import mark_safe
from tagging.models import Tag
from cmsplugin_blog.models import Entry

class AutoCompleteTagInput(forms.TextInput):
    class Media:
        css = {
            'all': (settings.JQUERY_UI_CSS,)
        }
        js = (
            settings.JQUERY_JS,
            settings.JQUERY_UI_JS,
            '%scmsplugin_blog/jquery_init.js' % settings.STATIC_URL
        )

    def render(self, name, value, attrs=None):
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)
        page_tags = Tag.objects.usage_for_model(Entry)
        tag_list = simplejson.dumps([tag.name for tag in page_tags],
                                    ensure_ascii=False)
        return output + mark_safe(u'''<script type="text/javascript">
            blog.jQuery("#id_%s").autocomplete({
                width: 150,
                max: 10,
                highlight: false,
                multiple: true,
                multipleSeparator: ", ",
                scroll: true,
                scrollHeight: 300,
                matchContains: true,
                autoFill: true,
                source: %s
            });
            </script>''' % (name, tag_list))
