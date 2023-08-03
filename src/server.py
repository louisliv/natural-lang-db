from typing import Dict
import json
import os

from flask import Flask, render_template, request, jsonify, session

from app.database_query import DatabaseQuery
from app.auth.token_authentication import TokenAuthentication
from app.auth.helpers import login_required

SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)
app.secret_key = SECRET_KEY
database_query = DatabaseQuery()

app.debug = True


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        is_authorised = TokenAuthentication(request).is_authorised()

        if not is_authorised:
            return jsonify(error=400, text=str("Invalid Token")), 400

        token = request.get_json().get("token")

        session["token"] = token

        response = jsonify()

        return response

    return render_template("login.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    session.clear()

    return jsonify()


@app.route("/ask-query", methods=["POST"])
@login_required
def ask_query():
    data: Dict = request.json

    prompt: str = data.get("prompt")

    query = database_query.query(prompt)

    return jsonify({"query_result": query})
