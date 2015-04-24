from django import template

register = template.Library()


@register.filter
def beautify_details(value):
    """Converts SalesDetails item into human readable format"""
    result = ''
    for name, item in value.iteritems():
        result += "'%s': %s, " % (name, item)
    return result