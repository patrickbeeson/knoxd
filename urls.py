from django.conf.urls.defaults import *
from knoxd.apps.aggregator.models import FeedItem, Category, Feed
from knoxd.apps.aggregator.feeds import RiverFeed
from knoxd.sitemaps import AggregatorSitemap
from django.contrib.sitemaps import FlatPageSitemap
from knoxd.robots import robots_txt
from knoxd.apps.blog.feeds import BlogEntryFeed
from django.contrib import admin

admin.autodiscover()

sitemaps = {
	'aggregator': AggregatorSitemap,
    'flatpages': FlatPageSitemap,
}

aggregator_info_dict = {
	'queryset': FeedItem.objects.select_related(),
	'paginate_by': 15,
}

feed_info_dict = {
	'queryset': Feed.objects.filter(is_defunct=False),
	'allow_empty': True,
}

feed_detail_info = {
	'queryset': Feed.objects.all(),
	'template_object_name': 'feed',
}

feeditem_detail_info = {
	'queryset': FeedItem.objects.all(),
	'template_object_name': 'feeditem',
}

category_list_info = {
	'queryset': Category.objects.all(),
	'allow_empty': True,
}

category_detail_info = {
	'queryset': Category.objects.all(),
	'template_object_name': 'category',
}

feeds = {
	'river': RiverFeed,
	'blog': BlogEntryFeed,
}

urlpatterns = patterns('',
	# Robots
	(r'^robots.txt$', robots_txt),
	# Homepage
	(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),
	# Admin
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	('^admin/(.*)', admin.site.root),
	# Categories
	(r'^categories/$', 'django.views.generic.list_detail.object_list', category_list_info),
	(r'^categories/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', category_detail_info),
	#Feed
	(r'^categories/([-\w]+)/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', feed_detail_info),
	# Contact form
	(r'^contact/', include('contact_form.urls')),
	# Feeds
	(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
	# Feed Items
	(r'^headline/(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', feeditem_detail_info),
	# River
	(r'^river/$', 'django.views.generic.list_detail.object_list', aggregator_info_dict),
	# Sitemaps
	(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	(r'^sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	# Blog
	(r'^blog/', include('knoxd.apps.blog.urls')),
	# Comments
	(r'^comments/', include('django.contrib.comments.urls')),
	# Flat pages
	(r'', include('django.contrib.flatpages.urls')),
)
