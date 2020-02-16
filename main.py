from flask import Flask, request, jsonify
from render_views import *
from config import *


app = Flask(__name__)


@app.route("/")
def view_main():
    r = render_main()
    return r


@app.route("/balance_iml")
def view_balance_iml():
    r = render_balance_iml()
    return r


if __name__ == '__main__':
    app.run(host=URL_APP)
