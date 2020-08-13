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
            # TODO: Maybe use `response.info()` for headers and such?
            end_url = response.geturl()
            contents = response.read().decode()
            status_code = response.getcode()
        except (urllib.error.URLError, urllib.error.HTTPError) as err:
            return (False, str(err.reason))

        if 'status' in self.config.keys():
            if status_code != self.config['status']:
                return (False, f'Expected {self.config["status"]} status code, got {status_code}')

        if 'contents' in self.config.keys():
            if not self.config['contents'] in contents:
                return (False, f'Response did not include {self.config["contents"]!r}')

        if 'redirect' in self.config.keys():
            if self.config['redirect'] is True:
                if end_url != self.config['redirect']:
                    if end_url == self.url:
                        return (False, f'Expected redirect to {self.config["redirect"]}, but was not redirected.')
                    else:
                        return (False, f'Expected redirect to {self.config["redirect"]}, got redirect to {end_url}')
            if self.config['redirect'] is False:
                if end_url != self.url:
                    return (False, f'Expected no redirect, but was redirected to {end_url}')

        return (True, 'Okay.')
