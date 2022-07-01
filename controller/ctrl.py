"""
master controller
"""

from flask import Response, request
from flask import Blueprint

api = Blueprint("RELAY API", __name__, url_prefix="/")


@api.route("/", methods=["POST"])
def index():
    """ flask dispatcher for controlling rpc requests
        @return: Response
    """
    req = request.get_data().decode()

    return Response(None, content_type="application/json")
