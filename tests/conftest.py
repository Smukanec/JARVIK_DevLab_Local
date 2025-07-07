import sys
import types

if 'requests' not in sys.modules:
    class HTTPError(Exception):
        def __init__(self, response=None):
            self.response = response
    class RequestException(Exception):
        pass
    def post(*args, **kwargs):
        class Resp:
            def raise_for_status(self):
                pass
            def json(self):
                return {}
        return Resp()
    dummy = types.SimpleNamespace(post=post, HTTPError=HTTPError, RequestException=RequestException)
    sys.modules['requests'] = dummy
