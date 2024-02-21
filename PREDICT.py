import datetime
import os
import pandas as pd
import joblib
from mysql.connector import connect, Error
from sklearn.preprocessing import StandardScaler
import warnings
from datetime import datetime, timedelta

from GET_GIORNALIERA_MODENA_BENZINA import obtain_daily_data_, obtain_id_modena, preprocess_data, create_csv

warnings.filterwarnings("ignore")


def load_model():
    if os.environ['FUEL'] == 'Benzina':
        model = joblib.load("pesi_modello_benzina.joblib")
    else:
        model = joblib.load("pesi_modello_gasolio.joblib")

    return model


def get_test_data(path):
    test_data = pd.read_csv(path)

    return test_data


def operations(test_data):
    scaler = StandardScaler()
    test_data = test_data.set_index('data')
    date_column = test_data.index
    test_data = scaler.fit_transform(test_data)

    return test_data, date_column


def predict(model, test_data, date_column):
    preds = model.predict(test_data)
    preds = pd.Series(preds, index=date_column, name="predizioni")

    return preds


def misurazione_piu_recente():
    lista_file = os.listdir()
    file_prezzi = [file for file in lista_file if file.startswith("Prezzi_") and len(file) == len("Prezzi_YYYY-MM-DD.csv")]
    if not file_prezzi:
        print("Nessun file 'Prezzi' trovato nella directory corrente.")
        return None

    data_più_recente = max([datetime.datetime.strptime(file[7:-4], "%Y-%m-%d") for file in file_prezzi])
    nome_file_più_recente = f"Prezzi_{data_più_recente.strftime('%Y-%m-%d')}.csv"
    return nome_file_più_recente


def get_recent_data():
    try:
        with connect(
            host="my_sql",
            user="fre", 
            password="password", 
            database="pieno",
            autocommit=True  
        ) as connection:
            with connection.cursor() as cursor:
                # Calcolo della data di 7 giorni fa
                seven_days_ago = datetime.now() - timedelta(days=7)
                seven_days_ago_date = seven_days_ago.date()
                seven_days_ago_str = seven_days_ago_date.strftime('%Y-%m-%d')

                # Query per ottenere i dati degli ultimi 7 giorni
                query = """
                SELECT data, prezzo, giorno, mese, trimestre, anno, stagione, SMA, deviazione_standard, banda_superiore, banda_inferiore
                FROM prezzi
                WHERE data >= STR_TO_DATE(%s, '%Y-%m-%d')
                """
                cursor.execute(query, (seven_days_ago_str,))

                # Estrazione dei risultati
                results = cursor.fetchall()
                print(results)

                # Creazione di un DataFrame con i risultati
                columns = ['data', 'prezzo', 'giorno', 'mese', 'trimestre', 'anno', 'stagione', 'SMA',
                           'deviazione_standard', 'banda_superiore', 'banda_inferiore']
                df = pd.DataFrame(results, columns=columns)
                return df

    except Error as e:
        # Handle specific MySQL server has gone away error
        if "MySQL server has gone away" in str(e):
            # Reconnect and retry the operation
            create_csv(df)
        else:
            print(f"Error: {e}")
            
def push_predictions(preds): 
    try:
        with connect(
            host="my_sql",
            user="fre", 
            password="password", 
            database="pieno",
            autocommit=True  
        ) as connection:
            with connection.cursor() as cursor:
                for index, value in preds.items():
                    print(index)
                    print(value)
                    query = """INSERT INTO predizioni (data, pred)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE
                    pred = VALUES(pred)
                    """
                    values = (
                        index, value
                        )
                    cursor.execute(query, values)
                    print("Inserimento ok")

    except Error as e:
        # Handle specific MySQL server has gone away error
        if "MySQL server has gone away" in str(e):
            # Reconnect and retry the operation
            create_csv(df)
        else:
            print(f"Error: {e}")

if __name__ == '__main__':
    #OK TUTTI (ma da eseguire una volta al giorno)
    df = obtain_daily_data_()
    id_modena = obtain_id_modena()
    df = preprocess_data(df, id_modena)
    create_csv(df)
        #a questo punto la create_csv carica sul db le nuove istanze e aggiorna se trova già la data
    
        #OK
    model = load_model()
    
        #DOVREBBE ANDARE
    test_data = get_recent_data()
    print(test_data)
    print(type(test_data))
    
        #OK
    test_data, date_column = operations(test_data)
    preds = predict(model, test_data, date_column)
        #carico sul db le predizioni
    push_predictions(preds)
    print(preds)
    