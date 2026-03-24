import sys
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# Hack to find your library folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy_dnd.drop_zone import DropZoneBehavior
from kivy_dnd.manager import drag_manager

class MyLandingPad(DropZoneBehavior, Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Let's add a background color so we can see the exact borders of the zone
        with self.canvas.before:
            self.bg_color = Color(0.2, 0.2, 0.2, 1)  # Dark Gray by default
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            
        # Keep the background attached to the widget if the window resizes
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    # 2. Let's override the events you wrote in drop_zone.py to add visual flair!
    def on_drag_enter(self, draggable_widget):
        super().on_drag_enter(draggable_widget) # Keep the console print
        self.bg_color.rgba = (0, 0.6, 0.2, 1)   # Turn GREEN!

    def on_drag_leave(self, draggable_widget):
        super().on_drag_leave(draggable_widget) # Keep the console print
        self.bg_color.rgba = (0.2, 0.2, 0.2, 1) # Back to Dark Gray

class DemoApp(App):
    def build(self):
        layout = BoxLayout(padding=50, spacing=20)
        
        zone1 = MyLandingPad(text="Zone 1 (Drop Here)")
        zone2 = MyLandingPad(text="Zone 2 (Or Here)")
        
        layout.add_widget(zone1)
        layout.add_widget(zone2)
        
        # 3. FAKE PERSON 1: Track the mouse position constantly
        Window.bind(mouse_pos=self.simulate_drag_motion)
        
        # We need to remember which zone we are currently hovering over
        self.current_hovered_zone = None
        
        return layout

    def simulate_drag_motion(self, window, pos):
        """This runs every single time your mouse moves a pixel."""
        
        # Ask your manager: "Are these X/Y coordinates inside any registered zone?"
        hovered_zone = drag_manager.get_hovered_zone(pos)

        # Did the zone change? (e.g., we entered a new zone, or left a zone)
        if hovered_zone != self.current_hovered_zone:
            
            # If we were previously in a zone, tell it we left
            if self.current_hovered_zone is not None:
                self.current_hovered_zone.on_drag_leave(draggable_widget=None) # None because we don't have a real widget yet
                
            # If we just entered a new zone, tell it we arrived
            if hovered_zone is not None:
                hovered_zone.on_drag_enter(draggable_widget=None)
                
            # Update our tracker
            self.current_hovered_zone = hovered_zone

if __name__ == '__main__':
    DemoApp().run()