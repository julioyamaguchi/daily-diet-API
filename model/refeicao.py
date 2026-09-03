from sqlalchemy import ForeignKey
from database import db


class Refeicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100),nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    dentro_dieta = db.Column(db.Boolean, default=True)
    usuario = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        return{
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "data_hora": self.data_hora.isoformat(),
            "dentro_dieta": self.dentro_dieta,
            "usuario": self.usuario
        }