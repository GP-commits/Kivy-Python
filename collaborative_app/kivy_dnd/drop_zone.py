from kivy.properties import BooleanProperty
from .manager import drag_manager

class DropZoneBehavior:
    is_hovered = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        drag_manager.register_zone(self)

    def accepts_drag(self, draggable_widget):
        return True

    def on_drag_enter(self, draggable_widget):
        print(f"ENTERED: Something is hovering over {self}")
        self.is_hovered = True

    def on_drag_leave(self, draggable_widget):
        print(f"LEFT: The item left {self}")
        self.is_hovered = False

    def on_drop(self, draggable_widget):
        print(f"DROPPED: Successfully dropped on {self}")
        self.is_hovered = False