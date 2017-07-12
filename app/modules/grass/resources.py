# encoding: utf-8
# pylint: disable=bad-continuation
"""
RESTful API GRASS GIS resources
-------------------------------
"""
import logging

from flask_login import current_user
from flask_restplus_patched import Resource
from flask_restplus_patched._http import HTTPStatus

from app.extensions import db
from app.extensions.api import Namespace, abort
from app.extensions.api.parameters import PaginationParameters

# from app.extensions.grass import get_commands, Module as GModule
# FIXME: remove this class definition once we are able to start a GRASS session
# and uncomment the import
class GModule():
    def __init__(self, module_name):
        pass

from app.modules.users import permissions
from app.modules.users.models import User

# from .models import parameter, flag, module


#def get_modules():
#    # read the configuration file with the published modules
#    # check all the modules are avaialable in the path
#    # return the list of the modules
#    return get_commands()


#CMDS, SCRS = get_modules()
CMDS = ['r.slope.aspect', 'r.sun']

PKEYS = ['name', 'description', 'guisection',
         'required', 'multiple', 'isrange', 'ischoice',
         'type', 'typedesc', 'keydesc', 'keydescvalues',
         'min', 'max', 'values',
         'default']

FKEYS = ['name', 'description', 'guisection', 'default']

log = logging.getLogger(__name__)              # pylint: disable=invalid-name
api = Namespace('modules', description="Teams")  # pylint: disable=invalid-name


def obj2dict(obj, attributes):
    """Convert a general object into a dictionary, providing the list of
    attributes to be used as keys"""
    return {attr: getattr(obj, attr) for attr in attributes}


def convert_parameter(gparm):
    """Convert a GRASS GIS Parameter instance into a rest parameter"""
    # add an extra attribute to distinguish when values are possible choices
    gparm.ischoice = (True if (getattr(gparm, 'isrange', False) is False and
                               getattr(gparm, 'values', None) is not None)
                      else False)
    return obj2dict(gparm, PKEYS)


def convert_flag(gflag):
    """Convert a GRASS GIS Flag instance into a rest flag"""
    return obj2dict(gflag, FKEYS)


@api.route('/')
@api.login_required(oauth_scopes=['grass:read'])
class Modules(Resource):
    """
    List of GRASS GIS Modules.
    """
    def get(self):
        """
        List of modules.

        """
        return CMDS


@api.route('/<str:module_name>')
@api.login_required(oauth_scopes=['grass:read'])
class Module(Resource):
    """
    List of GRASS GIS Modules.
    """
    def get(self, module_name):
        """
        Module information and parameters.

        """
        if module_name not in CMDS:
            return "GRASS GIS module not found or not enabled", 404
        try:
            mdl = GModule(module_name)
        except Exception as exc:
            return "Not able to load the module description",

        return dict(name=mdl.name, description=mdl.label,
                    keywords=[kw.strip() for kw in mdl.keywords.split(',')],
                    inputs=[convert_parameter(parm, PKEYS)
                            for parm in mdl.inputs],
                    outputs=[convert_parameter(parm, PKEYS)
                             for parm in mdl.outputs],
                    flags=[convert_flag(flg, FKEYS) for flg in mdl.flags]
                    )
