from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from quiz import db, app
from quiz.models import User

from quiz.menu import menu


################################################################

@app.route('/', methods=['GET', 'POST'])
def index():

    if current_user.__dict__:
        authentication=True
    else:
        authentication=False

    return render_template('index.html',  menu=menu, authentication=authentication)

################################################################


@app.route('/login', methods=['GET', 'POST'])
def login_page():

    if session.get('authentication'):
        return redirect(url_for('index'))       

    if request.method == 'POST':
        
        login = request.form.get('login')
        password = request.form.get('psw')

        if login and password:
            user = User.query.filter_by(login=login).first()

            if not user:
                flash('неверный логин', category = 'error')

            elif user and check_password_hash(user.psw, password):
                login_user(user)
                session.permanent = True
                session['authentication'] = True

                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:

                    return redirect(url_for('index'))
                
            else:
                flash('Неверный пароль', category = 'error')

        else:
            flash('введите логин и пароль', category = 'error')


    return render_template('login.html', menu=menu)

################################################################


@app.route('/register', methods=['GET', 'POST'])
def register_page():

    if session.get('authentication'):
        return redirect(url_for('index'))
    
    name = request.form.get('name')
    login = request.form.get('login')
    psw = request.form.get('psw')
    psw2 = request.form.get('psw2')

    if request.method == 'POST':

        user = User.query.filter_by(login=login).first()
        if user:
            flash('пользовательй с таким логином уже существует', category = 'error')
            return redirect(url_for('register_page'))

        if not (login or psw or psw2):
            flash('заполните все поля', category = 'error')
            return redirect(url_for('register_page'))
        
        elif psw != psw2:
            flash('пароли не совпадают', category = 'error')
            return redirect(url_for('register_page'))

        else:
            hash_psw = generate_password_hash(psw)
            new_user = User(name= name, login= login, psw= hash_psw)

            db.session.add(new_user)
            db.session.commit()

            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login_page'))

    return render_template('register.html', menu=menu, title='Регистрация')

################################################################


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout_page():

    logout_user()
    session['authentication'] = False
    return redirect(url_for('login_page'))

################################################################


@app.after_request
def redirect_to_signi(response):
    if response.status_code == 401:
        session['authentication'] = False
        return redirect(url_for('login_page') + '?next' + request.url)

    return response


