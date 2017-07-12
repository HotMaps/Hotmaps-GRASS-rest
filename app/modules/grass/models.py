#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define model for GRASS GIS
--------------------------
"""
from app.extensions.api import api_v1
from flask_restplus import fields


parameter = api_v1.model('Parameter', {
    # general info
    'name': fields.String,
    'description': fields.String,
    'guisection': fields.String,
    # boolean fields
    'is_required': fields.Boolean(default=False, attribute='required'),
    'is_multiple': fields.Boolean(default=False, attribute='multiple'),
    'is_within_a_range': fields.Boolean(default=False, attribute='isrange'),
    'is_a_choice': fields.Boolean(default=False, attribute='ischoice'),
    # define the parameter type
    'type': fields.String,
    'typedesc': fields.String,
    'keydesc': fields.String,
    'keydescvalues': fields.String,
    # define the range limits
    'min': fields.String,
    'max': fields.String,
    # define the list of possible choices
    'choices': fields.List(fields.String, attribute='values'),
    # define the default value
    'default': fields.String,
})


flag = api_v1.model('Flag', {
    # general info
    'name': fields.String,
    'description': fields.String,
    'guisection': fields.String,
    # define the default value
    'default': fields.Boolean,
})


module = api_v1.model('Module', {
    'name': fields.String,
    'description': fields.String,
    'keywords': fields.List(fields.String),
    'man': fields.String,
    'inputs': fields.List(parameter),
    'outputs': fields.List(parameter),
    'flags': fields.List(flag),
})
