

import os
import json
import urllib2

from time import time, strptime
from .exceptions import Unauthorized, Forbidden

cache = {}


def authenticate(headers, required_scopes=None):
    if 'Authorization' not in headers:
        raise Unauthorized('No SSO Token found in request headers.')

    try:
        bearer, auth_token = headers['Authorization'].split()

    except ValueError:
        raise Unauthorized('Invalid SSO token supplied in request.')

    token = check_token_cache(auth_token)

    if token is None:
        token = get_token_data(auth_token)
    
    verify_token_scopes(required_scopes, token)

    return token


def get_sso_data(token):
    url = os.environ.get('EVEAUTH_URL', 'https://login.eveonline.com/oauth/verify/')
    headers = {'Authorization': 'Bearer {}'.format(token)}
    request = urllib2.Request(url, headers=headers)

    response = urllib2.urlopen(request)
    response_json = json.load(response)

    if 'error' in response_json:
        raise Unauthorized(response_json['error_description'])

    data = {
        'character_id': response_json['CharacterID'],
        'character_name': response_json['CharacterName'],
        'character_owner_hash': response_json['CharacterOwnerHash'],
        'expires_on': strptime(response_json['ExpiresOn'], '%Y-%m-%dT%H:%M:%S'),
        'scopes': response_json['Scopes'],
        'token_type': response_json['TokenType'],
    }

    return data

def check_token_cache(auth_token):
    token = None
    cache_result = cache.get(auth_token, None)
    
    if cache_result is not None:
        token, expiration = cache_result
    
        if expiration < time():
            del cache[auth_token]
            token = None
    
    return token

def get_token_data(auth_token):
    token = get_sso_data(auth_token)
    
    expiration = time() + os.environ.get('EVEAUTH_CACHE_TIME', 300)

    if expiration > token['expires_on']:
        expiration = token['expires_on']

    cache[auth_token] = (token, expiration)

    return token

def verify_token_scopes(required_scopes, token):
    if required_scopes is not None:
        for rs in required_scopes:
            if rs not in token['scopes']:
                raise Forbidden('Missing required scopes.')
