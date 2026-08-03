import json


class JSONValidator:

    @staticmethod
    def validate(response: str):

        if not response:
            return False, None

        try:
            data = json.loads(response)
            return True, data

        except json.JSONDecodeError:
            return False, None