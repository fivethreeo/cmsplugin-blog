from django import forms
from django.conf import settings
from django.utils import simplejson
from django.utils.safestring import mark_safe
from tagging.models import Tag
from cmsplugin_blog.models import Entry

class AutoCompleteTagInput(forms.TextInput):
    class Media:
        css = {
            'all': (
                settings.JQUERY_UI_CSS,
                '%scmsplugin_blog/cmsplugin_blog.css' % settings.STATIC_URL
            )
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
            
            var availableTags = %s
            
            function split( val ) {
                return val.split( /,\s*|^/ );
            }
            function extractLast( term ) {
                return split( term ).pop();
            }
            
            blog.jQuery("#id_%s")
                // don't navigate away from the field on tab when selecting an item
                .bind( "keydown", function( event ) {
                    if ( event.keyCode === blog.jQuery.ui.keyCode.TAB &&
                            $( this ).data( "autocomplete" ).menu.active ) {
                        event.preventDefault();
                    }
                })
                .autocomplete({
                    minLength: 0,
                    source: function( request, response ) {
                        // delegate back to autocomplete, but extract the last term
                        response( blog.jQuery.ui.autocomplete.filter(
                            availableTags, extractLast( request.term ) ) );
                    },
                    focus: function() {
                        // prevent value inserted on focus
                        return false;
                    },
                    select: function( event, ui ) {
                        var terms = split( this.value );
                        // remove the current input
                        terms.pop();
                        // add the selected item
                        terms.push( ui.item.value );
                        // add placeholder to get the comma-and-space at the end
                        terms.push( "" );
                        this.value = terms.join( ", " );
                        return false;
                    }
            });



            </script>''' % (tag_list, name))
