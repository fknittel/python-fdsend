#Intro#

fdsend is yet another file descriptor passing abstraction, specifically for Python. This package offers a few conveniences not commonly found together in other abstractions: sending multiple files at once, sending arbitrary data, and working with both files and file descriptors.

#License#

fdsend is free software, licensed under the GPLv2+. It was originally developed by [Michael J. Pomraning](http://pilcrow.madison.wi.us/) and is currently maintained by Philipp Kern and Fabian Knittel. Small portions of fdsend are adapted from other sources, see the main source file for details.

#Requirements#

Python >= 2.2 is required, as is SCM_RIGHTS support on AF_UNIX sockets. Only Linux has been tested.

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

#Feedback#

Please report problems, bugs, feature requests, successes on the [mailing list](https://groups.google.com/group/python-fdsend).

#Related Interest#

[scgi](http://www.mems-exchange.org/software/scgi/) (python) contains a passfd module.
This [sendmsg](http://www.python.org/pycon/dc2004/papers/51/migration-code/sendmsg/) module (python) is a mostly complete sendmsg interface.
[Socket::MsgHdr](http://search.cpan.org/dist/Socket-MsgHdr/lib/Socket/MsgHdr.pm) (perl) offers a full sendmsg interface.
[bglibs](http://untroubled.org/bglibs/) provides a variety of UNIX-ish conveniences, including a socket_sendfd function.
The [I_SENDFD](http://pubs.opengroup.org/onlinepubs/007908799/xsh/ioctl.html) ioctl is an alternative approach for streams-based systems