from lla.interpreter import Interpreter, UndefinedVariableException
from .agent_manager import AgentManager
from .notifications import NotificationManager


class InferenceEngine:
    def __init__(self, agents, rules):
        self.notifications = NotificationManager()
        self.inferences = {}
        self.agents = AgentManager(agents)
        self.interpreter = Interpreter(self)
        self.rules = rules
        self._times = {}

    def get(self, name):
        return self[name]

    def __contains__(self, name):
        return name in self.rules or name in self.inferences or name in self.agents

    def __getitem__(self, name):
        if not isinstance(name, str):
            raise Exception(f'name is not a str: {name!r}')

        if name in self.rules:
            try:
                result = self.interpreter.run(self.rules[name])
            except UndefinedVariableException as err:
                print(f'ERROR: {err}')
                return None
        else:
            result = self.inferences.get(name, self.agents.get(name))

        if result is None:
            print(f"ERROR: Couldn't resolve {name}.")
        return result
