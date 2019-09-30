from django import template
from datetime import date, timedelta

register = template.Library()
@register.filter(name='get_at_index')
def get_at_index(list, index):
    return list[index]