from flask import render_template, redirect, url_for, request, flash, g, session
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta

from quiz import db, app, login_manager
from quiz.models import User, Word
from quiz.menu import menu

from scripts.parsing import Parsing, replace, change_column, next_column

import time



@app.route('/my_words', methods=['GET', 'POST'])
@login_required
def my_words():

    column_counter = 2
    column_width = 'width_lng'

    if request.method == 'POST':

        if request.form.get('save'):

            word_id = int(request.form.get('save')[2:])
            column_1 = request.form.get('column_1_' + str(word_id))
            column_2 = request.form.get('column_2_' + str(word_id))
            column_3 = request.form.get('column_3_' + str(word_id))
            column_4 = request.form.get('column_4_' + str(word_id))

            Word.query.filter((Word.user_id == session['_user_id']) & (Word.word_id == word_id)).update({Word.first_lng: column_1, 
                                                                                                         Word.second_lng: column_2, 
                                                                                                         Word.third_lng: replace(column_3), 
                                                                                                         Word.fourth_lng: replace(column_4), })
            db.session.commit()

        if request.form.get('delete'):
            word_id = int(request.form.get('delete')[2:])
            Word.query.filter((Word.user_id == session['_user_id']) & (Word.word_id == word_id)).delete()
            db.session.commit()

        if request.form.get('column_counter') in ['2', '3', '4']:
            column_counter = int(request.form.get('column_counter'))

        elif session.get('column_counter'):
            column_counter = int(session.get('column_counter'))

        else:
            column_counter = 2
        column_width = {2: 'width_lng', 3: 'width_lng_3', 4: 'width_lng_4'}[column_counter]
        session['column_counter'] = column_counter


    session['dict_word'] = dict()
    session['id_lesson'] = dict()
    session['id_word'] = dict()
    words = Word.query.filter_by(user_id= session['_user_id']).order_by(Word.lesson.desc()).all()
    return render_template('my_words.html', menu=menu, title='Мои слова', column_counter=column_counter, column_width=column_width, words=words, authentication=True)

################################################################


@app.route('/add_words', methods=['GET', 'POST'])
@login_required
def add_words():

    column_counter = 2
    column_width = 'width_lng'

    last_word = Word.query.filter((Word.user_id == session['_user_id']) & (Word.lesson > 1) ).order_by(Word.lesson.desc()).first()

    if last_word:         
        if (datetime.utcnow() - last_word.date) > timedelta(hours=2):
            lesson = int(last_word.lesson) + 1
        else:
            lesson = int(last_word.lesson)
    else:
        lesson = 1


    session['_user_id'] = current_user.__dict__['id']
    if request.method == 'POST':

        if request.form.get('clean'):
            session['dict_word'] = dict()
            lesson= request.form.get('lesson')
            
        else:
            if request.form.get('delete'):
                line = request.form['delete'].replace(' удалить', '')            
                try:
                    session['dict_word'].pop(str(line))
                except:
                    print('key error', line)           

            dict_word = Parsing()
            dict_word.convert(name='column_1', text=request.form.get('column_1'))
            dict_word.convert(name='column_2', text=request.form.get('column_2'))
            dict_word.convert(name='column_3', text=request.form.get('column_3'))
            dict_word.convert(name='column_4', text=request.form.get('column_4'))
            table = dict_word.get_dict()
            lesson = request.form.get('lesson')
            if table:
                session['dict_word'] = table

            else:                
                keys = session['dict_word'].keys()
                for key in keys:
                   session['dict_word'][key]['column_1'] = request.form.get('column_1_' + str(key))
                   session['dict_word'][key]['column_2'] = request.form.get('column_2_' + str(key))
                   session['dict_word'][key]['column_3'] = request.form.get('column_3_' + str(key))
                   session['dict_word'][key]['column_4'] = request.form.get('column_4_' + str(key))

        if request.form.get('append'):
            for value in session['dict_word'].values():
                words = Word(user_id= current_user.__dict__['id'],
                             first_lng= value['column_1'],
                             second_lng= value['column_2'],
                             third_lng= replace(value['column_3']),
                             fourth_lng= replace(value['column_4']),
                             lesson= request.form.get('lesson'))

                db.session.add(words)
            db.session.commit()
            session['dict_word'] = dict()
            flash("Слова дабавлены в БД", "success")

#        else:
#            flash('Ошибка сохранения', category = 'error')

        if request.form.get('column_counter') in ['2', '3', '4']:
            column_counter = int(request.form.get('column_counter'))

        elif session.get('column_counter'):
            column_counter = int(session.get('column_counter'))

        else:
            column_counter = 2
        column_width = {2: 'width_lng', 3: 'width_lng_3', 4: 'width_lng_4'}[column_counter]
        session['column_counter'] = column_counter

    return render_template('add_words.html', menu=menu, table=session['dict_word'], title='Добавление слов', column_counter=column_counter, column_width=column_width, lesson=lesson, authentication=True)

################################################################


@app.route('/show_quiz', methods=['GET', 'POST'])
@login_required
def show_quiz():

    words = Word.query.filter_by(user_id= session['_user_id']).order_by(Word.lesson.desc()).all()
    dict_words = Parsing().lesson_dict(words)

    if request.form.get('id_lesson'):
        session['id_lesson'] = int(request.form['id_lesson'])
        session['id_word'] = min(dict_words[session['id_lesson']].keys())
        session['quiz_column'] = next_column(dict_words=dict_words, id_lesson=session['id_lesson'], id_word=session['id_word'])

    elif not session.get('id_lesson'):
        session['id_lesson'] = max(dict_words.keys())


    if not session.get('id_word'):
        session['id_word'] = min(dict_words[session['id_lesson']].keys())


    if request.form.get('quiz_column'):
        session['quiz_column'] = change_column(last_column=session['quiz_column'], dict_words=dict_words, id_lesson=session['id_lesson'], id_word=session['id_word'])
        time.sleep(0.5)

    elif not session.get('quiz_column'):
        session['quiz_column'] = 'column_1'
        

    if request.form.get('>'):

        if session['id_word'] == max(dict_words[session['id_lesson']].keys()):
            session['id_word'] = min(dict_words[session['id_lesson']].keys())
        
        else:
            for id_word in dict_words[session['id_lesson']].keys():
                if id_word > session['id_word']:
                    session['id_word'] = id_word
                    break
        
        session['quiz_column'] = next_column(dict_words=dict_words, id_lesson=session['id_lesson'], id_word=session['id_word'])

            
    if request.form.get('<'):

        if session['id_word'] == min(dict_words[session['id_lesson']].keys()):
            session['id_word'] = max(dict_words[session['id_lesson']].keys())
        
        else:
            for id_word in dict_words[session['id_lesson']].keys():
                if id_word == session['id_word'] - 1:
                    session['id_word'] = id_word
                    break

        session['quiz_column'] = next_column(dict_words=dict_words, id_lesson=session['id_lesson'], id_word=session['id_word'])


    return render_template('show_quiz.html', id_lesson=session['id_lesson'], id_word=session['id_word'], quiz_column=session['quiz_column'], menu=menu, dict_words=dict_words, title='Quiz', authentication=True)


 
