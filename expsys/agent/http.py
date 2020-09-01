"""Agent for checking HTTP(S) servers."""

import urllib.request
import urllib.error


class Agent:  # pylint:disable=too-few-public-methods
    """HTTP agent for checking status code, contents, redirects, and errors."""

    def __init__(self, config):
        self.url = config.pop('url')
        if not config:
            config = {'status': 200}
        self.config = config

    def run(self):
        try:
            response = urllib.request.urlopen(self.url)
            # info = response.info()
            end_url = response.geturl()
            contents = response.read().decode()
            status_code = response.getcode()
        except urllib.error.URLError as err:
            return (False, str(err.reason))

        if 'status' in self.config.keys():
            if status_code != self.config['status']:
                return (False, f'Expected {self.config["status"]} status code, got {status_code}')

        if 'contents' in self.config.keys():
            if not self.config['contents'] in contents:
                return (False, f'Response did not include {self.config["contents"]!r}')

        if 'redirect' in self.config.keys():
            if self.config['redirect']:
                expected = self.config['redirect']
                if end_url != expected:
                    if end_url == self.url:
                        message = f'Expected redirect to {expected}, but was not redirected.'
                    else:
                        message = f'Expected redirect to {expected}, got redirect to {end_url}'
                    return (False, message)
            if self.config['redirect'] is False:
                if end_url != self.url:
                    return (False, f'Expected no redirect, but was redirected to {end_url}')

        return (True, 'Okay.')
