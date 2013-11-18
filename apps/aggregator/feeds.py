from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.syndication.feeds import Feed
from knoxd.apps.aggregator.models import FeedItem

class RiverFeed(Feed):
    title = "Knox'd river | knoxd.com"
    link = "http://knoxd.com/river/"
    description = "The latest headlines aggregated on Knox'd."

    def items(self):
        return FeedItem.objects.order_by('-date_modified')[:10]
        