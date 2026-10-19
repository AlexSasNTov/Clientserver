"""
Routes and views for the flask application.
"""

import sqlite3
from datetime import datetime
from flask import render_template, request
from FlaskWebProjectDmitry import app

DB_NAME = 'calculations.db'

def init_db():
    """Создает базу данных и таблицу, если они еще не созданы."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num1 TEXT,
                num2 TEXT,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Создаем базу данных при загрузке

init_db()


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    """Renders the home page with calculator logic and DB history."""
    result = None
    num1 = ""
    num2 = ""

    # Если пользователь отправил форму
    if request.method == 'POST':
        num1 = request.form.get('num1', '')
        num2 = request.form.get('num2', '')

        try:
            calculated_result = float(num1) + float(num2)
            if calculated_result.is_integer():
                calculated_result = int(calculated_result)
            result = str(calculated_result)
            
            # Сохранение в БД
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO history (num1, num2, result) VALUES (?, ?, ?)',
                    (num1, num2, result)
                )
                conn.commit()
                
        except ValueError:
            result = "Ошибка: введите корректные числа!"

    # Получение истории
    history = []
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT num1, num2, result FROM history ORDER BY id DESC LIMIT 10')
            history = cursor.fetchall()
    except sqlite3.Error:
        pass

    return render_template(
        'calc.html',
        title='Калькулятор',
        year=datetime.now().year,
        result=result,
        num1=num1,
        num2=num2,
        history=history  # Историю в шаблон
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.jade',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.jade',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )