try:
    from kivy.event import EventDispatcher
    from kivy.clock import Clock
except Exception:
    import threading

    class Clock:
        @staticmethod
        def schedule_once(callback, timeout=0):
            def _run():
                try:
                    callback(timeout if timeout else 0)
                except TypeError:
                    callback()
            t = threading.Timer(0 if timeout <= 0 else timeout, _run)
            t.daemon = True
            t.start()
            return t

    class EventDispatcher:
        def __init__(self, **kwargs):
            self._bindings = {}

        def bind(self, **kwargs):
            for name, fn in kwargs.items():
                self._bindings.setdefault(name, []).append(fn)

        def unbind(self, **kwargs):
            for name, fn in kwargs.items():
                if name in self._bindings:
                    try:
                        self._bindings[name].remove(fn)
                    except ValueError:
                        pass

        def dispatch(self, event_name, *args, **kwargs):
            method = getattr(self, event_name, None)
            if callable(method):
                try:
                    method(*args, **kwargs)
                except TypeError:
                    method(*args)
                except Exception:
                    import traceback

                    traceback.print_exc()
            for h in list(self._bindings.get(event_name, [])):
                try:
                    h(*args, **kwargs)
                except Exception:
                    import traceback

                    traceback.print_exc()
class NetworkMessenger(EventDispatcher):
    """
    The Kivy Bridge: Safely passes background network data to the Main UI Thread.
    """
    
    # 1. Register our custom events (the "shouts")
    __events__ = ('on_connected', 'on_disconnected', 'on_message_received', 'on_error')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # ------------------------------------------------------------------
    # TRIGGERS: Person 1 (The Network) will call these functions
    # ------------------------------------------------------------------

    def safe_trigger_message(self, message_data):
        """Passes a received message to the UI safely on the next frame."""
        Clock.schedule_once(lambda dt: self.dispatch('on_message_received', message_data), 0)

    def safe_trigger_connected(self):
        """Tells the UI we successfully connected to the server."""
        Clock.schedule_once(lambda dt: self.dispatch('on_connected'), 0)
        
    def safe_trigger_disconnected(self):
        """Tells the UI we lost connection."""
        Clock.schedule_once(lambda dt: self.dispatch('on_disconnected'), 0)

    def safe_trigger_error(self, error_msg):
        """Tells the UI something went wrong."""
        Clock.schedule_once(lambda dt: self.dispatch('on_error', error_msg), 0)

    # ------------------------------------------------------------------
    # DEFAULT EVENT HANDLERS: Person 4 (The UI) will override these
    # ------------------------------------------------------------------

    def on_connected(self, *args):
        pass

    def on_disconnected(self, *args):
        pass

    def on_message_received(self, message_data):
        pass
        
    def on_error(self, error_message):
        pass