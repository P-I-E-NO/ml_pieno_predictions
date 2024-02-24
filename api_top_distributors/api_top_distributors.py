from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fre:password@my_sql:3306/pieno'
db = SQLAlchemy(app)

class Top_Distributori(db.Model):
    __tablename__ = 'top_distributori'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)


@app.get('/api_top_distributors/get_top_distributors')
def get_top():
    top_distributori = Top_Distributori.query.all()
    top_distributori_list = [{'id': item.id, 'data': item.data} for item in top_distributori]
    return jsonify({'distributori': top_distributori_list})


app.run(host='0.0.0.0', port=8080, debug=True)