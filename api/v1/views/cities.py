#!/usr/bin/python3
""" Cities view """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("states/<state_id>/cities", methods=["GET"])
def list_cities_by_state(state_id):
    """ Lists Cities by state """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def list_city(city_id):
    """ Lists a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """ Deletes a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a city """
    data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not data:
        return jsonify("Not a JSON"), 400
    elif "name" not in data:
        return jsonify("Missing name"), 400
    else:
        new_city = City()
        new_city.name = data["name"]
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()
        return jsonify(new_City.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """ Updates a city """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    city = storage.get(City, city_id)
    if not city or not city_id:
        abort(404)

    not_for_change = ["id", "created_at", "updated_at", "state_id"]
    for key, value in data.items():
        if key not in not_for_change:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
