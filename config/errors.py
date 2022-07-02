class ErrorMessages:
    ParseError = {
        "code": -32700,
        "message": "Parse Error",
        "data": "Invalid JSON was received by the server. An error occurred on the server while parsing the JSON text."
    }
    InvalidRequest = {
        "code": -32600,
        "message": "Invalid Request",
        "data": "The JSON sent is not a valid Request object."
    }
    MethodNotFound = {
        "code": -32601,
        "message": "Method Not Found",
        "data": "The method does not exist / is not available."
    }
    InvalidParams = {
        "code": -32602,
        "message": "Invalid Params",
        "data": "Invalid method parameter(s)."
    }
    InternalError = {
        "code": -32603,
        "message": "Internal Error",
        "data": "Internal JSON-RPC error."
    }
    ServerError = {
        "code": -32000,
        "message": "Server Error",
        "data": "Reserved for implementation-defined server-errors (-32000 to -32099)."
    }
