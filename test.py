#!/usr/bin/env python
# vim:set et ts=4 sw=4:
# GPLv2; (C) 2011 Philipp Kern <pkern@debian.org>
# Simple test case to verify that fdsend is working correctly.
# (I.e. both message and fds are sent properly.)  This fails
# on Debian Lenny/amd64, presumably due to a kernel bug.

# Lenny has Python 2.5, so we need this.
from __future__ import with_statement

import fdsend
import os
import socket
import sys
import tempfile
import time

def try_connect(s, fn, n=0):
    try:
        s.connect(fn)
    except socket.error:
        if n > 3:
            raise
        time.sleep(1)
        try_connect(s, fn, n+1)

def child(fn):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try_connect(s, fn)
    req, fds = fdsend.recvfds(s, 1024, numfds=1)
    files = [os.fdopen(fd, 'r') for fd in fds]
    result = files[0].read()
    if req == "fds" and result == "TESTDATA\n":
        sys.exit(0)
    else:
        print "Test failed!"
        print "Message expected: fds"
        print "Message got: " + req
        print "FD content expected: TESTDATA"
        print "FD got: " + result.strip()
        sys.exit(1)

def parent(child_pid, fn):
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
    if exit_status != 0:
        # Test failed
        sys.exit(1)

def main():
    temp_dir = tempfile.mkdtemp()
    socket_filename = os.path.join(temp_dir, 'sock')

    pid = os.fork()
    if pid == 0:
        child(socket_filename)
    else:
        parent(pid, socket_filename)

if __name__ == '__main__':
    main()

