"""Functions for managing agents."""

from datetime import datetime
import importlib
from typing import Any, Dict, Optional, Tuple


class AgentTask:
    """A single task, managed by a AgentManager."""

    def __init__(self, name: str, agent_config: Dict[str, Any]):
        self.last_run = 0
        self.name = name
        self.config = agent_config
        self.instance = self.get_agent_class(self.config['type'])(self.config)
        self.value = False
        self.message = None

    @staticmethod
    def _timestamp():
        return datetime.now().timestamp()

    def _expired(self, timestamp, duration):
        new_timestamp = self._timestamp()

        # If time goes backwards, bust the cache.
        if (new_timestamp - timestamp) < 0:
            return True

        return (new_timestamp - timestamp) >= duration

    def status(self) -> Tuple[bool, Optional[str]]:
        return (self.value, self.message)

    def run(self):
        # If the duration hasn't passed, bail early.
        if not self._expired(self.last_run, self.instance.DELAY):
            return self.status()

        self.last_run = self._timestamp()
        value, message = self.instance.run()
        self.value = value
        self.message = message
        return self.status()

    @staticmethod
    def get_agent_class(module_name):
        """Find and return the class for an agent."""
        return importlib.import_module(f"expsys.agent.{module_name}").Agent


class AgentManager:
    def __init__(self, agent_configs):
        self.agent_configs = agent_configs
        self._agents = {}
        self._setup()

    def _setup(self):
        for name, agent_config in self.agent_configs.items():
            print(f'[AGENT MANAGER] Adding agent {name!r}.')
            self._agents[name] = AgentTask(name, agent_config)

    def status(self, name):
        return self._agents[name].status()

    def __contains__(self, name):
        return name in self._agents

    def get(self, name, default=None):
        if name in self._agents:
            return self.__getitem__(name)
        else:
            return default

    def __getitem__(self, name):
        return self._agents[name].run()[0]

    @property
    def agents(self):
        return self._agents.keys()
