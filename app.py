import csv

import pymysql
from flask import Flask, render_template, request, jsonify
from env import HOST, DATABASE, USER, PASSWORD

app = Flask(__name__)


def create_connection():
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DATABASE,
                           cursorclass=pymysql.cursors.DictCursor)
    return conn


@app.route('/cynical-reader/from')
def from_source():
    '''
        URL: /cynical-reader/from?site=stackoverflow.com&page=1
    '''
    site = request.args.get('site', '')
    page = request.args.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1

    if page < 1:
        page = 1

    limit = 30
    offset = (page - 1) * limit

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM data WHERE source="{site}" ORDER BY published_date DESC LIMIT {offset}, {limit}')
    data = cursor.fetchall()  # list of dict
    return render_template('site.html', data=data, next_page=page + 1, site=site)


@app.route('/cynical-reader')
def cynical_reader():
    page = request.args.get('page', 1)
    try:
        page = int(page)
    except:
        page = 1

    if page < 1:
        page = 1

    limit = 30
    offset = (page - 1) * limit

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM data ORDER BY published_date DESC LIMIT {offset}, {limit}')
    data = cursor.fetchall()
    return render_template('index.html', data=data, next_page=page + 1)


@app.route('/')
def home():
    return '<h1 align="center" style="margin-top:200px;">Lets Get Cynical!</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0')

