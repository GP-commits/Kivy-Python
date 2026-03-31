"""
events.py - Dual-mode Event Dispatcher
Uses Kivy's Clock if available, otherwise falls back to standard Python threading.
This allows the network engine to be tested in "headless" environments.
"""

try:
    from kivy.event import EventDispatcher
    from kivy.clock import Clock
except ImportError:
    # --- HEADLESS FALLBACK (No Kivy installed) ---
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
                except Exception as e:
                    import traceback

                    traceback.print_exc()

            for h in list(self._bindings.get(event_name, [])):
                try:
                    h(*args, **kwargs)
                except Exception as e:
                    import traceback

                    traceback.print_exc()


# --- THE ACTUAL DISPATCHER ---
class NetworkDispatcher(EventDispatcher):
    """The bridge between background networking and the main thread."""

    __events__ = ("on_connected", "on_disconnected", "on_message_received", "on_error")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Default handlers
    def on_connected(self):
        pass

    def on_disconnected(self):
        pass

    def on_message_received(self, message_data):
        pass

    def on_error(self, error_message):
        pass

    def trigger_event_safely(self, event_name, *args):
        """
        The DRY way to safely push events to the main thread.
        Example: self.trigger_event_safely('on_error', "Connection dropped!")
        """
        Clock.schedule_once(lambda dt: self.dispatch(event_name, *args), 0)
