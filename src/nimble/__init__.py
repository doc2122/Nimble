# __init__.py
# (C)2012-2013 http://www.ThreeAddOne.com
# Scott Ernst

import atexit

from nimble.NimbleEnvironment import NimbleEnvironment
from nimble.connection.NimbleConnection import NimbleConnection
from nimble.connection.NimbleConnectionWrapper import NimbleConnectionWrapper
from nimble.connection.batch.NimbleBatchCommandConnection import NimbleBatchCommandConnection
from nimble.connection.script.RemoteScriptResponse import RemoteScriptResponse
from nimble.connection.support.ImportedCommand import ImportedCommand
from nimble.connection.thread.NimbleServerThread import NimbleServerThread
from nimble.error.MayaCommandException import MayaCommandException

#===================================================================================================
#                                                                               F U N C T I O N S

#___________________________________________________________________________________________________ startServer
def startServer(logLevel =0, router =None, inMaya =None):
    """ Starts the NimbleServer properly given the current environmental conditions. The server runs
        in a separate thread and remains active until the stopServer() method.

        @@@param logLevel:int
            The integer logLevel to use when starting the server. The allowed values are:
            [#list]
                [#item]0 (default): Only log critical actions.[/#item]
                [#item]1: Additionally log warnings as well as succinct activity.[/#item]
                [#item]2: Full verbose logging of all activity.[/#item]
            [/#list]

        @@@param router:NimbleRouter
            The router to use for the server. The default value of None will use the default
            router for the given environment. The router is responsible for handling the
            communication traffic received by the server and correctly responding as a result.

        @@@param inMaya:boolean
            Whether or not the server is being run in Maya. By default this is determined
            automatically by the Nimble environment settings. However, in some cases the
            determination can be incorrect if your external or Maya Python interpreters have been
            modified to fool the environment test. In such cases this may need to be explicitly
            set.
    """

    NimbleEnvironment.inMaya(override=inMaya)
    NimbleEnvironment.setServerLogLevel(logLevel)
    NimbleServerThread(router=router).start()

#___________________________________________________________________________________________________ changeServerLogLevel
def changeServerLogLevel(logLevel =0):
    """ Changes the active servers logging level, or, if no server is active, changes the
        environment so that when a server is started it will run at the specified level. This is
        useful if, for example, you want to dynamically change the log level at a given point
        to debug.

        @@@param logLevel:int
            The integer logLevel to use when starting the server. The allowed values are:
            [#list]
                [#item]0 (default): Only log critical actions.[/#item]
                [#item]1: Additionally log warnings as well as succinct activity.[/#item]
                [#item]2: Full verbose logging of all activity.[/#item]
            [/#list]
    """

    return NimbleEnvironment.setServerLogLevel(logLevel)

#___________________________________________________________________________________________________ stopServer
def stopServer():
    """ Stops the currently running server if one is active. If no server is active this method
        will fail silently, no exception will be thrown, making it safe to call at any time.
    """

    return NimbleServerThread.closeServer()

#___________________________________________________________________________________________________ echoServerStatus
def echoServerStatus():
    """ Prints the status of the server, either inactive or active as well as returning the server
        activity integer. Note that servers are started up asynchronously, so there is a short
        period of time after the startServer() call where the server is loading but not yet ready
        for communication. These states are captured by both the printed output and the return value

        @@@returns int
            An integer representing the state of the server. Values will be:
            [#list]
                [#item]0: Server is inactive.[/#item]
                [#item]1: Server is loading.[/#item]
                [#item]2: Server is active and ready for communication.[/#item]
            [/#list]
    """

    if NimbleServerThread.isActivating():
        print 'Nimble server is loading'
        return 1

    if NimbleServerThread.isRunning():
        print 'Nimble server is running.'
        return 2

    print 'Nimble server is inactive.'
    return 0

#___________________________________________________________________________________________________ getConnection
def getConnection(inMaya =None, forceCreate =False):
    """ Retrieves a communication connection object from the connection pool, which is used for
        sending commands to the remote nimble server.

        @@@param inMaya:boolean
            Whether or not the server is being run in Maya. By default this is determined
            automatically by the Nimble environment settings. However, in some cases the
            determination can be incorrect if your external or Maya Python interpreters have been
            modified to fool the environment test. In such cases this may need to be explicitly
            set.

        @@@param forceCreate:boolean
            If True a new connection will be created even if one already exists and is available.
            This should rarely be used but can be useful in multi-threaded situations where sharing
            a single connection could be harmful.

        @@@returns NimbleConnection
            A NimbleConnection instance opened and ready for issuing commands to the remote server.
    """

    NimbleEnvironment.inMaya(override=inMaya)
    return NimbleConnection.getConnection(forceCreate=forceCreate)

#___________________________________________________________________________________________________ createBatch
def createCommandsBatch():
    return NimbleBatchCommandConnection()

#___________________________________________________________________________________________________ getRemoteKwargs
def getRemoteKwargs(scriptGlobalVars):
    """ This method is used to gain access to the kwargs dictionary sent with python script
        execution request. Under any other circumstances it just returns an empty dictionary.
    """

    out = scriptGlobalVars.get(NimbleEnvironment.REMOTE_KWARGS_KEY, None)
    if out is None:
        return dict()
    return out

#___________________________________________________________________________________________________ createRemoteResponse
def createRemoteResponse(scriptGlobalVars):
    return RemoteScriptResponse(scriptGlobalVars)

#___________________________________________________________________________________________________ getIsRunningInMaya
def getIsRunningInMaya():
    return NimbleEnvironment.inMaya()

#===================================================================================================
#                                                                                     M O D U L E

#___________________________________________________________________________________________________ CommandImport
# Convenience access to the ImportedCommand class.
CommandImport = ImportedCommand

#___________________________________________________________________________________________________ log
# Convenience access to the nimble environment logger.
log = NimbleEnvironment.log

#___________________________________________________________________________________________________ cmds
# Convenience access of the environmental Maya commands
cmds = NimbleConnectionWrapper()

#___________________________________________________________________________________________________ EVENT HANDLER: closeConnectionPool
# Cleans up the active socket connection pool on close to prevent communication errors in the
# NimbleServer routers.
def _handleExit():
    NimbleConnection.closeConnectionPool()
    stopServer()

atexit.register(_handleExit)
