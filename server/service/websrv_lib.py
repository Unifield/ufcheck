# -*- coding: utf-8 -*-
#
# Copyright P. Christeas <p_christ@hol.gr> 2008-2010
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

""" Framework for generic http servers

"""

import socket
import base64
import errno
import SocketServer
from BaseHTTPServer import *
from SimpleHTTPServer import SimpleHTTPRequestHandler

class dummyconn:
    def shutdown(self, tru):
        pass

def _quote_html(html):
    return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

import threading
class ConnThreadingMixIn:
    """Mix-in class to handle each _connection_ in a new thread.

       This is necessary for persistent connections, where multiple
       requests should be handled synchronously at each connection, but
       multiple connections can run in parallel.
    """

    # Decides how threads will act upon termination of the
    # main process
    daemon_threads = False

    def _get_next_name(self):
        return None

    def _handle_request_noblock(self):
        """Start a new thread to process the request."""
        if not threading: # happens while quitting python
            return
        t = threading.Thread(name=self._get_next_name(), target=self._handle_request2)
        if self.daemon_threads:
            t.setDaemon (1)
        t.start()

    def _mark_start(self, thread):
        """ Mark the start of a request thread """
        pass

    def _mark_end(self, thread):
        """ Mark the end of a request thread """
        pass

    def _handle_request2(self):
        """Handle one request, without blocking.

        I assume that select.select has returned that the socket is
        readable before this function was called, so there should be
        no risk of blocking in get_request().
        """
        try:
            self._mark_start(threading.currentThread())
            request, client_address = self.get_request()
            if self.verify_request(request, client_address):
                try:
                    self.process_request(request, client_address)
                except Exception:
                    self.handle_error(request, client_address)
                    self.close_request(request)
        except socket.error:
            return
        finally:
            self._mark_end(threading.currentThread())

#eof
