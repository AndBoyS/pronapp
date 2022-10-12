import json
import random

from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class BigAssButton(MDFloatingActionButton):
    """
    Опций в родительской кнопке на размер всего три

    Эта штука позволит увеличить кнопки с типом large еще больше
    """

    # Насколько мы увеличиваем размер кнопки по сравнению с обычной версией large
    multiplier = 1.3

    def set__radius(self, *args) -> None:
        super().set__radius(*args)
        if self.type == "large" and self.theme_cls.material_style != "M2":
            self._radius = dp(int(28*self.multiplier))

    def set_size(self, *args) -> None:
        super().set_size(*args)
        if self.type == "large" and self.theme_cls.material_style != "M2":
            raw_size = int(96*self.multiplier)
            self.size = dp(raw_size), dp(raw_size)


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
        self.theme_cls.material_style = "M3"

        return(
            MDScreen(
                self.label,
                BigAssButton(
                    icon='circle',
                    type='large',
                    pos_hint={"center_x": 0.5, "center_y": 0.35},
                    on_press=self.generate_callback
                ),
                # Reset button
                MDIconButton(
                    icon="restore",
                    #type='standart',
                    pos_hint={"center_x": 0.7, "center_y": 0.5},
                ),
            )
        )

    def generate_callback(self, event):
        self.label.text = random.choice(self.data)


if __name__ == '__main__':
    MainApp().run()