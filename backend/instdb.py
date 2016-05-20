#! /usr/bin/env python3

import base64
import hashlib
import json
import os

import psycopg2

from voluptuous import Schema, Required, All, Length
from flask import Flask, render_template, request

import instdb_settings as idbs

conn = psycopg2.connect(dbname=idbs.dbname, user=idbs.user, host=idbs.host, password=idbs.password)
bad_request = json.dumps({"success":False})

validators = {
    "new user":Schema({
        Required("username"): All(str, Length(min=1)),
        Required("password"): All(str, Length(min=1))
    })
}

# validators["new login"]({"username":"user","password":"pass"})

app = Flask(__name__)

@app.route("/")
def render_console():
    return render_template("console.html")

@app.route("/user/create", methods=["POST"])
def api_user_create():
    try:
        body = validators["new user"](json.loads(request.data.decode("utf-8")))
    except:
        return bad_request
    newsalt = base64.b64encode(os.urandom(45)).decode("utf-8")
    newhash = hashlib.sha256(newsalt.encode("utf-8") + body["password"].encode("utf-8")).hexdigest()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (body["username"],))
    matches = cur.fetchall()
    if matches != []:
        return bad_request
    cur.execute("INSERT INTO users (username, passhash, salt) VALUES (%s, %s, %s) RETURNING id", (body["username"], newhash, newsalt))
    newid = cur.fetchone()[0]
    conn.commit()
    return json.dumps({"success":True,"new_id":newid})

if __name__ == "__main__":
    app.run(debug=True)
