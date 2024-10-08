from django import template
import math

register = template.Library()


@register.filter
def time_format(value):
    """Convert seconds into minutes:seconds.milliseconds"""
    minutes = math.floor(value / 60)
    seconds = value % 60
    return f"{minutes}:{seconds:06.3f}"  # Minutes:seconds.milliseconds
