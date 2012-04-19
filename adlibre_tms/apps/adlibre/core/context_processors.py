from django.conf import settings

from template_utils.context_processors import settings_processor

adlibre_settings = settings_processor(
    'SITE_NAME'
    )
