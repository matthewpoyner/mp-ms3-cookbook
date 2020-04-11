import os
from os import path

if path.exists("env.py"):
    import env

from flask import Flask, render_template, redirect, request, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), 
    port=os.environ.get("PORT"), debug=True)