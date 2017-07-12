# coding: utf-8
"""
GRASS GIS provider setup
------------------------

"""

from flask import Blueprint, request, render_template
from flask_login import current_user
from flask_restplus_patched._http import HTTPStatus

from app.extensions import api, oauth2

# from .models import ...

