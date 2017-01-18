# -*- coding: utf-8 -*-
#
# Copyright P. Christeas <p_christ@hol.gr> 2008-2010
# Copyright 2010 OpenERP SA. (http://www.openerp.com)
#
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
###############################################################################

""" This file contains instance of the http server.


"""
from websrv_lib import *
import netsvc
import errno
import threading
import tools
import posixpath
import urllib
import os
import select
import socket
import xmlrpclib
import logging

import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
import gzip_xmlrpclib

try:
    import fcntl
except ImportError:
    fcntl = None

try:
    from ssl import SSLError
except ImportError:
    class SSLError(Exception): pass

class ThreadedHTTPServer(ConnThreadingMixIn, SimpleXMLRPCDispatcher, HTTPServer):
    """ A threaded httpd server, with all the necessary functionality for us.

        It also inherits the xml-rpc dispatcher, so that some xml-rpc functions
        will be available to the request handler
    """
    encoding = None
    allow_none = False
    allow_reuse_address = 1
    _send_traceback_header = False
    i = 0

    def __init__(self, addr, requestHandler, proto='http',
                 logRequests=True, allow_none=False, encoding=None, bind_and_activate=True):
        self.logRequests = logRequests

        SimpleXMLRPCDispatcher.__init__(self, allow_none, encoding)
        HTTPServer.__init__(self, addr, requestHandler)
        
        self.numThreads = 0
        self.proto = proto
        self.__threadno = 0

        # [Bug #1222790] If possible, set close-on-exec flag; if a
        # method spawns a subprocess, the subprocess shouldn't have
        # the listening socket open.
        if fcntl is not None and hasattr(fcntl, 'FD_CLOEXEC'):
            flags = fcntl.fcntl(self.fileno(), fcntl.F_GETFD)
            flags |= fcntl.FD_CLOEXEC
            fcntl.fcntl(self.fileno(), fcntl.F_SETFD, flags)

    def handle_error(self, request, client_address):
        """ Override the error handler
        """
        logging.getLogger("init").exception("Server error in request from %s:" % (client_address,))

    def _mark_start(self, thread):
        self.numThreads += 1

    def _mark_end(self, thread):
        self.numThreads -= 1


    def _get_next_name(self):
        self.__threadno += 1
        return 'http-client-%d' % self.__threadno

#eof
