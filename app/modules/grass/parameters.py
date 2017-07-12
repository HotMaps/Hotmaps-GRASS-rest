# encoding: utf-8
# pylint: disable=wrong-import-order
"""
Input arguments (Parameters) for GRASS resources RESTful API
------------------------------------------------------------
"""
from flask_login import current_user
from flask_marshmallow import base_fields
from flask_restplus_patched import PostFormParameters
from marshmallow import validates, ValidationError

from app.extensions import api
from app.extensions.api.parameters import PaginationParameters


class ListMapsetParameters(PaginationParameters):
    user_id = base_fields.Integer(required=True)

    @validates('user_id')
    def validate_user_id(self, data):
        if current_user.id != data:
            raise ValidationError("It is only allowed to query your own Mapsets.")
