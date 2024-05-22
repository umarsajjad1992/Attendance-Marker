from flask import Flask, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(id=user[0], username=user[1])
    return None


def connect_db():
    return sqlite3.connect('attendance.db')


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        conn = connect_db()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                      (username, generate_password_hash(password)))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'Username already exists'}), 400

        conn.close()
        return jsonify({'message': 'User registered successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            user_obj = User(id=user[0], username=user[1])
            login_user(user_obj)
            return jsonify({'message': 'Logged in successfully'}), 200
        return jsonify({'error': 'Invalid credentials'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/mark_attendance', methods=['POST'])
@login_required
def mark_attendance():
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('INSERT INTO attendance (user_id) VALUES (?)', (current_user.id,))
        conn.commit()
        conn.close()
        return jsonify({'message': f'Attendance marked for {current_user.username}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/attendance', methods=['GET'])
@login_required
def get_attendance():
    try:
        conn = connect_db()
        c = conn.cursor()
        c.execute('SELECT a.id, u.username, a.timestamp FROM attendance a JOIN users u ON a.user_id = u.id')
        rows = c.fetchall()
        conn.close()

        attendance_list = [{'id': row[0], 'username': row[1], 'timestamp': row[2]} for row in rows]
        return jsonify(attendance_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
