"""
master controller
"""

from flask import Blueprint
from flask import request, jsonify

from libs.helper import propagate_to_chain, log_rpc_call

api = Blueprint("RELAY API", __name__, url_prefix="/")


@api.route("/health", methods=["POST", "GET"])
def health():
    return "ok", 200


@api.route("/", methods=["POST"])
def index():
    """ flask dispatcher for controlling rpc requests
        @return: Response
    """
    log_rpc_call("query")
    req = request.get_data().decode()
    return jsonify(propagate_to_chain(req))
