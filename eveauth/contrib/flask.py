

from __future__ import absolute_import

import eveauth
import functools

from flask import request, abort, current_app


def authenticate(required_scopes=None, match_data=None):
    def decorator(target):
        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            if current_app.config.get('AUTH_TESTING', False) is True:
                request.token = current_app.config.get('TEST_TOKEN_DATA', {})

            else:
                try:
                    request.token = eveauth.authenticate(request.headers, required_scopes)
    
                except eveauth.Unauthorized as e:
                    abort(401, str(e))
    
                except eveauth.Forbidden as e:
                    abort(403, str(e))
            
            if match_data is not None:
                for element in match_data:
                    try:
                        if request.token[element] != kwargs[element]:
                            abort(403)
                    except KeyError as e:
                        abort(401, str(e))
                
            return target(*args, **kwargs)
        return wrapper
    return decorator
