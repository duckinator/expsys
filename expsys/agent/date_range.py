from datetime import datetime

class Agent:
    DELAY = 0

    def __init__(self, config):
        self.attribute = config.get('attribute', config['attr'])
        self.range = range(*config['range'])

    def run(self):
        result = getattr(datetime.now(), self.attribute)
        return (result in self.range, result)
