import json

from flask import Flask, request, render_template
import time
from datetime import datetime


app = Flask(__name__)


@app.route("/")
def index_page():
    return "HELLO"

db_file = "./data/db.json"
json_db = open(db_file, "rb")
data = json.load(json_db)
db = data["messages"]

def saveMessages():
    data = {
        "messages": db
    }
    json_db = open(db_file, "w")
    json.dump(data, json_db)


@app.route("/form")
def form():
    return render_template("form.html")


# POST - как правило означает изменение данных
# GET - запрос, который ничего не меняет

@app.route("/sendMessage")
def chat():
    name = request.args["name"]
    text = request.args["text"]

    name_len = len(name)  # длина имени
    text_len = len(text)  # длина текста

    if name_len > 100 or name_len < 3:
        return "ERROR"  # Невалидный запрос

    if text_len < 1 or text_len > 3000:
        return "ERROR"

    message = {
        "name": name,
        "text": text,
        "time": time.time()  # таймстемп
    }
    db.append(message)
    saveMessages()   # Добавляем новое сообщение в список
    return "OK"


@app.route("/messages")
def get_messages():
    after_timestamp = float(request.args["after_timestamp"])
    result = []  # Все сообщения, отправленные после after_timestamp
    for message in db:
        if message["time"] > after_timestamp:
            result.append(message)

    return {"messages": result}

@app.route('/status')
def status():
    server_version = "1234"
    name_author = "master Yoda"
    time_server = datetime.now()  # Получаем текущее время
    all_messages = len(db)  # Количество записей в db

    return f'{name_author}, версия: {server_version} <br> Время: {time_server.strftime("%d-%m-%Y %H:%M")} <br> Всего сообщений: {all_messages}'

@app.route('/admin_delete_everything')
def del_post():
    password = 1234
    del_password = int(request.args["delete"]) # Пароль передается в качестве параметра: http://127.0.0.1:5000/admin_delete_everything?delete=1234
    if del_password == password:
        db.clear()
        saveMessages()
        return 'Удалены все сообщения'
    else:
        return 'Неверный пароль'


app.run()
