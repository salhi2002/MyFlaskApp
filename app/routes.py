from flask import render_template, request, redirect, session, url_for
from . import get_connection

def setup_routes(app):
    app.secret_key = 'secretkey'  # ضروري للجلسات

    @app.route('/')
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def do_login():
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")

    @app.route('/dashboard')
    def dashboard():
        if 'user' not in session:
            return redirect(url_for('login'))

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM data")
        rows = cur.fetchall()
        conn.close()
        return render_template('dashboard.html', rows=rows)

    @app.route('/add', methods=['POST'])
    def add_data():
        if 'user' not in session:
            return redirect(url_for('login'))

        content = request.form['content']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO data (content) VALUES (%s)", (content,))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    
    @app.route('/delete/<int:data_id>', methods=['POST'])
    def delete_data(data_id):
        if 'user' not in session:
            return redirect(url_for('login'))

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM data WHERE id = %s", (data_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

