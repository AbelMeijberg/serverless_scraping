import random
import string


class SocialMediaWrapper:
    def __init__(self, key: str):
        self.key = key

    @staticmethod
    def _generate_random_string(length: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def get_dummy_response(self):
        # generate a random json
        dummy = {f"key{ind}": self._generate_random_string(10) for ind in range(10)}
        dummy["id"] = self._generate_random_string(10)
        return dummy
