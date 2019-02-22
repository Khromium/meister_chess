#!/usr/bin/env python

from __future__ import print_function

import argparse
import os.path
import json

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

class Assist:
    # 辞書オブジェクトの定義
    speechdata = {}
    # JSONファイルのパス
    filepath = "/home/pi/Desktop/speech.json"

    def __init__(self):
        # Jsonデータ初期化
        self.initJson()
        # GoogleAssistantSDK認証
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--credentials', type=existing_file,
                            metavar='OAUTH2_CREDENTIALS_FILE',
                            default=os.path.join(
                                os.path.expanduser('~/.config'),
                                'google-oauthlib-tool',
                                'credentials.json'
                            ),
                            help='Path to store and read OAuth2 credentials')
        args = parser.parse_args()
        with open(args.credentials, 'r') as f:
            self.credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))


    # JSONファイルの書き込み
    def writeJson(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    # JSONデータ用初期化処理
    def initJson(self):

        self.speechdata = {
            'status': 'waiting',
            'txtStatus': 'waiting',
            'txt': '',
        }
        self.writeJson(self.filepath, self.speechdata)

    # 「process_event(event)()」にプログラムを追加していきます。
    def process_event(self, event):
        self.speechdata['txt'] = ''
        if event.type == EventType.ON_START_FINISHED:
            print('ON_START_FINISHED')

        if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            print('ON_CONVERSATION_TURN_STARTED')

            self.speechdata['status'] = 'start'
            self.speechdata['txtStatus'] = 'waiting'
            self.speechdata['txt'] = ''
            self.writeJson(self.filepath, self.speechdata)

        if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
            print('ON_RECOGNIZING_SPEECH_FINISHED')
            print(event.args)

            queryTxt = event.args['text']
            self.speechdata['status'] = 'talking'
            self.speechdata['txtStatus'] = 'query'
            self.speechdata['txt'] = queryTxt

            self.writeJson(self.filepath, self.speechdata)

        if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
                event.args and not event.args['with_follow_on_turn']):
            print('ON_CONVERSATION_TURN_FINISHED')

            self.speechdata['status'] = 'finish'
            self.speechdata['txtStatus'] = 'waiting'
            self.speechdata['txt'] = ''

            self.writeJson(self.filepath, self.speechdata)

    # 「main()」は主に認証部分です。
    def main(self):

        with Assistant(self.credentials, "zairiki") as assistant:
            for event in assistant.start():
                self.process_event(event)


# import文でモジュールとしてインポートされた場合ではなく
# コマンドラインから実行された時に「main()」を実行します。
if __name__ == '__main__':
    Assist.main()
