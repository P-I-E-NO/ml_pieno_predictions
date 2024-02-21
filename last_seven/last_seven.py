import pandas as pd
from mysql.connector import connect, Error

def insert_data_into_mysql(dataframe):
    try:
        with connect(
            host="my_sql",
            user="fre", 
            password="password", 
            database="pieno",
            autocommit=True  # Enable autocommit to avoid explicit commit statements
        ) as connection:
            with connection.cursor() as cursor:
                for index, row in dataframe.iterrows():
                    query = "INSERT INTO prezzi VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (
                        row['data'], row['prezzo'], row['giorno'],
                        row['mese'], row['trimestre'],
                        row['anno'], row['stagione'], row['SMA'],
                        row['deviazione_standard'], row['banda_superiore'],
                        row['banda_inferiore']
                    )
                    cursor.execute(query, values)

    except Error as e:
        # Handle specific MySQL server has gone away error
        if "MySQL server has gone away" in str(e):
            # Reconnect and retry the operation
            insert_data_into_mysql(dataframe)
        else:
            print(f"Error: {e}")

if __name__ == '__main__':
    df = pd.read_csv("merge.csv")
    insert_data_into_mysql(df)