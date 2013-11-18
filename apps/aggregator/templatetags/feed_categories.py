from django import template
from django.core import template_loader
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
import re
from knoxd.apps.aggregator.models import Category
from django.template import Node


class FeedCategories(template.Node):
  def __init__(self, var_name):
    self.var_name = var_name
  
  def render(self, context):
    categories = Category.objects.all()
    context[self.var_name] = categories
    return ''

def do_get_feed_categories(parser, token):
  """
  Gets a list of all feed categories.
  
  Syntax::
    
    {% get_feed_categories as [var_name] %}
  
  Example usage::
  
    {% get_feed_categories as category_list %}
  """
  try:
    category_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s category requires arguments" % token.contents.split()[0]
  m = re.search(r'as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "%s category had invalid arguments" % category_name
  var_name = m.groups()[0]
  return FeedCategories(var_name)

register = template.Library()
register.tag('get_feed_categories', do_get_feed_categories)