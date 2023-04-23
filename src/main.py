import json
import attrs
from larksuiteoapi.event import handle_event, set_event_callback
from larksuiteoapi.model import OapiHeader, OapiRequest
from flask import Flask, request
from flask.helpers import make_response
from store.chat_history import init_db_if_required
from message_router import route_bot_message, route_im_message
from larksuiteoapi.service.im.v1.event import MessageReceiveEventHandler
from feishu.feishu_conf import feishu_conf
from util.app_config import app_config
from util.logger import app_logger,feishu_message_logger

init_db_if_required()

MessageReceiveEventHandler.set_callback(feishu_conf, route_im_message)
# set_event_callback(conf, "im.message.receive_v1", route_im_message)

app = Flask("feishu_bot")

@app.route('/', methods=['GET', 'POST'])
def ping():
    resp = make_response()
    resp.data = "pong"
    resp.status_code = 200
    return resp

@app.route('/bot_event', methods=['GET', 'POST'])
def bot_event():
    body = json.loads(request.data.decode(encoding="utf-8"))
    if "challenge" in body:
        resp = make_response()
        resp.data = json.dumps({"challenge": body["challenge"]})
        resp.status_code = 200
        return resp
    app_logger.debug("bot_event: %s", body)
    route_bot_message(body)
    resp = make_response()
    resp.data = "pong"
    resp.status_code = 200
    return resp 

@app.route('/webhook/event', methods=['GET', 'POST'])
def webhook_event():
    oapi_request = OapiRequest(uri=request.path, body=request.data, header=OapiHeader(
        request.headers))  # type: ignore[arg-type]
    resp = make_response()
    oapi_resp = handle_event(feishu_conf, oapi_request)
    resp.headers['Content-Type'] = oapi_resp.content_type
    resp.data = oapi_resp.body
    resp.status_code = oapi_resp.status_code
    return resp

MessageReceiveEventHandler.set_callback(feishu_conf, route_im_message)

def app_main():
    init_db_if_required()
    app.run(port=app_config.HTTP_PORT, host="0.0.0.0")

if __name__ == '__main__':
    app_main()