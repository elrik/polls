# -*- coding: utf-8 -*-
from django.conf import settings


def development_settings(request):
    """
    This function inserts development settings into the context.

    At the moment it adds:
        * less_compile_clientside - defined in the settings
                                    LESS_COMPILE_CLIENTSIDE
    """

    return {
        'less_compile_clientside': getattr(
            settings,
            'LESS_COMPILE_CLIENTSIDE',
            False
        ),
    }
