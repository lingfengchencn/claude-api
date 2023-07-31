import mimetypes
import os
from typing import Optional


class Attachment:

    @staticmethod
    def get_mime_type(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            # 无法判断类型时,返回默认类型
            return 'application/octet-stream'
        else:
            return mime_type

    @classmethod
    def add(cls, file_path: str):

        with open(file_path, 'r') as f:
            text = f.read()
        file_type = cls.get_mime_type(file_path=file_path)

        attach_file = {
            'extracted_content': text,
            'file_name': os.path.basename(file_path),
            'file_size': os.path.getsize(file_path),
            'file_type': file_type,
            'totalPages': 0
        }
        return attach_file

    @classmethod
    def add_with_content(self, file_name: str, file_content: str,
                         file_type: str,
                         file_size: int = 0,
                         totalPages: int = 0):
        attach_file = {
            'extracted_content': file_content,
            'file_name': file_name,
            'file_size': file_size,
            'file_type': file_type,
            'totalPages': totalPages
        }
        return attach_file


class Completion:

    @classmethod
    def add(self, prompt: str = '', incremental: bool = True,
            model: str = 'claude-2.0',
            timezone: str = 'Asia/Shanghai'):
        completion = {
            'incremental': "true" if incremental else "false",
            'model': model,
            'prompt': prompt,
            'timezone': timezone
        }
        return completion


class Message:
    data = {
        'attachments': [],
        'completion': {},
        'conversation_uuid': '',
        'organization_uuid': '',
        'text': ''
    }

    @classmethod
    def add_message(cls, text: str,
                    file_list: Optional[str] = None,
                    conversation_uuid: Optional[str] = '',
                    organization_uuid: Optional[str] = '',
                    model: str = 'claude-2',
                    incremental: bool = True,
                    timezone: str = 'Asia/Shanghai') -> None:
        cls.data['conversation_uuid'] = conversation_uuid
        cls.data['organization_uuid'] = organization_uuid
        cls.data['text'] = text

        completion = Completion.add(prompt=text, timezone=timezone,
                                    model=model, incremental=incremental)
        cls.data['completion'] = completion

        if file_list is not None:
            for file in file_list:
                attachment = Attachment.add(file_path=file)
                cls.data['attachments'].append(attachment)
        return cls
