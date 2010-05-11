from django.db import models
from cms.models import CMSPlugin

class PygmentsPlugin(CMSPlugin):
    code_language = models.CharField(max_length=20)
    code = models.TextField()