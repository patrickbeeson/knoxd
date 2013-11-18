from django.db import models
import datetime
from django.contrib.auth.models import User
from django.contrib import admin
from markdown import markdown

class Category(models.Model):
	slug = models.SlugField(help_text='Prepopulates from title field.')
	title = models.CharField(max_length=200)
	description = models.TextField(help_text='Use markdown formatting.')
	description_html = models.TextField(editable=False, blank=True)

	class Meta:
		db_table = 'blog_categories'
		verbose_name_plural = 'categories'

	def __unicode__(self):
		return self.title

	def save(self):
		self.description_html = markdown(self.description)
		super(Category, self).save()

	def get_absolute_url(self):
		return "/blog/category/%s/" % (self.slug)

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'description')
	prepopulated_fields = {'slug': ('title',)}

class Entry(models.Model):

	STATUS_CHOICES = (
		(1, 'Closed'),
		(2, 'Editing'),
		(3, 'Public'),
	)

	pub_date = models.DateTimeField()
	author = models.ForeignKey(User)
	slug = models.SlugField(unique_for_date='pub_date', help_text='Prepopulates from headline field.')
	headline = models.CharField(max_length=200)
	summary = models.TextField()
	summary_html = models.TextField(editable=False, blank=True)
	body = models.TextField()
	body_html = models.TextField(editable=False, blank=True)
	category = models.ForeignKey(Category)
	keywords = models.CharField(max_length=200, help_text='Use comma-separated values. Limit 200 characters.')
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
	enable_comments = models.BooleanField()
	
	class Meta:
		db_table = 'blog_entries'
		verbose_name_plural = 'entries'
		ordering = ('-pub_date',)
		get_latest_by = 'pub_date'

	def __unicode__(self):
		return self.headline
		
	def save(self):
		self.summary_html = markdown(self.summary)
		self.body_html = markdown(self.body)
		super(Entry, self).save()

	def get_absolute_url(self):
		return "/blog/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)

class EntryAdmin(admin.ModelAdmin):
	list_display = ('pub_date', 'headline', 'author', 'category', 'status', 'enable_comments')
	list_filter = ('status', 'category', 'author', 'enable_comments')
	search_fields = ('headline', 'summary', 'body', 'keywords')
	prepopulated_fields = {'slug': ('headline',)}	
	
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)