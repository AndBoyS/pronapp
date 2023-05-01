import json
import random
from pathlib import Path
from typing import List, Union, Dict, Set

from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from .utils import open_json, dump_json, get_formatted_modified_date_of_file, UrlRequestWithFailure


class MainApp(MDApp):
    # Список возможных результатов при нажатии кнопки
    data: Set[str]
    # Сколько времени дается на апдейт соуса при запуске приложения
    sauce_max_request_time: float = 3
    # Инфа о последнем времени обновлении соуса
    sauce_info: str

    sauce_path: Path = Path('data/sauce.json')
    sauce_url: str = 'https://raw.githubusercontent.com/AndBoyS/pronlib/main/sauce.json'
    checkpoint_path: Path = Path('data/checkpoint.json')
    checkpoint_data: Set[str]

    # Какой атрибут у json с чекпоинтами
    checkpoint_attr: str = 'used_sauce'

    label: MDLabel
    button: MDIconButton
    sauce_info_label: MDLabel
    checkpoint_info_label: MDLabel
    reset_button: MDIconButton

    def __init__(
            self,
            ):
        super().__init__()

        # Словарь {имя папки: количество вариантов в ней}
        sauce = self.request_sauce(self.sauce_url)
        if sauce is not None:
            dump_json(sauce, self.sauce_path)
        else:
            sauce = open_json(self.sauce_path)

        self.sauce_info = f'Sauce last update: {get_formatted_modified_date_of_file(self.sauce_path)}'

        self.load_data(sauce)
        self.setup_checkpoint()
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
                self.checkpoint_info_label,
                self.reset_button,
            )
        )

    def define_app_elements(self):

        self.label = MDLabel(
            text="Aboba",
            halign='center',
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            font_style='H4',
        )

        self.button = MDIconButton(
            icon='data/button.png',
            icon_size=200,
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            on_press=self.generate_callback,
        )

        self.sauce_info_label = MDLabel(
            text=self.sauce_info,
            halign='center',
            pos_hint={"center_x": 0.5, "center_y": 0.1},
            font_style='Subtitle1',
        )

        self.checkpoint_info_label = MDLabel(
            text=self.get_checkpoint_label(),
            halign='center',
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            font_style='H5',
        )

        self.reset_button = MDIconButton(
            icon="backup-restore",
            icon_size=130,
            # icon='data/restore.png',
            pos_hint={"center_x": 0.85, "center_y": 0.5},
            on_press=self.reset_checkpoint,
        )

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
        Распаковывает словарь соусов в множество возможных вариантов
        """
        self.data = set()
        for name, num in sauce.items():
            for i in range(1, num + 1):
                self.data = self.data | {f'{name} - {i}'}

    def get_possible_titles(self):
        return list(self.data - self.checkpoint_data)

    def generate_callback(self, event):
        possible_titles = self.get_possible_titles()
        if not possible_titles:
            self.reset_checkpoint()
            possible_titles = self.get_possible_titles()

        self.label.text = random.choice(possible_titles)
        self.update_checkpoint(self.label.text)

    def setup_checkpoint(self):

        if self.checkpoint_path.exists():
            # Множество уже выпавших тайтлов из self.data
            self.checkpoint_data = open_json(self.checkpoint_path)[self.checkpoint_attr]
            self.checkpoint_data = set(self.checkpoint_data) & self.data
        else:
            self.checkpoint_data = set()

    def update_checkpoint(self, title=None):
        if title is not None:
            self.checkpoint_data = self.checkpoint_data | {title}

        self.checkpoint_info_label.text = self.get_checkpoint_label()
        dump_json(
            {self.checkpoint_attr: list(self.checkpoint_data)},
            self.checkpoint_path,
        )

    def reset_checkpoint(self, event=None):
        self.checkpoint_data = set()
        self.update_checkpoint()

    def get_checkpoint_label(self):
        return f'{len(self.checkpoint_data)} / {len(self.data)}'
