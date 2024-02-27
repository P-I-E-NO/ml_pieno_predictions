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
                               CREATE TABLE top_distributori(
                                id int not null primary key,
                                data DATE not null,
                                PRIMARY KEY (id, data)
                               )
                               """)
                               
                               
    except Error as e: 
        print(e)        