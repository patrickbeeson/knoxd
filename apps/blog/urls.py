from django.conf.urls.defaults import *
from models import Entry, Category

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}

archive_info_dict = {
    'queryset': Entry.objects.all(),
    'paginate_by': 15,
}

category_detail_info = {
	'queryset': Category.objects.all(),
}

urlpatterns = patterns('',
   (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', 'django.views.generic.date_based.object_detail', dict(info_dict, slug_field='slug')),
   #(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'django.views.generic.date_based.archive_day', info_dict),
   #(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'django.views.generic.date_based.archive_month', info_dict),
   #(r'^(?P<year>\d{4})/$', 'django.views.generic.date_based.archive_year', info_dict),
   (r'^/?$', 'django.views.generic.date_based.archive_index', info_dict),
   (r'^category/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', category_detail_info),
   (r'^archives/$', 'django.views.generic.list_detail.object_list', archive_info_dict),
)
