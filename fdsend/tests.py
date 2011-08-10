#!/usr/bin/env python
# vim:set et ts=4 sw=4:
#
# Copyright (C) 2011 Philipp Kern <pkern@debian.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Lenny has Python 2.5, so we need this.
from __future__ import with_statement

import fdsend
import os
import socket
import sys
import tempfile
import unittest
import time

class TestFDSend(unittest.TestCase):
    """Simple test case to verify that fdsend is working correctly. (I.e. both
    message and fds are sent properly.)  This fails on Debian Lenny/amd64,
    presumably due to a kernel bug.
    """
    @staticmethod
    def try_connect(s, fn, n=0):
        try:
            s.connect(fn)
        except socket.error:
            if n > 3:
                raise
            time.sleep(1)
            try_connect(s, fn, n+1)

    def child(self, fn):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.try_connect(s, fn)
        req, fds = fdsend.recvfds(s, 1024, numfds=1)
        files = [os.fdopen(fd, 'r') for fd in fds]
        result = files[0].read()
        if req == "fds" and result == "TESTDATA\n":
            os._exit(0)
        else:
            print "Test failed!"
            print "Message expected: fds"
            print "Message got: " + req
            print "FD content expected: TESTDATA"
            print "FD got: " + result.strip()
            os._exit(1)

    def parent(self, child_pid, fn):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.bind(fn)
        s.listen(1)
        (conn, address) = s.accept()

        with tempfile.TemporaryFile(mode='w+') as f:
            f.write("TESTDATA\n")
            f.flush()
            f.seek(0)
            fdsend.sendfds(conn, "fds", fds=[f])

        (pid, exit_status) = os.waitpid(child_pid, 0)
        self.assertTrue(exit_status == 0)

    def test_main(self):
        temp_dir = tempfile.mkdtemp()
        socket_filename = os.path.join(temp_dir, 'sock')

        pid = os.fork()
        if pid == 0:
            self.child(socket_filename)
        else:
            self.parent(pid, socket_filename)
