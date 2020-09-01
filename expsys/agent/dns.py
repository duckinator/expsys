import socket

class Agent:
    def __init__(self, config):
        self.config = config
        self.domain = self.config['domain']

    def run(self):
        try:
            result = socket.getaddrinfo(self.domain, None)
            addresses = {addr for (*_, (addr, *_)) in result}
            return (True, ' '.join(addresses))
        except Exception as err:  # pylint: disable=broad-except
            return (False, f'Domain {self.domain} could not be resolved.\n{err}')
