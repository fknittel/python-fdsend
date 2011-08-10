import _fdsend
import fdsend.tests

tests = fdsend.tests

# Wrap the C module.
sendfds = _fdsend.sendfds
recvfds = _fdsend.recvfds
socketpair = _fdsend.socketpair
