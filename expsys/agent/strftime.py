from datetime import datetime

class Agent:
    """
    The strftime creates a datetime argument, calls strftime with the
    specified format variable, and checks if it matches the expected value.

    Example basic config, returning True if it's currently Sunday:
        {
            'type': 'strftime',
            'format': '%a',
            'match': 'Sun',
        }
    """

    DELAY = 0

    def __init__(self, config):
        self.format = config['format']
        self.match = config['match']

    def run(self):
        dt = datetime.now()
        result = dt.strftime(self.format)
        if result == self.match:
            return (True, result)
        else:
            return (False, result + f" ({dt.strftime('%Y-%m-%d')})")
