import json
from typing import Tuple

import flask
from flask import current_app
from requests import post

from config.app import LEADER_NODE, RELAY_ID
from config.errors import *


def log_rpc_call(name: str):
    """ log rpc calls
        @param name: str
    """
    current_app.logger.info("RPC-CALL{%s}" % name)


def get_ip_and_agent() -> Tuple[str, str]:
    """ extract request ip and agent
        @return: Tuple[str, str]
    """
    agent = flask.request.user_agent if flask.has_request_context() else ""
    ip = flask.request.headers.getlist("X-Forwarded-For")[0] if flask.request.headers.getlist(
        "X-Forwarded-For") else flask.request.remote_addr
    ip = str(ip).split(',')[1].replace(' ', '') if "," in ip else ip
    return str(ip), str(agent)


def response_error(error_dict: dict, id_: int = 0) -> str:
    """ error response to client
        @param error_dict: dict
        @param id_: int
        @return: str
    """
    return {
        "jsonrpc": "2.0",
        "error": error_dict,
        "id": id_ if id_ is not None else 0
    }


def response_success(success: int | list | str | tuple | dict, id_: int = 0) -> str:
    """ error response to client
        @param success: int | list | str | tuple | dict
        @param id_: int
        @return: str
    """
    return {
        "jsonrpc": "2.0",
        "result": success,
        "id": id_ if id_ is not None else 0
    }


def propagate_to_chain(body: str):
    """ propagate body request to chain
        @param body: str
        @return: Response
    """
    if (json_obj := deserialize(body)) is None:
        current_app.logger.error(f"Error, ParseError, Body: {body}")
        return response_error(error_dict=ErrorMessages.ParseError)
    ip, agent = get_ip_and_agent()
    json_obj['params'].append({
        "relay_id": RELAY_ID,
        "client_ip": ip,
        "client_agent": agent
    })
    try:
        chain_data = json.dumps(json_obj)
        chain_response = post(LEADER_NODE, json=chain_data).json()
        if "error" in chain_response:
            return response_error(chain_response['error'], chain_response['id'])
        return response_success(chain_response['result'], chain_response['id'])
    except Exception as e:
        current_app.logger.critical(str(e))
        return response_error(error_dict=ErrorMessages.ParseError)


def deserialize(json_str: str) -> dict:
    """ deserialize json string to dictionary
        @param json_str: str
        @return: dict
    """
    try:
        obj = json.loads(json_str)
        if "id" not in obj or not isinstance(obj['id'], int):
            return None
        if "method" not in obj or not isinstance(obj['method'], str):
            return None
        if "params" not in obj or not isinstance(obj['params'], list):
            return None
        if "jsonrpc" not in obj or not isinstance(obj['jsonrpc'], str) or obj['jsonrpc'] != '2.0':
            return None
        return obj
    except Exception as e:
        current_app.logger.error(f"cannot serialize json_str({json_str}) to dict: {str(e)}")
        return None
