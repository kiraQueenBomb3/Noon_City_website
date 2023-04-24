from flask import Flask, url_for, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from registerform import RegisterForm
from loginform import LoginForm
import sqlite3
from data import db_session
from data.users import User
from data.news import NewsForm, News


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.content = form.content.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    param = {}
    param['title'] = 'Новости Noon City'
    param['news'] = db_sess.query(News)[::-1]
    if current_user.is_authenticated:
        pass
    else:
        pass  #  тут нужно убрать у зареганного ползователя кнопки войти и зарегаться, и заменить их на оставить запись
    return render_template('index.html', **param)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    from_where = {'Из крупного города': 3,
                  'Из Noon City': 4,
                  'Из небольшого поселения': 2,
                  'Мигрировал из бедной страны': 1}
    ambitions = {'Стать легендой Noon City': 4,
                 'Уничтожить корпорацию АраСакэ': 4,
                 'Навести порядок в городе, уменьшить преступность': 3,
                 'Разбогатеть': 1}
    parameter = {'Физическая сила': 4,
                 'Ловкость': 4,
                 'Интеллект': 3,
                 'Технические способности': 3,
                 'Харизма': 3}

    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        new_user = User(
            name=form.username.data,
            email=form.email.data,
            sex=form.sex.data,
            gun=form.favourite_gun.data
        )
        new_user.set_password(form.password.data)
        personal_points = from_where[form.from_where.data] + \
                          ambitions[form.ambitions.data] + parameter[form.parameters.data]

        if personal_points in [5, 6]:
            new_user.job = 'Безработный'
            new_user.reputation = 'Никто'
        elif personal_points == 12 and form.ambitions != 'Уничтожить корпорацию АраСакэ':
            new_user.job = 'Работник АраСакэ'
            new_user.reputation = 'Легенда Noon City'
        elif personal_points == 12:
            new_user.job = 'Террорист'
            new_user.reputation = 'Легенда Noon City'
        elif form.ambitions == 'Навести порядок в городе, уменьшить преступность':
            new_user.job = 'Полицейский'
            new_user.reputation = 'Известная личность'
        else:
            new_user.job = 'Наёмник'
            new_user.reputation = 'Известная личность'
        db_sess.add(new_user)
        db_sess.commit()

        return redirect('/login')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/profile/<int:id>')
def profile(id):
    db_sess = db_session.create_session()
    person = db_sess.query(User).filter(User.id == id).first()
    news = db_sess.query(News).filter(News.user_id == id)[::-1]
    param = {}
    param['news'] = news
    param['name'] = person.name
    param['sex'] = person.sex
    param['job'] = person.job
    param['reputation'] = person.reputation
    param['user_id'] = person.id
    if person:
        return render_template('profile.html', **param)
    else:
        abort(404)


@app.route('/single_new/<int:id>')
def single_new(id):
    db_sess = db_session.create_session()
    param = {}
    new = db_sess.query(News).filter(News.id == id).first()
    param['new'] = new
    if new:
        return render_template('single_new.html', **param)
    else:
        abort(404)


if __name__ == '__main__':
    db_session.global_init("db\\noon_town.db")
    app.run(port=8080, host='127.0.0.1')
