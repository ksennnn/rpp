import os
from datetime import datetime
from flask import Flask, request
from models import db, Visit

app = Flask(__name__)

#Сборка строки подключения из переменных окружения
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_HOST = os.environ["POSTGRES_HOST"]
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
DB_NAME = os.environ["POSTGRES_DB"]

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#Создание таблиц при старте приложения
with app.app_context():
    db.create_all()


@app.route("/hello", methods=["GET"])
def hello():
    # 1. Текущее время
    now = datetime.utcnow()

    # 2. IP-адрес клиента
    if request.headers.get("X-Forwarded-For"):
        ip = request.headers["X-Forwarded-For"].split(",")[0].strip()
    else:
        ip = request.remote_addr

    # 3. Сохраняем запись
    visit = Visit(visit_time=now, ip_address=ip)
    db.session.add(visit)
    db.session.commit()

    # 4. Отвечаем 200 OK с телом "Hello"
    return "Hello", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)