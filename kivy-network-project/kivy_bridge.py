from kivy.event import EventDispatcher
from kivy.clock import Clock


class NetworkEventDispatcher(EventDispatcher):
    __events__ = ("on_connected", "on_message", "on_error")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_message=self.on_message_handler)

    def on_connected(self, *args):
        pass

    def on_message(self, message_data):
        pass

    def on_error(self, error_msg):
        pass

    def trigger_message_safely(self, data):
        Clock.schedule_once(lambda dt: self.dispatch("on_message", data), 0)

    def trigger_connected_safely(self, *args):
        Clock.schedule_once(lambda dt: self.dispatch("on_connected", *args), 0)

    def trigger_error_safely(self, error_msg):
        Clock.schedule_once(lambda dt: self.dispatch("on_error", error_msg), 0)
