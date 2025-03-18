from django import template

register = template.Library()

@register.filter
def dict_key(dictionary, key):
    """Fetch dictionary value by key in Django template"""
    return dictionary.get(key, "")
