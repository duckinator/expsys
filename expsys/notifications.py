from typing import Dict


class NotificationManager:
    notifications: Dict[str, str] = {}

    def set(self, key: str, message: str):
        print(f'[MESSAGE/{key:<20}] {message!r}')
        self.notifications[key] = message

    def clear(self, key):
        self.set(key, None)
