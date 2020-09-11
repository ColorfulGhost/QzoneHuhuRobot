from flask import Flask
from flask_restful import Api, Resource, reqparse
from Qzone_auto_twitter import QzoneSpider as autoTwitter
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True, encoding='utf-8')


class QzoneHuhuRobot(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("msg")

    def post(self):
        args = self.parser.parse_args()
        msg = args.get("msg")

        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
                autoTwitter().pMsg(msg=msg)
                success = True
                return "发送成功", 200
            except:
                print("出现错误正在重试...")
                attempts += 1
                if attempts == 3:
                    return "超过重试次数 结束程序", 500


if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(QzoneHuhuRobot, "/sendMsgToQQZone")

    app.run(
        host='0.0.0.0',
        port=89,
        debug=True)
