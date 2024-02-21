import json

import requests
from rest_framework.request import Request

from common.Route import Route


class BotTemplate(Route):

    def __init__(self, request: Request) -> None:
        super().__init__(request=request)

    def send(self, endpoint: str) -> requests.Response:
        yadro_response = super().send(endpoint=endpoint)
        response = self.__add_additional_fields_to_response(yadro_response)
        return response

    def __add_additional_fields_to_response(self, response: requests.Response) -> requests.Response:
        content = {'result': []}
        for obj in response.json()['result']:
            obj.update(self.__parse_name_field(obj['name']))
            content['result'].append(obj)

        response._content = json.dumps(content).encode('utf-8')

        return response

    @staticmethod
    def __parse_name_field(name_field: str) -> dict:
        split_values = name_field.split('-')

        fields_to_add = {}

        if 'gpt' in split_values:
            fields_to_add['bot_name'] = 'ChatGPT'

        fields_to_add['model_name'] = f'{split_values[0]}-{split_values[1]}'.title()

        mode_value = name_field.lower()
        if mode_value == 'gpt-3.5-turbo':
            fields_to_add['mode_name'] = '4K context'
        elif mode_value == 'gpt-4':
            fields_to_add['mode_name'] = '8K context'
        else:
            fields_to_add['mode_name'] = f'{split_values[-1].title()} context'

        return fields_to_add
