# NimbleServer.py
# (C)2012 http://www.ThreeAddOne.com
# Scott Ernst

import asyncore
import socket

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.router.NimbleRouter import NimbleRouter
#AS NEEDED: from nimble.connection.router.MayaRouter import MayaRouter

#___________________________________________________________________________________________________ NimbleServer
class NimbleServer(asyncore.dispatcher):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, router =None):
        asyncore.dispatcher.__init__(self)

        try:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.set_reuse_addr()
            self.bind(('localhost', NimbleEnvironment.getServerPort()))
            self.listen(5)
        except Exception, err:
            print 'FAILED: Nimble server connection'
            print err
            raise

        if router is None:
            if NimbleEnvironment.inMaya():
                from nimble.connection.router.MayaRouter import MayaRouter
                self._router = MayaRouter
            else:
                self._router = NimbleRouter
        else:
            self._router = router

#___________________________________________________________________________________________________ handle_accept
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, address = pair
            handler = self._router(sock)
