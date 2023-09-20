from flask import jsonify

def ok_res(data, msg="ok"):
    return jsonify(
        {
            "msg": msg,
            "code": 0,
            "data": data
        }
    )


def error_res(msg, code=-1):
    return jsonify(
        {
            "msg": msg,
            "code": code
        }
    )
    