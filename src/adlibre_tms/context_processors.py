from django.conf import settings


def demo(context):
    """ Returns Demo Mode Boolean Context Variable """
    return {'DEMO': settings.DEMO}

def product_version(context):
    """ Returns Context Variable Containing Product version """
    return {'PRODUCT_VERSION': settings.PRODUCT_VERSION}