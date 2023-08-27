#!/usr/bin/python3
""" view for users """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users/', methods=["GET"])
@app_views.route("/users/<user_id>", methods=["GET"])
def list_users(user_id=None):
    """ Lists users """
    if user_id:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        else:
            user = user.to_dict()
    else:
        user = []
        all_users = storage.all(User)
        for value in all_users.values():
            user.append(value.to_dict())
    return jsonify(user)


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """ Deletes a user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/", methods=["POST"])
def create_user():
    """ Creates a user """
    data = request.get_json()
    if not data:
        return jsonify("Not a JSON"), 400
    elif "email" not in data:
        return jsonify("Missing email"), 400
    elif "password" not in data:
        return jsonify("Missing password"), 400
    else:
        new_user = User()
        new_user.email = data["email"]
        new_user.password = data["password"]
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """ Updates a user """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    not_for_change = ["id", "created_at", "updated_at", "email"]
    for key, value in data.items():
        if key not in not_for_change:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
