"""
https://github.com/Rovindu-Thamuditha/authentication-system

MIT License

Copyright (c) 2024 [Rovindu Thamuditha]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import re 
import time
import random
import hashlib
import sqlite3

def create_table(cursor):
    """Create the users table if it doesn't exist."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            id TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

def load_data(conn):
    """Load user data from the SQLite database."""
    users_data = {}
    cursor = conn.cursor()
    create_table(cursor)

    cursor.execute('SELECT username, name, id, password FROM users')
    rows = cursor.fetchall()
    for row in rows:
        username, name, user_id, hashed_password = row
        users_data[username] = {'name': name, 'id': user_id, 'password': hashed_password}

    return users_data

def save_data(conn, user_data):
    """Save user data to the SQLite database."""
    cursor = conn.cursor()
    create_table(cursor)

    for username, data in user_data.items():
        name = data['name']
        user_id = data['id']
        hashed_password = data['password']
        cursor.execute('''
            INSERT OR REPLACE INTO users (username, name, id, password)
            VALUES (?, ?, ?, ?)
        ''', (username, name, user_id, hashed_password))

    conn.commit()

def validate_username(username):
    """Check if the username has no spaces and illegal characters."""
    if re.match("^[a-zA-Z0-9_]+$", username):
        return True
    return False

def generate_user_id():
    """Generate a simple user ID."""
    timestamp = int(time.time() * 1000)
    random_number = random.randint(1000, 9999)
    user_id = f"{timestamp}-{random_number}"
    return user_id

def hash_password(password):
    """Hash the password using a secure hashing algorithm."""
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password, conn):
    """Verify user login credentials."""
    users_data = load_data(conn)

    if username in users_data:
        hashed_password = users_data[username].get('password', '')
        if hashed_password == hash_password(password):
            return {'success': True, 'message': 'Login Successful', 'user_info': users_data[username]}
        else:
            return {'success': False, 'message': 'Wrong Password'}
    else:
        return {'success': False, 'message': 'User not found'}

def register(username, name, password, confirm_password, conn):
    """Register a new user and save data"""
    if not validate_username(username):
        return {'success': False, 'message': 'Invalid username. Use only letters, numbers, and underscores.'}

    if ' ' in username:
        return {'success': False, 'message': 'Username cannot contain spaces.'}

    if not re.match("^[A-Za-z0-9_-]*$", username):
        return {'success': False, 'message': 'Username contains illegal characters.'}

    if password != confirm_password:
        return {'success': False, 'message': 'Passwords do not match.'}

    users_data = load_data(conn)

    if username in users_data:
        return {'success': False, 'message': 'Username already exists. Please choose another name.'}
    else:
        user_id = generate_user_id()
        hashed_password = hash_password(password)
        users_data[username] = {'name': name, 'id': user_id, 'password': hashed_password}
        save_data(conn, users_data)
        return {'success': True, 'message': f'Name : {name} \nUsername : {username} \nID : {user_id}', 'user_id': user_id, 'user_info': users_data[username]}


"""
---------EXAMPLE USAGE---------

conn = sqlite3.connect('users.db')
registration_result = register('john_doe', 'John Doe', 'password123', 'password123', conn)
print(registration_result)
login_result = login('john_doe', 'password123', conn)
print(login_result)
conn.close()

"""