import psycopg2
import db_config

conn = None
cur = None

def connect_to_db():
    """Подключается к базе данных."""
    global conn, cur
    try:
        conn = psycopg2.connect(
            host=db_config.DB_HOST,
            database=db_config.DB_NAME,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD
        )
        cur = conn.cursor()
        return True
    except Exception as e:
        print(f"Не удалось подключиться к БД: {e}")
        return False

def close_connection():
    """Закрывает соединение с базой данных."""
    global conn, cur
    if conn:
        cur.close()
        conn.close()
        conn = None
        cur = None

def get_tables():
    """Получает список таблиц из базы данных."""
    try:
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        return [table[0] for table in cur.fetchall()]
    except Exception as e:
        print(f"Ошибка при получении списка таблиц: {e}")
        return []

def create_table(table_name, primary_key, fields):
    """Создает новую таблицу."""
    try:
        sql = f"CREATE TABLE {table_name} ("
        for i, field in enumerate(fields):
            sql += f"{field[0]} {field[1]}"
            if i < len(fields) - 1:
                sql += ", "
        if primary_key:
            sql += f", PRIMARY KEY ({primary_key})"
        sql += ");"
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")

def delete_table(table_name):
    """Удаляет таблицу."""
    try:
        cur.execute(f"DROP TABLE {table_name}")
        conn.commit()
    except Exception as e:
        print(f"Ошибка при удалении таблицы: {e}")

def edit_table(table_name, primary_key, fields):
    """Изменяет существующую таблицу."""
    try:
        sql = f"ALTER TABLE {table_name} RENAME TO temp_{table_name};\n"
        sql += f"CREATE TABLE {table_name} ("
        for i, field in enumerate(fields):
            sql += f"{field[0]} {field[1]}"
            if i < len(fields) - 1:
                sql += ", "
        if primary_key:
            sql += f", PRIMARY KEY ({primary_key})"
        sql += ");\n"
        sql += f"INSERT INTO {table_name} SELECT * FROM temp_{table_name};\n"
        sql += f"DROP TABLE temp_{table_name};"
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(f"Ошибка при редактировании таблицы: {e}")