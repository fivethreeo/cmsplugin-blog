from cmsplugin_blog.models import Entry, EntryTitle
from simple_translation.translation_pool import translation_pool

translation_pool.register_translation(Entry, EntryTitle)

