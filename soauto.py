#!/usr/bin/env python
"""Auto-Login for StackOverflow"""

import json
import requests
from bs4 import BeautifulSoup
import sys
import config

__author__ = 'Pengyu CHEN'
__copyright__ = 'COPYLEFT, ALL WRONGS RESERVED.'
__credits__ = ['Pengyu CHEN']
__license__ = ''
__version__ = ''
__maintainer__ = 'Pengyu CHEN'
__email__ = 'pengyu@libstarrify.so'
__status__ = 'development'


def attempt_login(email, password, profile_url, per_request_timeout):
    """Attempts logging in to StackOverflow via StackExchange

    Args:
        email: Email of StackExchange.
        password: Password of StackExchange.
        per_request_timeout: Per request timeout in seconds.

    Returns:
        True on successful login, False on failure.

    Raises:
        None.
    """
    try:
        # Logging in to StackExchange
        session = requests.Session()
        login_url = 'https://stackoverflow.com/users/login'
        request = session.get(login_url, timeout=per_request_timeout)
        soup = BeautifulSoup(request.text)
        fkey = soup.select('input[name=fkey]')[0]['value']
        login_url = 'https://stackoverflow.com/users/login-or-signup/validation/track'
        login_data = {
            'isSignup': False,
            'isLogin': True,
            'isPassword': False,
            'isAddLogin': False,
            'hasCaptcha': False,
            'fkey': fkey,
            'email': email,
            'password': password,
            'submitbutton': 'Log In',
            }
        request = session.post(
            login_url,
            data=login_data,
            timeout=per_request_timeout)
        login_url = 'https://stackoverflow.com/users/login'
        login_data = {
            'fkey': fkey,
            'email': email,
            'password': password,
            }
        request = session.post(
            login_url,
            data=login_data,
            allow_redirects=False,
            timeout=per_request_timeout)
        if request.status_code == 302:
            index_url = 'http://stackoverflow.com/'
            request = session.get(index_url, timeout=per_request_timeout)
            profile_url = profile_url
            request = session.get(profile_url, timeout=per_request_timeout)
            return True, 'Logged-in successfully.'
        elif request.status_code == 200:
            return False, (
                'Logging-in failed. '
                'Maybe the email/password combination is incorrect.')
        else:
            raise Exception('This is not expected to happen.')

    except (requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError, requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects):
        return False, 'Connection error.'

    raise Exception('This line shall not be reached.')
    pass


def main():
    status, message = attempt_login(
        config.email,
        config.password,
        config.profile_url,
        config.per_request_timeout)
    print(message)
    pass

if __name__ == '__main__':
    main()
