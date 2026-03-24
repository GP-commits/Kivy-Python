from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

# Import our custom library behaviors!
from kivy_dnd.draggable import DraggableBehavior
from kivy_dnd.drop_zone import DropZoneBehavior

# 1. Make a Draggable Button
class DragButton(DraggableBehavior, Button):
    pass

# 2. Make a Drop Zone Layout
class DropBox(DropZoneBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        with self.canvas.before:
            # Give it a blue background so we can see it
            Color(0.2, 0.4, 0.8, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    # Override the drop zone events to make it visually react!
    def on_drag_enter(self, draggable_widget):
        super().on_drag_enter(draggable_widget)
        self.canvas.before.children[0].rgba = (0.2, 0.8, 0.4, 1) # Turn Green!

    def on_drag_leave(self, draggable_widget):
        super().on_drag_leave(draggable_widget)
        self.canvas.before.children[0].rgba = (0.2, 0.4, 0.8, 1) # Back to Blue

    def on_drop(self, draggable_widget):
        super().on_drop(draggable_widget)
        self.canvas.before.children[0].rgba = (0.2, 0.4, 0.8, 1) # Back to Blue
        
        # Actually move the widget into this box!
        if draggable_widget.parent:
            draggable_widget.parent.remove_widget(draggable_widget)
        
        draggable_widget.size_hint = (1, 0.5) # Resize it to fit the box
        self.add_widget(draggable_widget)


class DragAndDropApp(App):
    def build(self):
        root = FloatLayout()

        # Create the Drop Zone on the right side
        drop_zone = DropBox(size_hint=(0.4, 0.6), pos_hint={'right': 0.9, 'center_y': 0.5})
        drop_zone.add_widget(Label(text="Drop Items Here!"))
        
        # Create our draggable item on the left side
        btn = DragButton(
            text="Grab Me!", 
            size_hint=(None, None), size=(150, 50),
            pos=(50, 200)
        )

        root.add_widget(drop_zone)
        root.add_widget(btn)
        return root

if __name__ == "__main__":
    DragAndDropApp().run()