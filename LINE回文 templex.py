import requests
"""
作品名稱     ： Line templex
__author__ ： Ning 甯詠城
"""
# 一定要改的地方～～
auth_token = "hV0gN0T6RUKCAskSyGf4LbF1RxYUSqnHQqGZ9VEX4aV+TuyAnP4jYPGtOa+8L3Fvm4Eg0wlBXMj4nEwxWI68smcHAK/gVBOp3EQCsq4TzTiXIS1aZp/nwtmeSRjDHC59ngunTrdMGfR0PtUoZix06gdB04t89/1O/w1cDnyilFU="

from sys import version as python_version
from cgi import parse_header, parse_multipart
import socketserver as socketserver
import http.server
from http.server import SimpleHTTPRequestHandler as RequestHandler
from urllib.parse import parse_qs
import json
import requests


class MyHandler(RequestHandler):
    def do_POST(self):
        varLen = int(self.headers['Content-Length'])  # 取得讀取進來的網路資料長度
        if varLen > 0:
            post_data = self.rfile.read(varLen)  # 讀取傳過來的資料
            data = json.loads(post_data)  # 把字串 轉成JSON
            print(data)
            replyToken = data['events'][0]['replyToken']  # 回傳要用Token
            userId = data['events'][0]['source']['userId']  # 傳資料過來的使用者是誰
            text = data['events'][0]['message']['text']  # 用戶的傳遞過來的文字內容
            傳過來的資料型態 = data['events'][0]['message']['type']  # 傳過來的資料型態

        # 請參考
        # https://developers.line.biz/zh-hant/docs/messaging-api/sending-messages/#methods-of-sending-message
        message = {
            "replyToken": replyToken,
            "messages": [
                {
                    "type": "template",
                    "altText": "This is a buttons template",
                    "template": {
                        "type": "buttons",
                        "thumbnailImageUrl": "https://static.miraheze.org/hololivewiki/thumb/f/f9/Yukihana_Lamy_-_Portrait_02.png/580px-Yukihana_Lamy_-_Portrait_02.png",
                        "imageAspectRatio": "rectangle",
                        "imageSize": "cover",
                        "imageBackgroundColor": "#FFFFFF",
                        "title": "Menu",
                        "text": "Please select",
                        "defaultAction": {
                            "type": "uri",
                            "label": "View detail",
                            "uri": "https://www.youtube.com/channel/UCFKOVgVbGmX65RxO3EtH3iw"
                        },
                        "actions": [
                            {
                                "type": "postback",
                                "label": "Buy",
                                "data": "name=1&age=1"
                            },
                            {
                                "type": "uri",
                                "label": "Twitter",
                                "uri": "https://twitter.com/hololivetv"
                            },
                            {
                                "type": "uri",
                                "label": "wiki",
                                "uri": "https://virtualyoutuber.fandom.com/wiki/Yukihana_Lamy"
                            }
                        ]
                    }
                }

            ]
        }

        # 資料回傳 到 Line 的 https 伺服器
        hed = {'Authorization': 'Bearer ' + auth_token}
        url = 'https://api.line.me/v2/bot/message/reply'
        self.send_response(200)
        self.end_headers()
        requests.post(url, json=message, headers=hed)  # 把資料HTTP POST送出去


socketserver.TCPServer.allow_reuse_address = True  # 可以重複使用IP
httpd = socketserver.TCPServer(('0.0.0.0', 8888), MyHandler)  # 啟動WebServer   :8888
try:
    httpd.serve_forever()  # 等待用戶使用 WebServer
except:
    print("Closing the server.")
    httpd.server_close()  # 關閉 WebServer

