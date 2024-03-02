from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
import os
import requests
from math import radians, sin, cos, sqrt, atan2
from mysql.connector import connect, Error
from collections import OrderedDict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fre:password@my_sql:3306/pieno'
db = SQLAlchemy(app)

def get_all_distributors():
    api_url = "http://api_distributori:8080/api_distributori/get_distributori"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        distributori = data.get('distributori', [])
        return distributori
    else:
        # Gestisci eventuali errori nella risposta dell'API
        print(f"Errore nella richiesta API: {response.status_code}")
        return None
    
def haversine(lat1, lon1, lat2, lon2):
    url = f"{os.environ['OSRM_SERVER']}/{lon1},{lat1};{lon2},{lat2}"
    res = requests.get(url).json()
    distance = round(res['routes'][0]['distance']/1000, 3)
    return distance

def trova_id_nel_raggio(lat_tua, lon_tua, distributori, raggio_max):
    id_nel_raggio = []

    #df = pd.read_csv(csv_file_path)
    for d in distributori:
        lat_distributore = float(d['latitudine'])
        lon_distributore = float(d['longitudine'])

        distanza = haversine(lat_tua, lon_tua, lat_distributore, lon_distributore)
    
        if distanza <= raggio_max:
            id_nel_raggio.append((int(d['id']), distanza))

    return id_nel_raggio

def dati_finali(list_id, distributori):
    #csv_id = pd.read_csv(csv)
    list_id = sorted(list_id, key=lambda x: x[1])
    final_list = {}
    for id, distanza in list_id:
        for d in distributori:
            if d['id'] == id:
                #istanza = csv_id[csv_id['id'] == id]
                id_istanza = d['id']
                prezzo_benzina = d['prezzo_benzina']
                prezzo_diesel = d['prezzo_diesel']
                km_distanza = distanza
                indirizzo = d['indirizzo']
                elem = [prezzo_benzina, prezzo_diesel, km_distanza, indirizzo]
                final_list[id_istanza] = elem
    
    return final_list

def top_score(elements): 
    top_elem = {}
    for key in elements:
        prodotto = elements[key][0] * elements[key][2]
        top_elem[key] = prodotto
        
    return top_elem

def compute_cost(data, tank, consumption_per_km): 
    final_score = {}
    for key, value in data.items(): 
        final_score[key] = total_costs(tank, consumption_per_km, tank, value[2], value[0])

    final_score = OrderedDict(sorted(final_score.items(), key=lambda item: item[1]))
    return final_score

        
def travel_cost(distance:float, consumo:float, price_per_lt:float) -> float:
    return distance * consumo * price_per_lt



def fill_up_cost(tank_to_fill:float, price_per_lt:float, tank:int) -> float:
    return tank_to_fill * tank * price_per_lt



def total_costs(tank:int, consumption_per_km:float, tank_to_fill:int, distance:float, price_per_lt: float) -> float:
    return round(fill_up_cost(((100 - tank_to_fill))/100, price_per_lt, tank) + travel_cost(distance, consumption_per_km, price_per_lt), 3)

def save_data(final_score): 
    try:
        with connect(
            host="my_sql",
            user="fre", 
            password="password", 
            database="pieno",
            autocommit=True  
        ) as connection:
            with connection.cursor() as cursor:
                #IMPORTANTE, CONTROLLA COSA CONTIENE FINAL SCORE PRIMA
                print(final_score)
                min_key, min_value = min(final_score.items(), key=lambda item: item[1])
                #query dovrebbe essere ok
                query = """INSERT INTO top_distributori (id, data)
                    VALUES (%s, UTC_TIMESTAMP())
                    ON DUPLICATE KEY UPDATE
                    data = VALUES(data)
                    """
                values = (
                    min_key,
                )
                cursor.execute(query, values)
                print("Inserimento dei TOP ok")

    except Error as e:
        # Handle specific MySQL server has gone away error
        if "MySQL server has gone away" in str(e):
            # Reconnect and retry the operation
            save_data(final_score)
        else:
            print(f"Error: {e}")

@app.route('/api_obtain_data/get_data', methods=['GET'])
def get_data():
    # Ottenere i dati dalla richiesta GET
    lat = request.args.get('latitudine')
    long = request.args.get('longitudine')
    tank = int(request.args.get('serbatoio'))
    consumption_per_km = float(request.args.get('consumo_per_km'))
    raggio_max = 10
    
    distributori_modena = get_all_distributors()
    id_raggio = trova_id_nel_raggio(lat, long, distributori_modena, raggio_max)
    res = dati_finali(id_raggio, distributori_modena)
    final_score = compute_cost(res, tank, consumption_per_km)
    print(final_score)
    final_score = dict(sorted(final_score.items(), key=lambda item: item[1]))
    min_key, min_value = min(final_score.items(), key=lambda item: item[1])
    #print(min_elem)
    save_data(final_score)
    for d in distributori_modena: 
        if int(d['id']) == int(min_key):
            return jsonify(d)
    #print(final_score[0])
    #return jsonify(min_elem)

app.run(host='0.0.0.0', port=8080, debug=True)

