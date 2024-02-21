from mysql.connector import connect, Error



if __name__ == '__main__':
    try:
        with connect(
            host="my_sql",
            user="fre", 
            password="password", 
            database="pieno"
        ) as connection:
            with connection.cursor() as cursor: 
                cursor.execute("""
                               CREATE TABLE prezzi(data DATE not null primary key,
                               prezzo double not null,
                               giorno int not null,
                               mese int not null,
                               trimestre int not null,
                               anno int not null,
                               stagione int not null,
                               SMA float not null,
                               deviazione_standard float not null,
                               banda_superiore float not null,
                               banda_inferiore float not null
                               )
                               """)
                               
                               
    except Error as e: 
        print(e)        