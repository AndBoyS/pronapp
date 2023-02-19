import json
import random
from typing import List, Union, Dict

import requests
import time

from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from .utils import open_json, dump_json, get_formatted_modified_date_of_file, UrlRequestWithFailure


class MainApp(MDApp):
    # Список возможных результатов при нажатии кнопки
    data: List[str]
    # Сколько времени дается на апдейт соуса при запуске приложения
    sauce_max_request_time: float = 3
    # Инфа о последнем времени обновлении соуса
    sauce_info: str

    label: MDLabel
    button: MDIconButton
    sauce_info_label: MDLabel

    def __init__(self,
                 sauce_path: str = 'data/sauce.json',
                 sauce_url: str = 'https://raw.githubusercontent.com/AndBoyS/pronlib/main/sauce.json'):
        super().__init__()

        # Словарь {имя папки: количество вариантов в ней}
        sauce = self.request_sauce(sauce_url)
        if sauce is not None:
            dump_json(sauce, sauce_path)
        else:
            sauce = open_json(sauce_path)

        self.sauce_info = f'Sauce last update: {get_formatted_modified_date_of_file(sauce_path)}'

        self.load_data(sauce)
        self.define_app_elements()

    def build(self):

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "A200"

        return (
            MDScreen(
                self.label,
                self.button,
                self.sauce_info_label,
            )
        )

    def define_app_elements(self):

        self.label = MDLabel(
            text="Aboba",
            halign='center',
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            font_style='H4'
        )

        self.button = MDIconButton(
            icon='data/button.png',
            icon_size=200,
            # md_bg_color='#e9dff7',
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            on_press=self.generate_callback
        )

        self.sauce_info_label = MDLabel(
            text=self.sauce_info,
            halign='center',
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            font_style='Subtitle1',
        )

        #self.reset_button = MDIconButton(
        #   icon="restore",
        #   pos_hint={"center_x": 0.7, "center_y": 0.5},
        #)

    def request_sauce(self, url: str) -> Union[Dict[str, int], None]:
        """
        Если получится, скачать новую версию sauce
        """
        req = UrlRequestWithFailure(url=url, timeout=self.sauce_max_request_time)
        req.wait(delay=0.1)

        if req.is_finished and req.resp_status == 200:
            return json.loads(req.result)

        return None

    def load_data(self, sauce: Dict[str, int]) -> None:
        """
        Распаковывает словарь соусов в список возможных вариантов
        """
        self.data = []
        for name, num in sauce.items():
            for i in range(1, num + 1):
                self.data.append(f'{name} - {i}')

    def generate_callback(self, event):
        self.label.text = random.choice(self.data)
