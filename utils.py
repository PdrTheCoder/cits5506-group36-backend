from flask import jsonify


def ok_res(data, msg="ok"):
    return jsonify({"message": msg, "code": 0, "data": data})


def error_res(msg, code=-1):
    return jsonify({"message": msg, "code": code})
