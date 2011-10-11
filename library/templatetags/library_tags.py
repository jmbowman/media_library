from django import template
from django.conf import settings

from library.models import Media

register = template.Library()

@register.inclusion_tag('library/recently_added.html', takes_context=True)
def recently_added(context):
    items = None
    if context['user'].is_authenticated():
        items = Media.objects.order_by('-date_created')[:20]
    return {'items': items}

@register.simple_tag
def main_title():
    return settings.MAIN_TITLE

@register.simple_tag
def sub_title():
    return settings.SUB_TITLE