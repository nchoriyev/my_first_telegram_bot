import psycopg2 as psql


class Database:
    @staticmethod
    async def connect(query, query_type):
        db = psql.connect(
            database="bot_1",
            user='postgres',
            password='Aa9022560',
            host='localhost',
            port='5432'
        )

        cursor = db.cursor()
        cursor.execute(query)
        data = ['insert', 'delete']
        if query_type in data:
            db.commit()
            if query_type == 'insert':
                return "muvaffaqtiyatli qo'shildi"
        else:
            return cursor.fetchall()

    @staticmethod
    async def check_user_id(user_id: int):
        query = f"SELECT * FROM users_1 WHERE user_id = {user_id}"
        check_user = await Database.connect(query, query_type='select')
        if len(check_user) == 1:
            print("->", check_user)
            return True
        return False
