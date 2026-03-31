import json
import asyncio

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

# These are now local packages within the collaborative_app directory
from kivy_dnd.draggable import DraggableBehavior
from kivy_dnd.drop_zone import DropZoneBehavior
from kivy_network.network_client import RealTimeClient

class TaskItem(DraggableBehavior, Button):
    pass

class ZoneBoard(DropZoneBehavior, BoxLayout):
    def __init__(self, zone_id, **kwargs):
        super().__init__(**kwargs)
        self.zone_id = zone_id
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        with self.canvas.before:
            Color(0.2, 0.3, 0.4, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_drag_enter(self, draggable_widget):
        super().on_drag_enter(draggable_widget)
        self.canvas.before.children[0].rgba = (0.3, 0.6, 0.4, 1)

    def on_drag_leave(self, draggable_widget):
        super().on_drag_leave(draggable_widget)
        self.canvas.before.children[0].rgba = (0.2, 0.3, 0.4, 1)

    def on_drop(self, draggable_widget):
        super().on_drop(draggable_widget)
        self.canvas.before.children[0].rgba = (0.2, 0.3, 0.4, 1)
        
        # 1. Visually move the item on our screen
        self.move_item_here(draggable_widget)
        
        # 2. Broadcast the move to the server
        app = App.get_running_app()
        if app.network and app.network.connected and app.network.websocket:
            payload = {
                "type": "move",
                "task_id": draggable_widget.text,
                "target_zone": self.zone_id
            }
            asyncio.create_task(app.network.websocket.send(json.dumps(payload)))
            
    def move_item_here(self, widget):
        if widget.parent:
            widget.parent.remove_widget(widget)
        widget.size_hint = (1, 0.2)
        self.add_widget(widget)


class CollaborativeBoardApp(App):
    def build(self):
        root = FloatLayout()
        
        # Create 'To Do' Zone
        self.todo_zone = ZoneBoard("todo", size_hint=(0.4, 0.8), pos_hint={'x': 0.05, 'center_y': 0.5})
        self.todo_zone.add_widget(Label(text="TO DO", size_hint_y=0.1, bold=True))
        
        # Create 'Done' Zone
        self.done_zone = ZoneBoard("done", size_hint=(0.4, 0.8), pos_hint={'right': 0.95, 'center_y': 0.5})
        self.done_zone.add_widget(Label(text="DONE", size_hint_y=0.1, bold=True))
        
        # Create our draggable tasks
        self.tasks = {
            "Fix Login Bug": TaskItem(text="Fix Login Bug", size_hint=(1, 0.2)),
            "Write README": TaskItem(text="Write README", size_hint=(1, 0.2)),
            "Drink Coffee": TaskItem(text="Drink Coffee", size_hint=(1, 0.2)),
        }
        
        # Add all tasks to 'To Do' initially
        for task in self.tasks.values():
            self.todo_zone.add_widget(task)
            
        root.add_widget(self.todo_zone)
        root.add_widget(self.done_zone)
        
        # Start Networking
        self.network = RealTimeClient("ws://localhost:8765")
        self.network.bind(on_message_received=self.on_network_message)
        asyncio.create_task(self.network.run_forever())
            
        return root

    def on_network_message(self, instance, message):
        # We got a message from the network!
        if message.type == "move":
            data = message.raw_data
            task_id = data.get("task_id")
            target_zone_id = data.get("target_zone")
            
            # Find the task
            task = self.tasks.get(task_id)
            if not task:
                return
                
            # Move the task
            if target_zone_id == "todo":
                self.todo_zone.move_item_here(task)
            elif target_zone_id == "done":
                self.done_zone.move_item_here(task)

if __name__ == "__main__":
    asyncio.run(CollaborativeBoardApp().async_run(async_lib='asyncio'))
