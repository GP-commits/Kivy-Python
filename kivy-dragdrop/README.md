# Kivy Drag and Drop 🎯

A lightweight and easy-to-use drag-and-drop behavior library for Kivy applications.

`kivy-dragdrop` allows you to add sophisticated drag-and-drop interactions to any Kivy widget effortlessly using pure Python. It brings an overarching Drag Manager that handles tracking widgets, hover states, dropping, and interaction zones.

## Features
- **Extremely Simple API:** Just use `DraggableBehavior` and `DropZoneBehavior` alongside your UI widgets.
- **Hover Detection:** Visual feedback when a draggable widget enters or leaves a drop zone.
- **Cross-Widget Drop Manager:** The internal `drag_manager` singleton seamlessly tracks items globally across your float layouts or screens.
- **Customizable Events:** Override `on_drag_enter`, `on_drag_leave`, and `on_drop` to trigger visual or structural changes exactly when you want them.

## Installation

You can install it directly or use it by copying the `kivy_dnd` package into your project's directory.

## Quick Start

### 1. Make a Widget Draggable

Inherit from `DraggableBehavior` to make any widget movable.

```python
from kivy_dnd.draggable import DraggableBehavior
from kivy.uix.button import Button

class DragButton(DraggableBehavior, Button):
    pass
```

### 2. Create a Drop Zone

Inherit from `DropZoneBehavior` to create a region that can receive draggables.
You can override hover and drop methods to change behavior or UI!

```python
from kivy_dnd.drop_zone import DropZoneBehavior
from kivy.uix.boxlayout import BoxLayout

class DropBox(DropZoneBehavior, BoxLayout):
    def on_drag_enter(self, draggable_widget):
        super().on_drag_enter(draggable_widget)
        # Change color to green when hovering!
        self.canvas.before.children[0].rgba = (0.2, 0.8, 0.4, 1) 

    def on_drag_leave(self, draggable_widget):
        super().on_drag_leave(draggable_widget)
        # Change color back to blue
        self.canvas.before.children[0].rgba = (0.2, 0.4, 0.8, 1)

    def on_drop(self, draggable_widget):
        super().on_drop(draggable_widget)
        self.canvas.before.children[0].rgba = (0.2, 0.4, 0.8, 1)
        
        # Remove from old parent and add to the drop box
        if draggable_widget.parent:
            draggable_widget.parent.remove_widget(draggable_widget)
        
        self.add_widget(draggable_widget)
```

## Running the Demo

Find a fully working example inside the `/demo` directory. Run it with:
```bash
python demo/main.py
```
