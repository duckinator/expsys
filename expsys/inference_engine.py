from lla.interpreter import Interpreter, UndefinedVariableException
from .agent_manager import AgentManager
from .notifications import NotificationManager


class InferenceEngine:
    def __init__(self, agents, rules):
        self.notifications = NotificationManager()
        self.agents = AgentManager(agents)
        self.rules = rules
        self._times = {}

    def get(self, name):
        return self[name]

    def __contains__(self, name):
        return name in self.rules or name in self.agents

    def __getitem__(self, name):
        if not isinstance(name, str):
            raise Exception(f'name is not a str: {name!r}')

        if name in self.rules:
            try:
                return Interpreter(self).run(self.rules[name])
            except UndefinedVariableException as err:
                print(f'ERROR: {err}')
                return None
        elif name in self.agents:
            return self.agents.get(name)

        print(f"ERROR: Couldn't resolve {name}.")
        return None
