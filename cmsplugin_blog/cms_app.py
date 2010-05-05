from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class BlogApphook(CMSApp):
    name = _("Blog Apphook")
    urls = ["cmsplugin_blog.urls"]

apphook_pool.register(BlogApphook)