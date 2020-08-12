class NotificationManager:
    notifications = {}

    def set(self, key, message):
        # TODO: Actually do something with it.
        print(f'[MESSAGE/{key:<20}] {message!r}')
        self.notifications[key] = message

    def clear(self, key):
        self.set(key, None)
