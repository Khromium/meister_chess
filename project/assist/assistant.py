#!/usr/bin/env python
 
from __future__ import print_function
 
import argparse
import os.path
import json
 
import google.oauth2.credentials
 
from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
 
# 辞書オブジェクトの定義
speechdata = {}
# JSONファイルのパス
filepath = "/home/pi/Desktop/speech.json"
 
# JSONファイルの書き込み
def writeJson(path,data):
    with open(path,'w') as f:
        json.dump(data,f,indent=4)
 
# JSONデータ用初期化処理
def initJson():
     
    speechdata = {
        'status':'waiting',
        'txtStatus':'waiting',
        'txt':'',
    }
    writeJson(filepath,speechdata)
 
# 「process_event(event)()」にプログラムを追加していきます。
def process_event(event):
    speechdata['txt'] = ''
    if event.type == EventType.ON_START_FINISHED:
        print('ON_START_FINISHED')
     
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print('ON_CONVERSATION_TURN_STARTED')
         
        speechdata['status'] = 'start'
        speechdata['txtStatus'] = 'waiting'
        speechdata['txt'] = ''
        writeJson(filepath,speechdata)
 
    if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        print('ON_RECOGNIZING_SPEECH_FINISHED')
        print(event.args)
         
        queryTxt = event.args['text']
        speechdata['status'] = 'talking'
        speechdata['txtStatus'] = 'query'
        speechdata['txt'] = queryTxt
 
        writeJson(filepath,speechdata)
     
    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        print('ON_CONVERSATION_TURN_FINISHED')
 
        speechdata['status'] = 'finish'
        speechdata['txtStatus'] = 'waiting'
        speechdata['txt'] = ''
 
        writeJson(filepath,speechdata)
 
#「main()」は主に認証部分です。
def main():
 
    # Jsonデータ初期化
    initJson()
 
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
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))
 
    with Assistant(credentials,"zairiki") as assistant:
        for event in assistant.start():
            process_event(event)
 
# import文でモジュールとしてインポートされた場合ではなく
# コマンドラインから実行された時に「main()」を実行します。
if __name__ == '__main__':
    main()