import asyncio
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from kivy_network.network_client import RealTimeClient

class ChatUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        self.history = Label(text="Welcome to the App!\n", size_hint_y=0.8)
        self.history.bind(size=self.history.setter('text_size'))
        self.history.halign = 'left'
        self.history.valign = 'top'
        self.add_widget(self.history)
        
        bottom_bar = BoxLayout(size_hint_y=0.2)
        self.input_box = TextInput(multiline=False, hint_text="Type a message...")
        self.send_btn = Button(text="Send", size_hint_x=0.3)
        self.send_btn.bind(on_press=self.send_msg)
        
        bottom_bar.add_widget(self.input_box)
        bottom_bar.add_widget(self.send_btn)
        self.add_widget(bottom_bar)

        self.network = RealTimeClient("ws://localhost:8765")
        self.network.bind(on_connected=self.on_connect)
        self.network.bind(on_message=self.on_message)
        self.network.bind(on_disconnected=self.on_disconnect)

    def on_connect(self, instance):
        self.history.text += "[System]: Connected to Server!\n"
        asyncio.create_task(self.network.join_room("lobby"))

    def on_disconnect(self, instance):
        self.history.text += "[System]: Warning! Connection lost. Reconnecting...\n"

    def on_message(self, instance, message):
        if message.type == "admin":
            self.history.text += f"[Admin]: {message.content}\n"
        elif message.type == "message":
            short_id = message.sender_id[:4] if message.sender_id else "Unk"
            self.history.text += f"[User-{short_id}]: {message.content}\n"

    def send_msg(self, instance):
        text = self.input_box.text
        if text and self.network.connected:
            asyncio.create_task(self.network.send_chat("lobby", text))
            self.input_box.text = ""

class MultiplayerApp(App):
    def build(self):
        self.ui = ChatUI()
        asyncio.create_task(self.ui.network.run_forever())
        return self.ui

if __name__ == "__main__":
    asyncio.run(MultiplayerApp().async_run(async_lib='asyncio'))