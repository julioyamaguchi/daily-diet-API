from flask import Flask
from database import db
from model.refeicao import Refeicao

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@127.0.0.1:3306/diet_api'

db.init_app(app)

@app.route("/")
def hello_world():
    return "<p>Hello World</p>"

if __name__ == '__main__':
    app.run(debug=True)
