from flask_login import current_user, login_required, login_user, logout_user

import bcrypt

from database import db
from model.user import User
from flask import Blueprint, jsonify, request

user_ws = Blueprint('user_ws', __name__)

@user_ws.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        #login
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user) # faz o login do user no sistema
            print(current_user.is_authenticated)
            return jsonify({"messagem": "Auntenticação realizada com sucesso"})
    
    return jsonify({"messagem": "Credenciais inválidas"}), 400

@user_ws.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"messagem": "Logout realizado com sucesso!"})


@user_ws.route('/user', methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "usuario cadastrado com sucesso"})

    return jsonify({"message": "Dados inválidos"}), 400


@user_ws.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return jsonify({"username": user.username})

    return jsonify({"message": "Usuário não encontrado"}), 404


@user_ws.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user) 

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"messagem": "Operação não permitida"}), 403
    if user and data.get("password"):
        user.password = bcrypt.hashpw(str.encode(data.get("password")), bcrypt.gensalt())
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso"})

    return jsonify({"message": "Usuário não encontrado"}), 404

@user_ws.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    
    user = User.query.get(id_user) 

    if current_user.role != 'admin':
        return jsonify({"message": "Operação não permitida"}), 403
    if  id_user == current_user.id:
        return jsonify({"message": "Deleção não permitida"}), 403

    if user: 
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso"})

    return jsonify({"message": "Usuário não encontrado"}), 404


