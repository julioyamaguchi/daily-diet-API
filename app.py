from flask import Flask, request, jsonify
from database import db

from flask_login import LoginManager

from model.user import User
from model.refeicao import Refeicao

from routers.refeicao_ws import refeicao_ws
from routers.user_ws import user_ws

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secre_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@127.0.0.1:3306/diet_api'

login_manager = LoginManager() #classe responsavel por gerenciamento de usuario

#passando app para o banco
db.init_app(app)

#conectando biblioteca de login
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#separação de rotas
app.register_blueprint(refeicao_ws)
app.register_blueprint(user_ws)


if __name__ == '__main__':
    app.run(debug=True)
