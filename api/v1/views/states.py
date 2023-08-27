#!/usr/bin/python3
""" States view """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=["GET"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def list_states(state_id=None):
    """ Lists states """
    if state_id:
        states = storage.get(State, state_id)
        if states:
            states = states.to_dict()
        else:
            abort(404)
    else:
        states = []
        states_all = storage.all(State)
        for value in states_all.values():
            states.append(value.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/", methods=["POST"], strict_slashes=False)
def create_state():
    """ Creates a state """
    data = request.get_json()
    if not data:
        return jsonify("Not a JSON"), 400
    elif "name" not in data:
        return jsonify("Missing name"), 400
    else:
        new_state = State()
        new_state.name = data["name"]
        storage.new(new_state)
        storage.save
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ Updates a state """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Not a JSON"}), 400

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    not_for_change = ["id", "created_at", "updated_at"]
    for key, value in json_data.items():
        if key not in not_for_change:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
