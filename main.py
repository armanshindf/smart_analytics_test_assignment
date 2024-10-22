
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import db_manager
import db_config
import psycopg2


# Создание главного окна
root = tk.Tk()
root.title("Редактор таблиц")

# Фрейм для списка таблиц
table_frame = tk.Frame(root)
table_frame.pack(side="left", fill="both", expand=True)

# Фрейм для действий над таблицами
action_frame = tk.Frame(root)
action_frame.pack(side="right", fill="both", expand=True)

# Список таблиц
table_list = tk.Listbox(table_frame)
table_list.pack(fill="both", expand=True)

# Кнопки для действий над таблицами
create_button = tk.Button(action_frame, text="Создать таблицу", command=lambda: create_table_window())
create_button.pack(pady=10)
delete_button = tk.Button(action_frame, text="Удалить таблицу", command=lambda: delete_table())
delete_button.pack(pady=10)
edit_button = tk.Button(action_frame, text="Изменить таблицу", command=lambda: edit_table_window())
edit_button.pack(pady=10)

# Функция обновления списка таблиц
def update_table_list():
    try:
        table_list.delete(0, tk.END)
        tables = db_manager.get_tables()
        for table in tables:
            table_list.insert(tk.END, table)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при получении списка таблиц: {e}")

# Функция создания окна для создания таблицы
def create_table_window():
    def create_table():
        try:
            table_name = table_name_entry.get()
            primary_key = primary_key_entry.get()
            fields = []
            for i in range(len(field_names)):
                field_name = field_names[i].get()
                field_type = field_types[i].get()
                fields.append((field_name, field_type))
            
            db_manager.create_table(table_name, primary_key, fields)
            update_table_list()
            create_table_window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при создании таблицы: {e}")


    create_table_window = tk.Toplevel(root)
    create_table_window.title("Создание таблицы")


    table_name_label = tk.Label(create_table_window, text="Имя таблицы:")
    table_name_label.grid(row=0, column=0, padx=5, pady=5)
    table_name_entry = tk.Entry(create_table_window)
    table_name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Ввод первичного ключа
    primary_key_label = tk.Label(create_table_window, text="Первичный ключ:")
    primary_key_label.grid(row=1, column=0, padx=5, pady=5)
    primary_key_entry = tk.Entry(create_table_window)
    primary_key_entry.grid(row=1, column=1, padx=5, pady=5)

    # Список полей
    field_frame = tk.Frame(create_table_window)
    field_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    field_names = []
    field_types = []
    for i in range(3):  # Начальное количество полей
        # Ввод имени поля
        field_name_label = tk.Label(field_frame, text=f"Поле {i + 1}:")
        field_name_label.grid(row=i, column=0, padx=5, pady=5)
        field_name_entry = tk.Entry(field_frame)
        field_name_entry.grid(row=i, column=1, padx=5, pady=5)
        field_names.append(field_name_entry)

        # Выбор типа поля
        field_type_label = tk.Label(field_frame, text="Тип:")
        field_type_label.grid(row=i, column=2, padx=5, pady=5)
        field_type_var = tk.StringVar(field_frame)
        field_type_var.set("INTEGER")  # Начальное значение
        field_type_combobox = ttk.Combobox(field_frame, textvariable=field_type_var, values=["INTEGER", "REAL", "TEXT", "TIMESTAMP"])
        field_type_combobox.grid(row=i, column=3, padx=5, pady=5)
        field_types.append(field_type_var)


    create_button = tk.Button(create_table_window, text="Создать", command=create_table)
    create_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Функция удаления таблицы
def delete_table():
    try:
        selected_table = table_list.get(tk.ANCHOR)
        if selected_table:
            if messagebox.askyesno("Подтверждение удаления", f"Вы уверены, что хотите удалить таблицу {selected_table}?"):
                db_manager.delete_table(selected_table)
                update_table_list()
        else:
            messagebox.showwarning("Предупреждение", "Выберите таблицу для удаления.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при удалении таблицы: {e}")

