# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import base64
import os
import thread
import threading
import time
import sys
import platform
from tools.translate import _
import netsvc
import release
import tools
import locale
import logging
from cStringIO import StringIO
from tempfile import NamedTemporaryFile
import datetime


class _ObjectService(netsvc.ExportService):
     "A common base class for those who have fn(db, uid, password,...) "
     pass

class common(_ObjectService):
    def __init__(self,name="common"):
        _ObjectService.__init__(self,name)
        self.joinGroup("web-services")

    def exp_get_zip_file(self):
        # On va retourner le dispatch de la requête en question
        f = open("mypatch")
        data = f.read()
        f.close()
        return data

    def dispatch(self, method, auth, params):
        logger = netsvc.Logger()
        if method in ['get_zip_file']:
            pass
        else:
            raise Exception("Method not found: %s" % method)

        fn = getattr(self, 'exp_'+method)
        return fn(*params)


    def new_dispatch(self,method,auth,params):
        pass

common()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
