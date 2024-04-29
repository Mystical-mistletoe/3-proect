import datetime
import json

from flask import Flask, url_for
from flask import render_template, redirect, make_response, request, session
from data import db_session
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm
from forms.login_form import LoginForm
from forms.news import NewsForm
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

from flask_wtf import FlaskForm

from data import db_session, jobs_api
from flask import jsonify, make_response

''''''
#


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

#Затем сразу после создания приложения flask инициализируем LoginManager:

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)





@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)



def main():

    db_session.global_init("db/blogs.db")
    app.run(debug=True)

''''''
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)

@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Jobs()

        news.namep = form.namep.data
        news.size = form.size.data
        news.boost = form.boost.data
        news.biograph = form.biograph.data
        news.is_finished = form.is_finished.data

        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление анкета',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter(
            Jobs.id == id,
            Jobs.user == current_user).first()
        if news:
            #form.job.data = news.job
            news.team_lead.data = form.team_lead

            form.namep.data = news.namep
            form.size.data = news.size
            form.boost.data = news.boost
            form.biograph.data = news.biograph

            form.is_finished = news.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if news:
            #news.job = form.job.data

            news.namep = form.namep.data
            news.size = form.size.data
            news.boost = form.boost.data
            news.biograph = form.biograph.data

            news.is_finished = form.is_finished.data

            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование anketi',
                           form=form)

@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id).first()

    if news:
        if news.user.id == current_user.id or current_user.id == 1:
            db_sess.delete(news)
            db_sess.commit()
        else:
            abort(404)
    else:
        abort(404)
    return redirect('/')






if __name__ == '__main__':
    main()











