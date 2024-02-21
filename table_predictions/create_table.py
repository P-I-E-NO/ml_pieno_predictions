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
                               CREATE TABLE predizioni(data DATE not null primary key,
                               pred int not null
                               )
                               """)
                               
                               
    except Error as e: 
        print(e)        