import socket

class Agent:
    def __init__(self, config):
        self.config = config
        self.domain = self.config['domain']

    def run(self):
        try:
            result = socket.getaddrinfo(self.domain, None)
            addresses = {addr for (*_, (addr, *_)) in result}
            return (True, 'Okay.')
        except Exception as err:
            return (False, f'Domain {self.domain} could not be resolved.\n{err}')
