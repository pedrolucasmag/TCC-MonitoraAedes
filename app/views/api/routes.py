import os
from flask import Blueprint, jsonify, request
from app.controllers.handleForms import FormOcorrencia, FormLogin
from app.controllers.handleUsers import authenticate_user
from app.controllers.handleOccurrences import add_occurrence, get_occurrences_data
from app.controllers.handleLocation import get_address_location, get_address_by_coordinates
from flask_login import login_user, login_required

municipio = os.getenv("MUNICIPIO")

api = Blueprint(
    'api', __name__,
    template_folder='templates',
    static_folder='static'
)

@api.route('/api/getReverseGeocode', methods=['GET'])
def reverseGeoCode():
    lat = request.args.get("lat")
    long = request.args.get("long")
    if lat and long:
        location = get_address_by_coordinates(lat, long)
        return jsonify(location), 200
    return jsonify({"error":"Parâmetros inválidos!"}), 400


@api.route('/api/getFormData', methods=["POST"])
def getFormData():
    form = FormOcorrencia()

    if form.validate_on_submit():
        location = get_address_location(form)

        if "error" in location:
            return jsonify({"data":location}), 400
        else:
            add_occurrence(form, location)
            return jsonify({"message":"Formulário enviado com sucesso!"})

    else:
         return jsonify(data=form.errors), 400
    

@api.route('/api/login', methods=["POST"])
def autenticarUsuario():
    form = FormLogin()
    if form.validate_on_submit():
        email = form.data["email"]
        password = form.data["password"]
        user = authenticate_user(email, password)

        if user:
            login_user(user)
            response = jsonify({"data":{"messsage":"Usuário autenticado com sucesso."}})
            return response
        
        return jsonify({"data":{"messsage":"Credenciais inválidas!"}}), 401

    else:
        return jsonify(data=form.errors), 400

@api.route("/api/occurrences", methods=["GET"])
@login_required
def get_occurrences():
    tipomanifest = request.args.get('tipomanifest')
    bairro = request.args.get('bairro')
    data = get_occurrences_data(tipomanifest, bairro)
    return data, 200