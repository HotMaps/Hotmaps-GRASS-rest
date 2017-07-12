# encoding: utf-8
"""
GRASS GIS module
================
"""

from app.extensions.api import api_v1


def init_app(app, **kwargs):
    # pylint: disable=unused-argument,unused-variable
    """
    Init GRASS GIS module.
    """
    api_v1.add_oauth_scope('grass:read',
                           "Provide access to GRASS GIS details")
    api_v1.add_oauth_scope('grass:write',
                           "Provide write access to GRASS GIS details")
    api_v1.add_oauth_scope('grass:execute',
                           "Provide write access to GRASS GIS details")

    # Touch underlying modules
    from . import models, resources

    api_v1.add_namespace(resources.api)
