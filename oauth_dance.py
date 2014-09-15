import httplib
import oauth2 as oauth
import sys
import urlparse


def get_oauth_token(consumer_key, consumer_secret):
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)
    request_token_url = 'https://api.xero.com/oauth/RequestToken'
    resp, content = client.request(request_token_url, "POST")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
    request_token = dict(urlparse.parse_qsl(content))
    return  request_token


def get_oauth_token_page_url(request_token):
    authorize_url = "https://api.xero.com/oauth/Authorize"
    get_token_url = authorize_url + '?oauth_token=' + request_token['oauth_token']
    return get_token_url


def get_access_token(request_token, oauth_verifier, consumer_key, consumer_secret):
    access_token_url = 'https://api.xero.com/oauth/AccessToken'
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer, token)
    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))
    return  access_token


