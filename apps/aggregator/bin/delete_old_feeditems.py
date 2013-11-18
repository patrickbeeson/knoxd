import os
import time
import optparse
import datetime

#from django.core.management import setup_environ
#import settings
#setup_environ(settings)

def delete_old_feeditems(verbose=False):
    from knoxd.apps.aggregator.models import FeedItem
    age_cutoff = datetime.datetime.now() - datetime.timedelta(days=30)
    feeditems_to_delete = FeedItem.objects.filter(date_modified__lt=age_cutoff)
    deleted_count = feeditems_to_delete.count()

    for FeedItem in feeditems_to_delete:
    	FeedItem.delete()
    print "Deleted %s feed items from database" % deleted_count

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('--settings')
    parser.add_option('-v', '--verbose', action="store_true")
    options, args = parser.parse_args()
    if options.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = options.settings
    delete_old_feeditems(options.verbose)