# Функция создания окна для редактирования таблицы
def edit_table_window():
    def edit_table():
        try:
            table_name = table_name_entry.get()
            primary_key = primary_key_entry.get()
            fields = []
            for i in range(len(field_names)):
                field_name = field_names[i].get()
                field_type = field_types[i].get()
                fields.append((field_name, field_type))

            db_manager.edit_table(table_name, primary_key, fields)
            update_table_list()
            edit_table_window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при редактировании таблицы: {e}")

    # Создание окна
    edit_table_window = tk.Toplevel(root)
    edit_table_window.title("Изменение таблицы")

    # Получение информации о выбранной таблице
    selected_table = table_list.get(tk.ANCHOR)
    if selected_table:
        conn = psycopg2.connect(
            host=db_config.DB_HOST,
            database=db_config.DB_NAME,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {selected_table}")
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchone()

        # Ввод имени таблицы
        table_name_label = tk.Label(edit_table_window, text="Имя таблицы:")
        table_name_label.grid(row=0, column=0, padx=5, pady=5)
        table_name_entry = tk.Entry(edit_table_window)
        table_name_entry.insert(0, selected_table)
        table_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Ввод первичного ключа
        primary_key_label = tk.Label(edit_table_window, text="Первичный ключ:")
        primary_key_label.grid(row=1, column=0, padx=5, pady=5)
        primary_key_entry = tk.Entry(edit_table_window)
        primary_key_entry.insert(0, "id" if "id" in columns else "")
        primary_key_entry.grid(row=1, column=1, padx=5, pady=5)

        # Список полей
        field_frame = tk.Frame(edit_table_window)
        field_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        field_names = []
        field_types = []
        for i, column in enumerate(columns):
            # Ввод имени поля
            field_name_label = tk.Label(field_frame, text=f"Поле {i + 1}:")
            field_name_label.grid(row=i, column=0, padx=5, pady=5)
            field_name_entry = tk.Entry(field_frame)
            field_name_entry.insert(0, column)
            field_name_entry.grid(row=i, column=1, padx=5, pady=5)
            field_names.append(field_name_entry)

            # Выбор типа поля
            field_type_label = tk.Label(field_frame, text="Тип:")
            field_type_label.grid(row=i, column=2, padx=5, pady=5)
            field_type_var = tk.StringVar(field_frame)
            field_type_var.set("INTEGER" if isinstance(data[i], int) else "REAL" if isinstance(data[i], float) else "TEXT" if isinstance(data[i], str) else "TIMESTAMP")
            field_type_combobox = ttk.Combobox(field_frame, textvariable=field_type_var, values=["INTEGER", "REAL", "TEXT", "TIMESTAMP"])
            field_type_combobox.grid(row=i, column=3, padx=5, pady=5)
            field_types.append(field_type_var)

        # Кнопка "Изменить"
        edit_button = tk.Button(edit_table_window, text="Изменить", command=edit_table)
        edit_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    else:
        messagebox.showwarning("Предупреждение", "Выберите таблицу для редактирования.")

# Функция открытия формы настройки подключения
def open_db_config_window():
    def save_config():
        host = host_entry.get()
        db_name = db_name_entry.get()
        user = user_entry.get()
        password = password_entry.get()
        db_config.save_db_config(host, db_name, user, password)
        config_window.destroy()
        connect_and_update()

    config_window = tk.Toplevel(root)
    config_window.title("Настройка подключения")

    host_label = tk.Label(config_window, text="Хост:")
    host_label.grid(row=0, column=0, padx=5, pady=5)
    host_entry = tk.Entry(config_window)
    host_entry.insert(0, db_config.DB_HOST)
    host_entry.grid(row=0, column=1, padx=5, pady=5)

    db_name_label = tk.Label(config_window, text="Имя базы данных:")
    db_name_label.grid(row=1, column=0, padx=5, pady=5)
    db_name_entry = tk.Entry(config_window)
    db_name_entry.grid(row=1, column=1, padx=5, pady=5)

    user_label = tk.Label(config_window, text="Пользователь:")
    user_label.grid(row=2, column=0, padx=5, pady=5)
    user_entry = tk.Entry(config_window)
    user_entry.grid(row=2, column=1, padx=5, pady=5)

    password_label = tk.Label(config_window, text="Пароль:")
    password_label.grid(row=3, column=0, padx=5, pady=5)
    password_entry = tk.Entry(config_window, show="*")
    password_entry.grid(row=3, column=1, padx=5, pady=5)

    save_button = tk.Button(config_window, text="Сохранить", command=save_config)
    save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Функция подключения к БД и обновления списка таблиц
def connect_and_update():
    if db_manager.connect_to_db():
        update_table_list()
    else:
        messagebox.showerror("Ошибка", "Не удалось подключиться к БД.")

# Открытие формы настройки подключения при запуске
open_db_config_window()

root.mainloop()

# Закрытие соединения при завершении работы приложения
db_manager.close_connection()