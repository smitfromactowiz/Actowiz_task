import mysql.connector

def connction():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="tometo"
    )

    cur =conn.cursor()
    return conn,cur

def create_db():
    conn,cur = connction()
    cur.execute('''
    create table if not exists movies(
                m_id int auto_increment primary key,
                movie_name varchar(255),
                score varchar(255),
                description text,
                img text,
                reviews_count int,
                videos json,
                want_to_know text,
                cast_and_crew json,
                all_reviews json
                )
    ''')
    conn.commit()
    conn.close()


