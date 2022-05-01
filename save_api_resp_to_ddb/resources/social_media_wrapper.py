import random
import string
from typing import Dict
import time
from datetime import datetime


class SocialMediaWrapper:
    def __init__(self, key: str):
        self.key = key
        self.fake_api_call_counter = 0

    @staticmethod
    def _generate_random_string(length: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def get_dummy_response(self, request_id: str) -> Dict[str, str]:
        # generate a random json, we don't actually use the request_id
        dummy = {f"key{ind}": self._generate_random_string(10) for ind in range(10)}
        dummy["id"] = self._generate_random_string(10)
        self.fake_api_call_counter += 1
        return dummy

    def check_if_rate_limit_hit(self) -> bool:
        rate_limit_hit = False
        if self.fake_api_call_counter > 10:
            self.fake_api_call_counter = 0
            rate_limit_hit = True
        return rate_limit_hit

    @staticmethod
    def get_ratelimit_reset_time() -> str:
        fake_reset_time = int(time.time()) + 30
        utc_dt = datetime.utcfromtimestamp(fake_reset_time)
        return utc_dt.strftime("%Y-%m-%dT%H:%M:%S%zZ")

