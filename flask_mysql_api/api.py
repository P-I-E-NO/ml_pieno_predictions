from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fre:password@my_sql:3306/pieno'
db = SQLAlchemy(app)

# Definisci i modelli delle tabelle del database
class Prezzi(db.Model):
    __tablename__ = 'prezzi'
    data = db.Column(db.Date, primary_key=True)
    prezzo = db.Column(db.Float, nullable=False)
    giorno = db.Column(db.Integer, nullable=False)
    mese = db.Column(db.Integer, nullable=False)
    trimestre = db.Column(db.Integer, nullable=False)
    anno = db.Column(db.Integer, nullable=False)
    stagione = db.Column(db.Integer, nullable=False)
    SMA = db.Column(db.Float, nullable=False)
    deviazione_standard = db.Column(db.Float, nullable=False)
    banda_superiore = db.Column(db.Float, nullable=False)
    banda_inferiore = db.Column(db.Float, nullable=False)

class Predizioni(db.Model):
    __tablename__ = 'predizioni'
    data = db.Column(db.Date, primary_key=True)
    pred = db.Column(db.Integer, nullable=False)

@app.get('/api/get_prezzi')
def get_prezzi():
    prezzi = Prezzi.query.order_by(Prezzi.data.desc()).limit(7).all()
    prezzi_list = [{'data': item.data, 'prezzo': item.prezzo}
                   for item in prezzi]
    return jsonify({'prezzi': prezzi_list})

@app.get('/api/get_predizioni')
def get_predizioni():
    predizioni = Predizioni.query.order_by(Predizioni.data.desc()).limit(7).all()
    predizioni_list = [{'data': predizione.data, 'pred': predizione.pred}
                       for predizione in predizioni]
    return jsonify({'predizioni': predizioni_list})

app.run(host='0.0.0.0', port=8080, debug=True)