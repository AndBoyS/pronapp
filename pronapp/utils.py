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
    # subclassed to use timeout in blocking wait()
    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)
        self.start_time = time.time()  # new attribute to keep track of request duration

    def wait(self, delay=0.5):
        # modified While to 'and' timeout not expired
        while (self.resp_status is None) and (self.start_time + self._timeout > time.time()):
            self._dispatch_result(delay)
            time.sleep(delay)
