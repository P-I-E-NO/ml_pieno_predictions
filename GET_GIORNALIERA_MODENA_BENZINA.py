import os
from mysql.connector import connect, Error
import requests
import pandas as pd
import datetime


def obtain_daily_data_():
    url = "https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv"
    response = requests.get(url)
    data = response.content.decode('utf-8')

    data = data.split("\n")
    data.pop(0)
    data.pop(0)

    data = [row.split(';') for row in data]

    df = pd.DataFrame(data, columns=["id_impianto", "tipo_carburante", "prezzo", "is_self", "data_ora"])
    df["data"] = df["data_ora"].str.split(" ").str.get(0)
    df["ora"] = df["data_ora"].str.split(" ").str.get(1)
    df.drop('data_ora', axis=1, inplace=True)

    df = df.iloc[:-1]
    return df


def obtain_id_modena():
    url_imp = "https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv"
    response_imp = requests.get(url_imp)

    data_imp = response_imp.content.decode('utf-8')

    data_imp = data_imp.split("\n")
    data_imp.pop(0)
    data_imp.pop(0)

    data_imp = [row.split(';', 9) for row in data_imp]

    df_imp = pd.DataFrame(data_imp,
                          columns=["id", "gestore", "bandiera", "tipo", "nome", "indirizzo", "comune", "provincia",
                                   "latitudine", "longitudine"])

    df_imp = df_imp.iloc[:-1]
    df_imp = df_imp[df_imp['provincia'] == 'MO']
    df_imp_list = list(df_imp['id'])
    return df_imp_list


def preprocess_data(df, id_modena):
    df = df[df['id_impianto'].isin(id_modena)]
    if os.environ['FUEL'] == 'Benzina':
        df = df[df['tipo_carburante'] == 'Benzina']
    else:
        df = df[df['tipo_carburante'] == 'Gasolio']

    df = df[df['is_self'] == '1']
    df = df.drop(['ora', 'is_self', 'tipo_carburante'], axis=1)
    df = df.sort_values(by='data')
    df['prezzo'] = pd.to_numeric(df['prezzo'], errors='coerce')
    df = df.drop_duplicates(subset=['id_impianto', 'data'])
    df['data'] = pd.to_datetime(df['data'], format='mixed', dayfirst=True)
    df['data'].dt.strftime('%y-%m-%d')
    df_media_giornaliera = df.groupby('data')['prezzo'].mean()
    df = df_media_giornaliera.to_frame()
    df = df.reset_index()
    df['giorno'] = df['data'].dt.dayofweek + 1
    df['mese'] = df['data'].dt.month
    df['trimestre'] = df['data'].dt.quarter
    df['anno'] = df['data'].dt.year
    df['date_offset'] = (df['data'].dt.month * 100 + df['data'].dt.day - 320) % 1300
    df['stagione'] = pd.cut(df['date_offset'], [0, 300, 602, 900, 1300],
                            labels=['0', '1', '2', '3'])
    df = df.drop('date_offset', axis=1)
    periodo_sma = 7
    df['SMA'] = df['prezzo'].rolling(window=periodo_sma).mean()
    df['deviazione_standard'] = df['prezzo'].rolling(window=periodo_sma).std()
    df['banda_superiore'] = df['SMA'] + 0.7 * df['deviazione_standard']
    df['banda_inferiore'] = df['SMA'] - 0.7 * df['deviazione_standard']
    df = df.dropna()
    #df = df.set_index('data')
    return df


def rinomina_file(n, percorso_file):
    try:
        nome_file = os.path.basename(percorso_file)
        nuovo_nome = nome_file[:-n]
        os.rename(percorso_file, nuovo_nome + '.csv')
        #print(f"File rinominato con successo in {nuovo_nome}")
    except FileNotFoundError:
        print("Il file specificato non esiste.")
    except Exception as e:
        print(f"Si è verificato un errore durante la rinomina: {e}")


def create_csv(df):
    #timestamp = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
    #nome_file = f"Prezzi_{timestamp}.csv"
    #df.to_csv(nome_file, index=False)
    #percorso_file = os.path.abspath(nome_file)
    #rinomina_file(13, percorso_file)
    try:
        with connect(
            host="my_sql",
            user="fre", 
            password="password", 
            database="pieno",
            autocommit=True  
        ) as connection:
            with connection.cursor() as cursor:
                for index, row in df.iterrows():
                    query = """INSERT INTO prezzi (data, prezzo, giorno, mese, trimestre, anno, stagione, SMA, deviazione_standard, banda_superiore, banda_inferiore)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    prezzo = VALUES(prezzo), giorno = VALUES(giorno), mese = VALUES(mese), trimestre = VALUES(trimestre),
                    anno = VALUES(anno), stagione = VALUES(stagione), SMA = VALUES(SMA),
                    deviazione_standard = VALUES(deviazione_standard), banda_superiore = VALUES(banda_superiore),
                    banda_inferiore = VALUES(banda_inferiore)
                    """
                    values = (
                        row['data'], row['prezzo'], row['giorno'],
                        row['mese'], row['trimestre'],
                        row['anno'], row['stagione'], row['SMA'],
                        row['deviazione_standard'], row['banda_superiore'],
                        row['banda_inferiore']
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
    df = obtain_daily_data_()
    id_modena = obtain_id_modena()
    df = preprocess_data(df, id_modena)
    create_csv(df)