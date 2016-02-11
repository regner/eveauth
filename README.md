# eveauth
[![Travis](https://img.shields.io/travis/Regner/eveauth.svg)](https://travis-ci.org/Regner/eveauth) [![PyPI](https://img.shields.io/pypi/v/eveauth.svg)](https://pypi.python.org/pypi/eveauth/)

A simple library for verifying authorization tokens provided against the EVE
Online SSO. Helper methods and decorators are provided for simplysimplifying the
ability to restrict access based on scopes or a character ID.

## Using
```python

from eveauth import authenticate

# Just get the token information back
token = authenticate(request)

# Require a specific scope
token = authenticate(request, ['character'])

# By default using the authenticate method directly will raise either a
# eveauth.Unauthorized or eveauth.Forbidden exception if something goes wrong or
# missing a scope.

# Decorate a flask view
from eveauth.contrib.flask import authenticate

@authenticate()
@app.route('/v1/<int:character_id>/')
def get_char_stats(character_id):
    if request.token['character_id'] != character_id:
        abort(403)

# The flask decorator will abort with a 401 or 403 if the eveauth package raises
# one if its exceptions. You only need to handle making sure the character the
# token is for is allowed the resource they are requesting.
```

## Environment Variables
* __EVEAUTH_URL:__ Defaults to 'https://login.eveonline.com/oauth/verify/'. The
URL which will be used to validate the authorization token.
* __EVEAUTH_CACHE_TIME:__ Defaults to 300. How long, in seconds, to cache the
response from the SSO server for.
* __AUTH_TESTING:__ 
* __TEST_TOKEN_DATA:__ 
