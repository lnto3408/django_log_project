from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Document(models.Model):
	docfile = models.FileField(upload_to='documents/%y/%m')
	description = models.CharField(max_length=255, blank=True)
	document = models.FileField(upload_to='documents/')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	


	def __unicode__(self):
		return self.docfile