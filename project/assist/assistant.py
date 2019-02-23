#!/usr/bin/env python

from __future__ import print_function

import argparse
import os.path
import json
import re
import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file


class Assist:
    # 辞書オブジェクトの定義
    speechdata = {}
    # JSONファイルのパス
    filepath = "speech.json"

    def __init__(self, board, arm):
        """
        初期化部分でJSONの初期化とGoogle assistantの有効化を行っている
        なお、認証時には
        ~/.config/google-oauthlib-tool/credentials.json
        に認証ファイルが必要
        :param board:
        :param arm:
        """
        self.board = board
        self.arm = arm
        # Jsonデータ初期化
        self._initJson()
        # GoogleAssistantSDK認証
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("--credentials", type=existing_file,
                            metavar="OAUTH2_CREDENTIALS_FILE",
                            default=os.path.join(
                                os.path.expanduser("~/.config"),
                                "google-oauthlib-tool",
                                "credentials.json"
                            ),
                            help="Path to store and read OAuth2 credentials")
        # parser.add_argument('--query-text', '--query-text', type=str, metavar='QUERY_TEXT', default='Who am I',
        #                     help='comma separated text sent to the Assistant as if it were spoken by the user')
        args = parser.parse_args()
        with open(args.credentials, "r") as f:
            self.credentials = google.oauth2.credentials.Credentials(token=None,
                                                                     **json.load(f))

    def _name_to_character(self, piece_with_str: str):
        """
        名前を文字列に修正
        :param piece_with_str:
        :return:
        """
        pairs = {"ルーク": "R", "ビショップ": "B", "クイーン": "Q", "ナイト": "N", "ポーン": "P", "キング": "K"}
        for k, v in pairs.items():
            if piece_with_str.count(k):
                return v

    def send_to_arm(self, query_txt):
        """
        アームに司令を送る関数
        クエリのテキストから駒情報と移動先情報を取得して、送信する。
        :param query_txt:
        :return:
        """
        txt = re.sub(r"\n\s", "", query_txt, flags=(re.MULTILINE | re.DOTALL))
        piece = self._name_to_character(txt)
        field = re.search(r"[a-h][1-8]", txt)
        print(piece + "を" + field + "へ動かします。")

        san = piece + field
        route = self.board.piece_move_str(san)
        if len(route) != 1:  # イリーガルムーブだとrouteに[-1]が入ってる
            for pos in route:
                self.arm.move_pos(pos)
            print(str(route))
            self.board.board.push_san(san)
            self.board.check_state()
        else:
            print('無効な移動です。')
        self.arm.home_pos()

    def _writeJson(path, filepath ,data):
        """
        JSONファイルの書き込み
        :param path:
        :param data:
        :return:
        """
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    def _initJson(self):
        """
        JSONデータ用初期化処理
        :return:
        """
        self.speechdata = {
            "status": "waiting",
            "txtStatus": "waiting",
            "txt": "",
        }
        self._writeJson(self.filepath, self.speechdata)

    def _process_event(self, event):
        """
        ここでGOOGLE HOMEとのやり取りをテキストとしてフックして
        必要な処理を加えていくことで処理を実現する。
        :param event:
        :return:
        """
        self.speechdata["txt"] = ""
        # print("args:")
        # print(event)

        if event.type == EventType.ON_START_FINISHED:
            print("ON_START_FINISHED")

        if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            print("ON_CONVERSATION_TURN_STARTED")
            self.speechdata["status"] = "start"
            self.speechdata["txtStatus"] = "waiting"
            self.speechdata["txt"] = ""
            self._writeJson(self.filepath, self.speechdata)

        if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
            print("ON_RECOGNIZING_SPEECH_FINISHED")
            print(event.args)

            query_txt = event.args["text"]
            self.speechdata["status"] = "talking"
            self.speechdata["txtStatus"] = "query"
            self.speechdata["txt"] = query_txt

            self._writeJson(self.filepath, self.speechdata)

        # 応答のテキスト取得
        if event.type == EventType.ON_RENDER_RESPONSE:
            print("ON_RENDER_RESPONSE")
            print(event.args)
            query_txt = event.args["text"]
            self.speechdata["status"] = "talking"
            self.speechdata["txtStatus"] = "query"
            self.speechdata["txt"] = query_txt
            self._writeJson(self.filepath, self.speechdata)
            self.send_to_arm(query_txt)

        if event.type == EventType.ON_RESPONDING_STARTED:
            print("ON_RESPONDING_STARTED")
            print(event.args)

        if event.type == EventType.ON_RESPONDING_FINISHED:
            print("ON_RESPONDING_FINISHED")
            print(event.args)

        if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
                event.args and not event.args["with_follow_on_turn"]):
            print("ON_CONVERSATION_TURN_FINISHED")

            self.speechdata["status"] = "finish"
            self.speechdata["txtStatus"] = "waiting"
            self.speechdata["txt"] = ""

            self._writeJson(self.filepath, self.speechdata)

    def activate(self):
        """
        GOOGLE ASSISTANTを有効にして処理を行う部分
        :return:
        """
        with Assistant(self.credentials, "zairiki") as assistant:
            for event in assistant.start():
                self._process_event(event)
