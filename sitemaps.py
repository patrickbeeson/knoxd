from django.contrib.sitemaps import Sitemap
from knoxd.apps.aggregator.models import Feed
import datetime

class AggregatorSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.5

    def items(self):
        return Feed.objects.all()

	def lastmod(self, obj):
		return obj.date_modified

	def location(self, obj):
		return "/categories/%s/%s" % obj.category.slug, obj.id 