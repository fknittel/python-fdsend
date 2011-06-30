import _fdsend

# Wrap the C module.
sendfds = _fdsend.sendfds
recvfds = _fdsend.recvfds
socketpair = _fdsend.socketpair

