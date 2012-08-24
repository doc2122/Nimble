# MayaCommandException.py
# Vizme, Inc. (C)2012
# Scott Ernst

#___________________________________________________________________________________________________ MayaCommandException
class MayaCommandException(Exception):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """Creates a new instance of MayaCommandException."""
        self._responseData = kwargs.get('response') if 'response' in kwargs else None
        Exception.__init__(self, *args)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: response
    @property
    def response(self):
        return None
    @response.setter
    def response(self, value):
        pass