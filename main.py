import json
import random

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class MainApp(MDApp):
    def __init__(self, sauce_path: str = 'data/sauce.json'):
        super().__init__()
        self.label = MDLabel(text="Aboba", halign="center")

        with open(sauce_path, 'r') as f:
            sauce = json.load(f)

        self.data = []
        for name, num in sauce.items():
            for i in range(1, num+1):
                self.data.append(f'{name} - {i}')

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "A200"

        return(
            MDScreen(
                self.label,
                MDRectangleFlatButton(
                    text="Generate",
                    pos_hint={"center_x": 0.5, "center_y": 0.4},
                    on_press=self.generate_callback
                ),
                # Reset button
                MDIconButton(
                   icon="restore",
                   pos_hint={"center_x": 0.7, "center_y": 0.5},
                ),
            )
        )

    def generate_callback(self, event):
        self.label.text = random.choice(self.data)


if __name__ == '__main__':
    MainApp().run()
