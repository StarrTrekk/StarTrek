from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import subprocess
import os
from flask_cors import CORS
from datetime import timedelta

PATH_KEY = ".secret.key"
HOST = os.getenv("HOST", "localhost")


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
