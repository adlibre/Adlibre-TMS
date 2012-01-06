from django import template
register = template.Library()

@register.filter
def in_decimalhours(value):
    """ Returns decimal time in hours.
    e.g. 120 min = 2"""
    try:
        temp = int(value)
    except:
        raise ValueError('Error in "in_decimalhours" filter. Variable must be in convertable to int format.')
    output = value / 60
    return output
in_decimalhours.is_safe = True

