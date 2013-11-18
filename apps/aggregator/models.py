from django.db import models
from django.contrib import admin

class Feed(models.Model):
    title = models.CharField(max_length=200, help_text='The name of the site providing the feed.')
    feed_url = models.URLField(max_length=200, unique=True, help_text='The feed URL.')
    public_url = models.URLField(max_length=200, help_text='The URL of the site providing the feed.')
    is_defunct = models.BooleanField()
    category = models.ForeignKey('Category')
    description = models.TextField(blank=True, help_text='A brief description of this feed, and the Web site that provides it. Use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.')
    keywords = models.CharField(max_length=200, blank=True, help_text='Comma-separated keywords describing this feed, and the Web site that provides it.')

    class Meta:
        db_table = 'aggregator_feeds'

    def __unicode__(self):
        return self.title

    def get_feeditems(self):
        """
        Returns the feeditem object for the feed.
        """
        return FeedItem.objects.filter(feed=self)[:5]

    def get_absolute_url(self):
    	return '/categories/%s/%s/' % (self.category.slug, self.id)

class FeedAdmin(admin.ModelAdmin):
	list_filter = ('category','is_defunct')

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    summary = models.TextField(blank=True)
    date_modified = models.DateTimeField()
    guid = models.CharField(max_length=200, unique=True, db_index=True)

    class Meta:
        db_table = 'aggregator_feeditems'
        ordering = ("-date_modified",)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.link

class FeedItemAdmin(admin.ModelAdmin):
	list_display = ('title', 'feed')
	list_filter = ('feed', 'date_modified')
	search_fields = ('title', 'summary', 'guid',)	

class Category(models.Model):
    slug = models.SlugField(help_text='This field will prepopulate from the title field.', unique=True)
    title = models.CharField(max_length=50)
    description = models.TextField(help_text='A brief summary of this category. Use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.')
    keywords = models.CharField(max_length=200, help_text='Comma-separated keywords describing the category. Limit 200 characters.', blank=True)
    
    class Admin:
        list_display = ('slug', 'title')
        
    class Meta:
        verbose_name_plural = 'categories'
        
    def __unicode__(self):
        return self.title

    def get_feeds(self):
        """
        Returns the feed object for the category.
        """
        return Feed.objects.filter(category=self).order_by('title')
        
    def get_feed_items(self):
        """
        Returns the feed items for feeds in a category.
        """
        return FeedItem.objects.filter(feed__category=self)[:5]
    
    def get_absolute_url(self):
        return '/categories/%s/' % (self.slug)

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('slug', 'title')
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(FeedItem, FeedItemAdmin)
admin.site.register(Feed, FeedAdmin)