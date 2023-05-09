from larksuiteoapi.card import handle_card, set_card_callback
from larksuiteoapi.event import handle_event, set_event_callback
from larksuiteoapi.model import OapiHeader, OapiRequest
from flask import Flask, request
from flask.helpers import make_response
from larksuiteoapi.service.im.v1.event import MessageReceiveEventHandler

from message_router import route_im_message
from message_action import action_im_message, delayedUpdateMessageCard
from feishu.feishu_conf import feishu_conf
from util.app_config import app_config

MessageReceiveEventHandler.set_callback(feishu_conf, route_im_message)
set_card_callback(feishu_conf, action_im_message)

app = Flask("feishu_sd_bot")

# 参考 https://github.com/larksuite/oapi-sdk-python/blob/main/README.zh.md


@app.route("/", methods=["GET", "POST"])
def ping():
    resp = make_response()
    resp.data = "pong"
    resp.status_code = 200
    return resp


@app.route("/webhook/card", methods=["POST"])
def webhook_card():
    oapi_request = OapiRequest(
        uri=request.path, body=request.data, header=OapiHeader(request.headers)
    )
    resp = make_response()
    oapi_resp = handle_card(feishu_conf, oapi_request)
    resp.headers["Content-Type"] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp


@app.route("/webhook/event", methods=["GET", "POST"])
def webhook_event():
    oapi_request = OapiRequest(
        uri=request.path, body=request.data, header=OapiHeader(request.headers)
    )  # type: ignore[arg-type]
    resp = make_response()
    oapi_resp = handle_event(feishu_conf, oapi_request)
    resp.headers["Content-Type"] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp


def app_main():
    app.run(port=app_config.HTTP_PORT, host="0.0.0.0")


if __name__ == "__main__":
    app_main()
