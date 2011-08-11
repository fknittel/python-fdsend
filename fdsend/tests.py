#!/usr/bin/env python
# vim:set et ts=4 sw=4:
"""
Provides test cases for :mod:`fdsend`.
"""
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

import fdsend
import os
import socket
import tempfile
import unittest
import time
import shutil

def try_connect(sock, sock_fn, retries=30):
    """Try connecting with `sock` to `sock_fn`.  The connection is attempted
    `retries` times.
    """
    try_num = 1
    while True:
        try:
            sock.connect(sock_fn)
            return
        except socket.error:
            if try_num > retries:
                raise
            time.sleep(0.1)
            try_num += 1


class TestFDSend(unittest.TestCase):
    """Simple test case to verify that fdsend is working correctly. (I.e. both
    message and fds are sent properly.)  This fails on Debian Lenny/amd64,
    presumably due to a kernel bug.
    """
    # We cannot change the function names dictated by :class:`TestCase`.
    # pylint: disable=C0103

    longMessage = True
    DIRECT_DATA = "This data was sent directly via the socket."
    FILE_DATA = "This data was stored in a file whose file descriptor "\
            "was passed via the socket."

    def setUp(self):
        """Prepares a temporary directory and the name of the communication
        socket file.
        """
        self.temp_dir = tempfile.mkdtemp()
        self.sock_fn = os.path.join(self.temp_dir, 'sock')

    def tearDown(self):
        """Clears out the temporary directory.
        """
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_send_receive(self):
        """Test sending and receiving of direct data and file descriptors.

        It splits off a child process to test the fdsend module while
        conveniently using blocking calls.
        """
        pid = os.fork()
        if pid == 0:
            # The child creates the socket and sends data.
            try:
                self.send_data()
            except: # pylint: disable=W0702
                # Suppress all exception handling to avoid :class:`TestCase`
                # from kicking in.
                os._exit(1) # pylint: disable=W0212
            os._exit(0) # pylint: disable=W0212

        # The parent receives the data and verifies it.
        self.receive_data()

        # Wait for the child to exit.
        (pid, exit_status) = os.waitpid(pid, 0)
        self.assertTrue(exit_status == 0)

    def receive_data(self):
        """This method verifies that the data received through the UNIX domain
        socket is as expected.
        """
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        # As the other process might not have created the socket file yet, try
        # connecting repeatedly.
        try_connect(sock, self.sock_fn)

        data, fds = fdsend.recvfds(sock, 1024, numfds=64)

        # Now verify that what we received is what we expected.

        # Exactly one file descriptor.
        self.assertEqual(len(fds), 1)

        # Received correct direct data.
        self.assertEqual(data, self.DIRECT_DATA)

        # Verify file descriptor position.
        transferred_fp = os.fdopen(fds[0], 'r')
        self.assertEqual(transferred_fp.tell(), len(self.FILE_DATA))

        # Verify data in passed file descriptor.
        transferred_fp.seek(0)
        self.assertEqual(transferred_fp.read(), self.FILE_DATA)

    def send_data(self):
        """Creates a new UNIX socket named `sock_fn` and a temporary file and
        transmits some data and the file descriptor of the temporary file
        through that socket.
        """
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(self.sock_fn)
        sock.listen(1)
        client_sock, _ = sock.accept()

        tmp_fp = open(os.path.join(self.temp_dir, 'somefile'), 'w+')
        tmp_fp.write(self.FILE_DATA)
        tmp_fp.flush()
        fdsend.sendfds(client_sock, self.DIRECT_DATA, fds=[tmp_fp])
        # tmp_fp will be cleaned up by deleting the temporary directory.
