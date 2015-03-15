__author__ = 'khorm'

from django import template

register = template.Library()


@register.filter
def get_name(list):
    thing = list[0]

    print list[0]
    return thing.name
