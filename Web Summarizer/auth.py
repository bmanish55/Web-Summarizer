from flask import request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

# MySQL connection setup
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Manish@845905',  # Replace with your MySQL password
    'database': 'websummerizer'
}

def register():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Validation checks
    if not email or not password or not confirm_password:
        return "<script>alert('All fields are required'); window.location.href='/'</script>"
    if password != confirm_password:
        return "<script>alert('Passwords do not match'); window.location.href='/'</script>"

    cursor = None  # Initialize cursor to None to prevent UnboundLocalError
    conn = None  # Initialize connection to None to prevent UnboundLocalError
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if email is already registered
        query_check = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query_check, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "<script>alert('Email is already registered'); window.location.href='/'</script>"

        # Insert the new user
        hashed_password = generate_password_hash(password)
        query_insert = "INSERT INTO users (email, password) VALUES (%s, %s)"
        cursor.execute(query_insert, (email, hashed_password))
        conn.commit()

        return "<script>alert('Registration successful!'); window.location.href='/'</script>"

    except mysql.connector.Error as err:
        return f"Database error: {err}"

    finally:
        if cursor:  # Only close cursor if it was created
            cursor.close()
        if conn:  # Only close connection if it was created
            conn.close()

def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return "<script>alert('All fields are required'); window.location.href='/'</script>"

    cursor = None  # Initialize cursor to None to prevent UnboundLocalError
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user exists
        query_check = "SELECT id, password FROM users WHERE email = %s"
        cursor.execute(query_check, (email,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user[1], password):
            return "<script>alert('Invalid email or password'); window.location.href='/'</script>"

        # Set session
        session['user_id'] = user[0]
        session['email'] = email

        return redirect(url_for('dashboard'))

    except mysql.connector.Error as err:
        return f"Database error: {err}"

    finally:
        if cursor:
            cursor.close()  # Only close cursor if it's initialized
        if conn:
            conn.close()  # Close the connection if it's established
