from django.contrib.syndication.feeds import Feed
from knoxd.apps.blog.models import Entry
import datetime

class BlogEntryFeed(Feed):
    title = "The Knox'd blog"
    link = "http://knoxd.com/blog/"
    description = "The latest information about new features and changes for Knox'd."

    def items(self):
        return Entry.objects.filter(status=3, pub_date__lte=datetime.datetime.now())[:10]
