from django import template

register = template.Library()


@register.filter
def index(some_list, i):
    return some_list[int(i)]
