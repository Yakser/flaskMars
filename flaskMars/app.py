from datetime import datetime

from flask import Flask, render_template, redirect

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = {i.id: i.name + ' ' + i.surname for i in db_sess.query(User).all()}

    return render_template("index.html", jobs=jobs, users=users)


def main():
    db_session.global_init("db/mars.db")
    app.run()


if __name__ == '__main__':
    main()
