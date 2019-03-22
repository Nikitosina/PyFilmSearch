from flask import Flask
from flask import jsonify, redirect, render_template, session, request
from flask_restful import reqparse, abort, Api, Resource
from Forms import LoginForm, RegistrationForm, AddFilmForm
from db import UsersModel, FilmsModel

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'films-searcher'
USERS, FILMS = UsersModel(), FilmsModel()
# FILMS.make_table()
# USERS.make_table()
# USERS.insert('222', '333', 'admin')
# USERS.task()


def abort_if_films_not_found(id):
    if not FILMS.get(id):
        abort(404, message="Films {} not found".format(id))


def optimize_cards(data):
    if len(data) < 5:
        while len(data) != 5:
            data.append(('Пусто', '-', '...', '-', '0'))
        return [data]
    elif len(data) == 5:
        return [data]
    elif len(data) > 5:
        new = []
        a = []
        for i in range(len(data)):
            a.append(data[i])
            if (i + 1) % 5 == 0:
                new.append(a)
                a = []
        new.append(a)
        new[-1] = optimize_cards(new[-1])[0]
        data = new
    return data


class Films(Resource):
    def get(self, id):
        abort_if_films_not_found(id)
        film_info = FILMS.get(id)
        return render_template('film_page.html', title=film_info[1], film=film_info)

    def delete(self, id):
        abort_if_films_not_found(id)
        FILMS.delete(id)
        return jsonify({'success': 'OK'})

    def put(self, id):
        abort_if_films_not_found(id)
        # args = users_parser.parse_args()
        FILMS.replace(id, 'https://st.kp.yandex.net/images/film_iphone/iphone360_64187.jpg')
        return jsonify({'Not working': 'OK'})


class FilmsList(Resource):
    def get(self):
        return jsonify({'Films': FILMS.get_all()})

    def post(self):
        # args = users_parser.parse_args()
        # USERS.insert(args['username'], args['password'])
        return jsonify({'Not working': 'OK'})


api.add_resource(FilmsList, '/films')
# api.add_resource(Films, '/films/<int:id>', methods=['GET'])


@app.route('/')
@app.route('/index')
def home():
    new_films = optimize_cards(FILMS.get_all(order='date', limit=5))
    action_mov = optimize_cards(FILMS.get_all(order='genre', arg='боевик', limit=5))
    print(action_mov)
    if 'success' not in session:
        return render_template('index.html', title='Главная', new_films=new_films, action_mov=action_mov)
    s = [session['success']]
    session.pop('success', 0)
    return render_template('index.html', title='Главная', success=s, new_films=new_films, action_mov=action_mov)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        exists = USERS.exists(form.username.data)
        if exists[0]:
            if exists[1][2] == form.password.data:
                session['username'] = form.username.data
                session['user_id'] = exists[1][0]
                session['success'] = 'Успешно'
                return redirect('/')
            else:
                form.password.errors = ['Неверный пароль']
        else:
            form.username.errors = ['Пользователь не найден']
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        exists = USERS.exists(form.username.data)
        if exists[0]:
            form.username.errors = ['Пользователь с таким именем уже существует']
        else:
            if form.password.data == form.password_again.data:
                USERS.insert(form.username.data, form.password.data, 'user')
                exists = USERS.exists(form.username.data)
                session['username'] = form.username.data
                session['user_id'] = exists[1][0]
                session['success'] = 'Успешно'
                return redirect('/')
            else:
                form.password.errors = ['Пароли не совпадают']
    return render_template('registration.html', title='Авторизация', form=form)


@app.route('/account')
def account():
    user = USERS.get(session['user_id'])
    print(user)
    fav = optimize_cards(FILMS.get_all(id=user[4], limit='5'))
    print(fav)
    return render_template('account.html', title='Личный кабинет', user=user, fav=fav)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/films/add', methods=['POST', 'GET'])
def add_film():
    if 'user_id' in session:
        if USERS.get(session['user_id'])[3] == 'admin':
            form = AddFilmForm()
            if form.validate_on_submit():
                FILMS.insert(form.name.data, form.genre.data, form.director.data, form.image.data, form.date.data,
                             form.time.data, form.description.data)
            return render_template('add_film.html', title='Добавление фильма', form=form)
    return redirect('/')


@app.route('/films/<int:id>', methods=['GET', 'POST'])
def film_info(id):
    abort_if_films_not_found(id)
    user_fav = False
    film = FILMS.get(id)
    if 'user_id' in session:
        fav = USERS.get(session['user_id'])[4]
        if str(id) in fav:
            user_fav = True
        if request.method == 'POST':
            f = fav
            if not user_fav:
                f += str(id) + ','
                USERS.fav(session['user_id'], film_id=f)
                user_fav = True
            else:
                f = f.split(',')[:-1]
                f = ','.join(list(filter(lambda a: a != str(id), f))) + ','
                if f == ',':
                    f = ''
                USERS.fav(session['user_id'], film_id=f)
                user_fav = False
    return render_template('film_page.html', title=film[1], film=film, user_fav=user_fav)


@app.route('/search', methods=['POST'])
def search():
    return redirect('search/{}'.format(request.form['req']))


@app.route('/search/<string:s>')
def searcher(s):
    res = FILMS.get_all(order='genre', arg=s)
    res = optimize_cards(res)
    return render_template('search_res.html', title='Поиск', res=res)


if __name__ == '__main__':
    app.run(port=8080, host='localhost')
