#Intro#

fdsend is yet another file descriptor passing abstraction, specifically for Python. This package offers a few conveniences not commonly found together in other abstractions: sending multiple files at once, sending arbitrary data, and working with both files and file descriptors.

#License#

fdsend is free software, licensed under the GPLv2+. It was originally developed by [Michael J. Pomraning](http://pilcrow.madison.wi.us/) and is currently maintained by Philipp Kern and Fabian Knittel. Small portions of fdsend are adapted from other sources, see the main source file for details.

#Requirements#

Python >= 2.2 is required, as is SCM_RIGHTS support on AF_UNIX sockets. Only Linux has been tested. Setuptools is required for automatic unit test runs at 
build-time.

#Installation#

  $ tar zxf fdsend-$VERSION.tar.gz
  $ cd fdsend-$VERSION
  $ python setup.py build
  $ python setup.py install

#Details#

fdsend allows the passing of open files between unrelated processes via local sockets (using SCM_RIGHTS), a process known as file descriptor passing.  The following functions are available:

  sendfds()
  recvfds()
  socketpair()

Unlike some other simplifications of the sendmsg()/recvmsg() interface, fdsend allows multiple files to be transferred in a single operation, and permits ordinary socket messages to accompany the files.  Additionally, fdsend understands bona fide Python sockets and files, as well as objects implementing fileno() methods and integers representing file descriptors.

Errors are raised via the socket.error exception object.

#Example#

    import fdsend
    import socket  # for socket.error    

    # -- sender; send 12 files
    #
    nulldevs = [ file('/dev/null') for i in xrange(12) ]
    fdsend.sendfds(sock, "here you go!", fds = nulldevs)

    # -- recipient; receive up to 128-byte message, and up to 32 files
    #
    (msg, fds) = fdsend.recvfds(sock, 128, numfds = 32)
    import os
    fds = [ os.fdopen(fileno) for fileno in fds ]

    # -- exception handling
    #
    import socket
    try:
	notasock = file("/dev/null")
        fdsend.sendfds(notasock, "This won't work!")
    except socket.error, e:
        import errno
        if e[0] == errno.ENOTSOCK:
            print "What did you expect? :)"

#Known Bugs#

- No provision is made to support msg_accrights systems (nor I_SENDFD fd passing).
- No support for Python 3 yet (coming soon, see the code repository).

#Feedback#

Please report problems, bugs, feature requests, successes on the [mailing list](https://groups.google.com/group/python-fdsend).

#Misc#

- The usual limitation in "rights" send/recv fd implementations, wherein
  msg_iov conveys a single, often hardcoded, byte, is a venerable approach
  dating back at least as far as Stevens' APUE examples (1992).  For many
  applications, it's no limitation at all.
- socketpair() is only for Python versions lacking this under the 'socket'
  module.

#Related Interest#

- [sendmsg()/recvmsg() patch](http://bugs.python.org/issue6560) (python) aims at adding the low-level methods. Based on this patch, fdsend could be turned into a pure Python module.
- [scgi](http://www.mems-exchange.org/software/scgi/) (python) contains a passfd module.
- This [sendmsg](http://www.python.org/pycon/dc2004/papers/51/migration-code/sendmsg/) module (python) is a mostly complete sendmsg interface.
- [Socket::MsgHdr](http://search.cpan.org/dist/Socket-MsgHdr/lib/Socket/MsgHdr.pm) (perl) offers a full sendmsg interface.
- [bglibs](http://untroubled.org/bglibs/) provides a variety of UNIX-ish conveniences, including a socket_sendfd function.
- The [I_SENDFD](http://pubs.opengroup.org/onlinepubs/007908799/xsh/ioctl.html) ioctl is an alternative approach for streams-based systems