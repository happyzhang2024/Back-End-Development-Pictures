from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for pic in data:
        if pic["id"] == id:
            return jsonify(pic)
    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if not request.is_json:
        return jsonify({"Message": "request body must be JSON"}), 400
    
    new_pic = request.get_json()
    if not new_pic:
        return jsonify({"Message": "missing picture data"}), 400
    if "id" not in new_pic:
        return jsonify({"Message": "missing 'id' field"}), 400
    print(new_pic)

    for pic in data:
        if new_pic["id"] == pic["id"]:
            return jsonify({"Message": f"picture with id {new_pic['id']} already present"}), 302
    
    data.append(new_pic)
    return jsonify(new_pic), 201
    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    if not request.is_json:
        return jsonify({"Message": "request body must be JSON"}), 400
    
    new_pic = request.get_json()
    if not new_pic:
        return jsonify({"Message": "picture not found"}), 404
    print(new_pic)

    for index, pic in enumerate(data):
        if pic["id"] == id:
            data[index] = new_pic
            return jsonify(pic), 201
    
    return jsonify({"Message": "picture not found"}), 404
    


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for pic in data:
        if pic["id"] == id:
            data.remove(pic)
            return "", 204
    return jsonify({"Message": "picture not found"}), 404

