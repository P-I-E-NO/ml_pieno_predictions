from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fre:password@my_sql:3306/pieno'
db = SQLAlchemy(app)

class Distributori(db.Model):
    __tablename__ = 'distributori'
    id = db.Column(db.Integer, primary_key=True)
    indirizzo = db.Column(db.String, nullable=False)
    latitudine = db.Column(db.Float, nullable=False)
    longitudine = db.Column(db.Float, nullable=False)
    prezzo_benzina = db.Column(db.Float, nullable=False)
    prezzo_diesel = db.Column(db.Float, nullable=False)


@app.get('/api_distributori/get_distributori')
def get_prezzi():
    distributori = Distributori.query.all()
    distributori_list = [{'id': item.id, 'indirizzo': item.indirizzo,
                          'latitudine': item.latitudine, 'longitudine': item.longitudine,
                          'prezzo_benzina': item.prezzo_benzina, 'prezzo_diesel': item.prezzo_diesel}
                   for item in distributori]
    return jsonify({'distributori': distributori_list})


app.run(host='0.0.0.0', port=8080, debug=True)