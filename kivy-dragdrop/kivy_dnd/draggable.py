from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget

class DraggableBehavior(Widget):
    """
    A mixin class that makes any Kivy widget draggable.
    Usage: class DraggableButton(DraggableBehavior, Button): pass
    """
    
    # We create custom events so other developers can trigger animations
    __events__ = ('on_drag_start', 'on_drag_success', 'on_drag_fail')

    # Keep track of where it came from so we can put it back if dropped in the wrong spot
    original_parent = ObjectProperty(None, allownone=True)
    original_pos = ListProperty([0, 0])
    original_size_hint = ListProperty([None, None])
    
    # Visual tweak: make it slightly transparent when dragged
    drag_opacity = NumericProperty(0.7)
    _original_opacity = NumericProperty(1.0)

    def on_touch_down(self, touch):
        # 1. Did they click exactly on this widget?
        if self.collide_point(*touch.pos):
            # Grab the touch so no other widget tries to use this swipe
            touch.grab(self)
            
            # Save its original state
            self.original_parent = self.parent
            self.original_pos = self.pos[:]
            self.original_size_hint = self.size_hint[:]
            self._original_opacity = self.opacity
            
            # Dispatch our custom start event
            self.dispatch('on_drag_start')
            return True # Tell Kivy we handled this touch
            
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        # 2. Are we currently the widget holding this touch?
        if touch.grab_current is self:
            # Move the center of the widget to exactly where the finger/mouse is
            self.center_x = touch.x
            self.center_y = touch.y
            return True
            
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        # 3. Did they let go?
        if touch.grab_current is self:
            touch.ungrab(self)
            
            # For Day 1 testing, we will just assume they failed to drop it in a zone.
            # (Person 2 will build the Drag Manager to check if this was a success tomorrow!)
            self.dispatch('on_drag_fail')
            return True
            
        return super().on_touch_up(touch)

    # --- Custom Event Handlers ---

    def on_drag_start(self):
        """Called automatically when picked up."""
        print(f"[{self.__class__.__name__}] Picked up!")
        
        if self.parent:
            # Break out of the layout jail!
            self.parent.remove_widget(self)
            
            # Force size so it doesn't collapse when removed from layout
            self.size_hint = (None, None) 
            
            # Add to the absolute top of the screen
            Window.add_widget(self)
            
            # Make it look like a ghost
            self.opacity = self.drag_opacity

    def on_drag_fail(self):
        """Called automatically if dropped in empty space."""
        print(f"[{self.__class__.__name__}] Dropped in the wrong place. Going home.")
        
        # Remove from the Window
        if self.parent == Window:
            Window.remove_widget(self)
            
        # Put it back exactly where it came from
        if self.original_parent:
            self.size_hint = self.original_size_hint
            self.pos = self.original_pos
            self.original_parent.add_widget(self)
            
        # Restore normal look
        self.opacity = self._original_opacity

    def on_drag_success(self):
        """Called if Person 2's Drop Zone accepts it."""
        print(f"[{self.__class__.__name__}] Successfully dropped!")
        self.opacity = self._original_opacity
        # The Manager/Drop Zone will handle re-parenting it.