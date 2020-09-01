from datetime import datetime

class Agent:
    def __init__(self, config):
        self.attribute = config.get('attribute', config['attr'])
        self.valid = config.get('valid', None)
        self.range = config.get('range', None)

        if self.range:
            self.range = range(*self.range)

    def run(self):
        result = getattr(datetime.now(), self.attribute)

        if self.valid:
            return (result in [*self.valid], result)

        if self.range:
            return (result in self.range, result)
