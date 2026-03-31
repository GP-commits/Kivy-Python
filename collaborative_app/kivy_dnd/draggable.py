from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget

# 1. NEW: Import the manager!
from .manager import drag_manager 

class DraggableBehavior(Widget):
    __events__ = ('on_drag_start', 'on_drag_success', 'on_drag_fail')

    original_parent = ObjectProperty(None, allownone=True)
    original_pos = ListProperty([0, 0])
    original_size_hint = ListProperty([None, None])
    
    drag_opacity = NumericProperty(0.7)
    _original_opacity = NumericProperty(1.0)
    
    # 2. NEW: Keep track of the zone we are currently hovering over
    _current_hover_zone = ObjectProperty(None, allownone=True)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.original_parent = self.parent
            self.original_pos = self.pos[:]
            self.original_size_hint = self.size_hint[:]
            self._original_opacity = self.opacity
            self.dispatch('on_drag_start')
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.center_x = touch.x
            self.center_y = touch.y
            
            # --- NEW INTERACTION LOGIC ---
            # Ask the manager if our mouse is over a Drop Zone
            hovered_zone = drag_manager.get_hovered_zone(touch.pos)
            
            # If we crossed the border into a NEW zone (or left one)...
            if hovered_zone != self._current_hover_zone:
                # Tell the old zone we left
                if self._current_hover_zone:
                    self._current_hover_zone.on_drag_leave(self)
                
                # Tell the new zone we entered
                if hovered_zone and hovered_zone.accepts_drag(self):
                    hovered_zone.on_drag_enter(self)
                    
                self._current_hover_zone = hovered_zone
                
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            
            # --- NEW DROP LOGIC ---
            # Ask the manager one last time where we let go
            final_zone = drag_manager.get_hovered_zone(touch.pos)
            
            if final_zone and final_zone.accepts_drag(self):
                # Success! Tell the zone to accept the drop
                final_zone.on_drop(self)
                self.dispatch('on_drag_success')
            else:
                # Failure! We dropped it on empty space
                self.dispatch('on_drag_fail')
                
            # Clean up the hover state
            if self._current_hover_zone:
                self._current_hover_zone.on_drag_leave(self)
                self._current_hover_zone = None
                
            return True
        return super().on_touch_up(touch)

    # ... (Keep your on_drag_start, on_drag_fail, and on_drag_success exactly the same!)