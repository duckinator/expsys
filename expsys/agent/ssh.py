import subprocess


class Agent:
    DELAY = 60 * 10  # 10 minutes

    def __init__(self, config):
        self.config = config

    def run(self):
        try:
            command = ['ssh', self.config['dest'], *self.config['cmd']]
            result = subprocess.run(command,
                                    check=False,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            if result.returncode == 0:
                return (True, result.stdout)
            else:
                return (False, result.stderr)
        except Exception as err:
            return (False, str(err))
