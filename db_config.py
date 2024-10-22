DB_HOST = "localhost"
DB_NAME = ""
DB_USER = ""
DB_PASSWORD = ""

def save_db_config(host, db_name, user, password):
    """Сохраняет настройки подключения к БД."""
    global DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
    DB_HOST = host
    DB_NAME = db_name
    DB_USER = user
    DB_PASSWORD = password