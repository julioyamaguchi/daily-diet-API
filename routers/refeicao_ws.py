from flask_login import current_user, login_required

from database import db
from model.refeicao import Refeicao
from datetime import datetime

from flask import Blueprint, jsonify, request

refeicao_ws = Blueprint('refeicao_ws', __name__)


@refeicao_ws.route("/refeicao", methods=["POST"])
@login_required
def create_refeicao():
    data = request.json

    new_refeicao = Refeicao(
        nome=data.get("nome"),
        descricao=data.get("descricao"),
        data_hora = datetime.fromisoformat(data.get("data_hora")),
        dentro_dieta = data.get("dentro_dieta"),
        usuario = current_user.id
        )
    
    db.session.add(new_refeicao)
    db.session.commit()
    return jsonify({"mensagem": "Refeicao cadastrada com sucesso"})


@refeicao_ws.route("/refeicao/<int:id>", methods=["PUT"])
@login_required
def update_refeicao(id):
    data = request.json
    refeicao = Refeicao.query.get(id)

    if refeicao == None:
        return jsonify({"mensagem": "Não foi possivel encontrar a refeicao"}), 404

    if refeicao.usuario != current_user.id:
        return jsonify({"mensagem": "Não foi possivel atualizar essa refeicao"}), 404

    if "nome" in data:
        refeicao.nome = data.get("nome")
    if "descricao" in data:
        refeicao.descricao = data.get("descricao")
    if "data_hora" in data:    
        refeicao.data_hora = datetime.fromisoformat(data.get("data_hora"))
    if "dentro_dieta" in data:    
        refeicao.dentro_dieta = data.get("dentro_dieta")
    db.session.commit()
    return jsonify({"mensagem": f"Refeicao {id} atualizada com sucesso"})


@refeicao_ws.route("/refeicao/<int:id>", methods=["DELETE"])
@login_required
def delete_refeicao(id):
    refeicao = Refeicao.query.get(id)

    if refeicao and refeicao.usuario == current_user.id:
        db.session.delete(refeicao)
        db.session.commit()
        return jsonify({"mensagem": f"Refeicao id={id} deletada com sucesso"})

    return jsonify({"message": "Refeição não encontrada"}), 404


@refeicao_ws.route("/refeicao", methods=["GET"])
@login_required
def read_refeicoes():
    refeicoes = Refeicao.query.filter(Refeicao.usuario== current_user.id).order_by(Refeicao.data_hora.desc()).all()

    refeicoes_dict = []
    for refeicao in refeicoes:
        refeicoes_dict.append(refeicao.to_dict())

    return jsonify({
        "message": "Sucesso, retornando todas as refeições do usuário",
        "refeicoes": refeicoes_dict})    

@refeicao_ws.route("/refeicao/<int:id_refeicao>", methods=["GET"])
@login_required
def read_refeicao(id_refeicao):
    refeicao = Refeicao.query.filter_by(
        id=id_refeicao,
        usuario=current_user.id
    ).first()

    if refeicao:
        return jsonify({
        "message": "Sucesso, retornando a refeição do usuário",
        "refeicoes": refeicao.to_dict()
    })

    return jsonify({"message": "Refeição não encontrada"}), 404    
    


