from django.db import models

# Create your models here.
class currency(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True, blank=True, default=None)
	pnl = models.FloatField(null=True, blank=True, default=None)
	pnlper = models.FloatField(null=True, blank=True, default=None)

	def __str__(self):
		return self.name

class indexes(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.CharField(max_length=200, null=True)
	pnl = models.FloatField(null=True, blank=True, default=None)
	pnlper = models.FloatField(null=True, blank=True, default=None)

	def __str__(self):
		return self.name

class equities(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.CharField(max_length=200, null=True)
	pnl = models.FloatField(null=True, blank=True, default=None)
	pnlper = models.FloatField(null=True, blank=True, default=None)

	def __str__(self):
		return self.name

class eqnews(models.Model):
	headline = models.CharField(max_length=200, null=True)
	imgurl = models.CharField(max_length=200, null=True)
	def __str__(self):
		return self.name

class fxnews(models.Model):
	headline = models.CharField(max_length=200, null=True)
	imgurl = models.CharField(max_length=200, null=True)
	def __str__(self):
		return self.name

class stocknews(models.Model):
	headline = models.CharField(max_length=400, null=True)
	content = models.CharField(max_length=400, null=True)
	imgurl = models.CharField(max_length=400, null=True)
	def __str__(self):
		return self.headline
