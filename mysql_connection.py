import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host = 'database-1.cnd2fqwu3b8i.ap-northeast-2.rds.amazonaws.com',
        database = 'movie_db',
        user = 'movie_user2',
        password = 'movie1234'
    )
    return connection