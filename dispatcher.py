# dispatcher.py

from kivy.event import EventDispatcher
from kivy.clock import Clock

class NetworkDispatcher(EventDispatcher):
    """
    The safe bridge between the background network and the Kivy UI.
    Developers will use this to listen for network events.
    """
    
    # 1. Register the custom events Kivy needs to know about
    __events__ = (
        'on_connected', 
        'on_disconnected', 
        'on_message_received',
        'on_error'
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # ----------------------------------------------------------------------
    # 2. DEFAULT EVENT HANDLERS
    # Kivy requires these methods to exist for the __events__ tuple.
    # We leave them empty (pass) because the user  will 
    # write their own code to handle them in their app.
    # ----------------------------------------------------------------------
    def on_connected(self):
        pass

    def on_disconnected(self):
        pass

    def on_message_received(self, message_data):
        pass
        
    def on_error(self, error_message):
        pass

    # ----------------------------------------------------------------------
    # 3. THE MAGIC BRIDGE (Thread-Safe Dispatcher)
    # ----------------------------------------------------------------------
    def trigger_event_safely(self, event_name, *args):
        """
        The Connector will call this method from their background 
        network thread whenever data arrives.
        
        Using Clock.schedule_once safely pushes the data onto Kivy's 
        Main Thread on the very next frame, preventing UI crashes.
        """
        # We use a lambda function so we can pass the arguments dynamically
        Clock.schedule_once(lambda dt: self.dispatch(event_name, *args), 0)