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
                               CREATE TABLE distributori(
                                id int not null primary key,
                                indirizzo text not null,
                                latitudine float not null,
                                longitudine float not null,
                                prezzo_benzina float not null,
                                prezzo_diesel float not null
                               )
                               """)
                               
                               
    except Error as e: 
        print(e)        