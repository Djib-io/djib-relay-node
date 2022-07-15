"""
main application source
"""

import logging
import sys

import requests
from flask import Flask, has_request_context, request
from flask_cors import CORS

from config.errors import ErrorMessages
from controller.ctrl import api


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr
        if has_request_context():
            record.method = request.path
            record.remote_addr = ip
            record.scheme = request.scheme
            record.agent = request.user_agent
        else:
            record.method = None
            record.remote_addr = None
        return super().format(record)


def create_server():
    server = Flask(__name__)
    server.config.from_pyfile("config/app.py")

    @server.after_request
    def after_request(response):
        """
        logging after every request
        """
        server.logger.info(
            "WWW-REQUEST Status{%s} Length{%s} referrer{%s}",
            response.status,
            response.content_length,
            request.referrer
        )
        return response

    @server.errorhandler(404)
    def page_not_found(e):
        return {
                   "jsonrpc": "2.0",
                   "error": ErrorMessages.MethodNotFound,
                   "id_": 0
               }, 200

    @server.errorhandler(400)
    def invalid_param(e):
        return {
                   "jsonrpc": "2.0",
                   "error": ErrorMessages.InvalidRequest,
                   "id_": 0
               }, 200

    @server.errorhandler(500)
    def internal_error(e):
        server.logger.error(str(e))
        return {
                   "jsonrpc": "2.0",
                   "error": ErrorMessages.InternalError,
                   "id_": 0
               }, 200

    server.register_blueprint(api)
    return server


if __name__ == '__main__':
    app = create_server()
    CORS(app)
    log = logging.getLogger("werkzeug")
    log.disabled = True
    formatter = RequestFormatter(
        '[%(asctime)s] %(levelname)s %(remote_addr)s UserAgent{%(agent)s} requested %(method)s in Module{%(module)s}: %(message)s'
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    print("\n * Machine Public IP: ", requests.get('https://api.ipify.org').text, "\n")
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'), use_reloader=False)
