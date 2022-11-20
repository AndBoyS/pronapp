import os
import time
import json
from pathlib import Path
from typing import Union, Any

from kivy.network.urlrequest import UrlRequest


def open_json(fp: Union[str, Path]):
    with open(fp, 'r') as f:
        return json.load(f)


def dump_json(obj: Any, fp: Union[str, Path]):
    with open(fp, 'w') as f:
        json.dump(obj, f)


def get_formatted_modified_date_of_file(fp: Union[str, Path]):
    mod_time_raw = time.localtime(os.path.getmtime(fp))
    return time.strftime("%m/%d/%Y %I:%M:%S %p", mod_time_raw)


class UrlRequestWithFailure(UrlRequest):
    """
    UrlRequest из kivy
    Особенность - .wait метод имеет макс время ожидания max_request_time
    """
    def __init__(self,
                 url: str,
                 max_request_time: float = 10):
        super().__init__(url)
        self.max_request_time = max_request_time

    def wait(self, delay=0.5):
        """
        Wait for the request to finish (until :attr:`resp_status` is not
        None or self.max_request_time is passed)
        """
        total_time_passed = 0

        while self.resp_status is None and total_time_passed < self.max_request_time:
            self._dispatch_result(delay)
            time.sleep(delay)
            total_time_passed += delay
