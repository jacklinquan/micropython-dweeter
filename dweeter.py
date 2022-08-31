"""A python module for messaging through the free dweet service.

- Author: Quan Lin
- License: MIT
"""

__version__ = "0.2.0"
__all__ = ["DweeterError", "Dweeter"]

import time
import json
from hashlib import sha256
from cryptodweet import CryptoDweet, to_bytes, from_bytes

BASE_URL = "https://dweet.io"


class DweeterError(Exception):
    pass


class Dweeter:
    utc_format = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z"

    def __init__(
        self,
        mailbox="default mailbox",
        key="default key",
        debug=False,
        base_url=BASE_URL,
    ):
        self.mailbox = mailbox
        hash_result = sha256(to_bytes(key)).digest()
        cd_key = hash_result[:16]
        cd_iv = hash_result[16:]
        self._cd = CryptoDweet(cd_key, cd_iv, base_url=base_url)
        self.debug = debug
        self.latest = None

    def send_data(self, data_dict):
        if not isinstance(data_dict, dict):
            raise DweeterError("data_dict must be instance of dict.")

        time_string = self.utc_format.format(*(time.gmtime()[:6]))
        data_dict_copy = data_dict.copy()
        data_dict_copy["remote_time"] = time_string
        data_json = json.dumps(data_dict_copy)
        res = None

        try:
            res = self._cd.dweet_for(self.mailbox, {time_string: data_json})
        except Exception as exc:
            if self.debug:
                print(type(exc).__name__, exc)

        return res

    def get_new_data(self):
        try:
            res = self._cd.get_latest_dweet_for(self.mailbox)
            content = res[0]["content"]
            created = res[0]["created"]
            time_string = list(content.keys())[0]
            data_json = list(content.values())[0]
            data_dict = json.loads(data_json)
            data_dict["created_time"] = created
            if data_dict["remote_time"] != time_string:
                raise DweeterError("Received data is compromised!")
        except Exception as exc:
            if self.debug:
                print(type(exc).__name__, exc)
            return None
        else:
            if (self.latest is None) or (
                self.latest["created_time"] < data_dict["created_time"]
            ):
                self.latest = data_dict
                return data_dict
            else:
                return None
