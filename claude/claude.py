import requests
import json
import os
import uuid
import logging
from typing import List, Generator
from schema import Message
logger = logging.getLogger(__name__)
from tenacity import (
    before_sleep_log,
    retry,
    retry_base,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

import tzlocal


class Claude:

    base_url = 'https://claude.ai/api'
    timezone = "Asia/Shanghai"

    def __init__(self, session_key='', proxies=None,
                 model: str = 'claude-2',
                 timezone=None,
                 base_url: str = 'https://claude.ai/api'):
        session_key = session_key or os.getenv('CLAUDE_SESSION_KEY', '')

        if not session_key:
            raise ValueError('session_key is required')

        self.base_url = base_url
        self.model = model
        self.cookies = f'sessionKey={session_key}'
        self.proxies = proxies
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Content-Type': 'application/json',
            'Cookie': f'sessionKey={session_key};',
            'Sec-Ch-Ua': ('"Not/A)Brand";v="99", '
                          '"Google Chrome";v="115", '
                          '"Chromium";v="115"'),
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/115.0.0.0 Safari/537.36'),
        }
        if timezone:
            self.timezone = timezone
        else:
            self.timezone = tzlocal.get_localzone()
        self.organization_uuid = self._get_organization_uuid()  # 获取组织ID

    @property
    def get_organization_uuid(self):
        return self.organization_uuid

    @retry(stop=stop_after_attempt(3))
    def http_get(self, url):
        response = requests.get(url, headers=self.headers,
                                proxies=self.proxies)
        return response

    @retry(stop=stop_after_attempt(3))
    def http_post(self, url, data, stream=False):
        response = requests.post(url, data=json.dumps(data),
                                 headers=self.headers,
                                 proxies=self.proxies, stream=stream)
        return response

    def _get_organization_uuid(self):
        uuid = ''
        url = f'{self.base_url}/organizations'
        response = self.http_get(url=url)

        if response.status_code == 200:
            data = response.json()
            uuid = data[0]['uuid']

            # Process the response data and analyze the chatbot's API behavior
            # Extract relevant information from the data and observe any patterns
        else:
            # Handle the case when the request is not successful
            logger.error('Request failed with status code:'
                         f'{response.status_code}')
            logger.error('Please check the cookies you have entered.'
                         'If they are correct then Claude might be down')
        return uuid

    def new_conversation(self,
                         conversation_uuid: str = "",
                         name: str = "") -> None:
        url = f"{self.base_url}/organizations/{self.organization_uuid}/chat_conversations"
        # conversation_uuid = self.get_random_uuid()
        conversation_uuid = conversation_uuid or str(uuid.uuid4().hex)
        payload = json.dumps({"uuid": conversation_uuid, "name": name})
        response = self.http_post(url=url, data=payload)

        if response.status_code == 201:
            data = response.json()
            conversation_uuid = data['uuid']
            logger.info('New Conversation Created')
        else:
            logger.error('Request failed with status code:'
                         f'{response.status_code}\n'
                         'Unable to create a new conversation'
                         'please try again')
        new_conersation = Conversation(claude=self,
                                       conversation_uuid=conversation_uuid,
                                       name=name)
        return new_conersation

    def get_conversation(self,
                         conversation_uuid: str,
                         name: str = '') -> 'Conversation':
        """
        获取已存在的 conversation，如果不存在则创建
        """
        conversation_uuid = conversation_uuid or self._get_organization_uuid()
        return Conversation(claude=self,
                            conversation_uuid=conversation_uuid,
                            name=name)

    def get_conversations(self) -> List['Conversation']:
        url = f'{self.base_url}/organizations/{self.organization_uuid}/chat_conversations'
        req = self.http_get(url=url)
        return [Conversation(self, conv['uuid'], conv['name'])
                for conv in req.json()]


class Conversation:
    def __init__(self,
                 claude: Claude,
                 conversation_uuid: str,
                 name: str = ''):
        self.claude = claude
        self.conversation_uuid = conversation_uuid
        self.conversation_name = name

    @property
    def id(self) -> str:
        return self.conversation_uuid

    @property
    def name(self) -> str:
        return self.conversation_name

    def append_message(self, message: str, file_list=[]) -> 'str':
        url = f"{self.claude.base_url}/append_message"

        message = Message.add_message(text=message, file_list=file_list,
                                      conversation_uuid=self.conversation_uuid,
                                      organization_uuid=self.claude.organization_uuid)
        data = message.data
        response = self.claude.http_post(url=url, data=data)
        # response.raise_for_status()

        return Response(response)

    def __repr__(self):
        return ('Conversation("'
                f'{self.conversation_name}": {self.conversation_uuid})')


class Response:
    def __init__(self, response):
        self.response = response

    def stream_chunks(self) -> Generator[str, None, None]:
        # Extract completion values from lines starting with 'data:'
        # completions = ''
        for line in self.response.iter_lines():
            line = line.decode('utf-8')  # data: {"completion":"ã€‚","stop_re..
            if line.startswith('data:'):
                # {
                #     "completion":"",
                #     "stop_reason":"stop_sequence",
                #     "model":"claude-2.0",
                #     "stop":"\n\nHuman:",
                #     "log_id":"11de2f016c4b5924ce055e8596419d19eb4977dfb0650e3ce242665398361712",
                #     "messageLimit":
                #         {
                #             "type":"within_limit"
                #         }
                # }
                json_str = line.replace('data:', '').strip()
                json_obj = json.loads(json_str)
                completion = json_obj.get('completion')
                stop_reason = json_obj.get('stop_reason')
                model = json_obj.get('model')
                stop = json_obj.get('stop')
                log_id = json_obj.get('log_id')
                message_limit = json_obj.get('messageLimit')

                yield {
                        'completion': completion,
                        'stop_reason': stop_reason,
                        'model': model,
                        'stop': stop,
                        'log_id': log_id,
                        'message_limit': message_limit
                    }
                # if completion is not None:
                #     completions += completion

    def get_full_response(self) -> str:
        return ''.join(completion
                       for completion, _, _, _, _, _ in self.stream_chunks())
