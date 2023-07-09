from typing import Dict
import json

from flask import Flask, render_template, request

from app.database_query import DatabaseQuery

app = Flask(__name__)
database_query = DatabaseQuery()


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/ask-query', methods=['POST'])
def ask_query():
    data: Dict = request.json

    prompt: str = data.get("prompt")

    query = database_query.query(prompt)

    return json.dumps(query)
