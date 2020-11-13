import csv

import pymysql
from flask import Flask, render_template, request, jsonify
from env import HOST, DATABASE, USER, PASSWORD
from dictionary import domains, sites
from datetime import datetime, timedelta

app = Flask(__name__)


def create_connection():
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DATABASE,
                           cursorclass=pymysql.cursors.DictCursor)
    return conn

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
    return render_template(
        'index.html', 
        data=data, 
        next_page=page + 1,
        domains=domains,
        sites=sites,
        active_site='all',
        active_domain='all'
    )



@app.route('/cynical-reader/filter')
def filter_domain():
    '''
        URL: /cynical-reader/filter?domain={{ domain }}&site={{ site }}&page=1
    '''
    domain = request.args.get('domain', 'all')
    site = request.args.get('site', 'all')
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
    if site == 'all' and domain == 'all':
        cursor.execute(f'SELECT * FROM data ORDER BY published_date DESC LIMIT {offset}, {limit}')
    elif site == 'all' and not domain == 'all':
        cursor.execute(f'SELECT * FROM data WHERE domains like "%{domain}%" ORDER BY published_date DESC LIMIT {offset}, {limit}')
    elif not site == 'all' and domain == 'all':
        cursor.execute(f'SELECT * FROM data WHERE source="{site}" ORDER BY published_date DESC LIMIT {offset}, {limit}')
    else:
        cursor.execute(f'SELECT * FROM data WHERE source="{site}" and domains like "%{domain}%" ORDER BY published_date DESC LIMIT {offset}, {limit}')
    
    data = cursor.fetchall()  # list of dict

    graph_data = []

    day_cnt = 7
    alias = 'all'
    while day_cnt >0:      # loop this for full week
        today = datetime.now() - timedelta(day_cnt)
        today = today.strftime("%Y-%m-%d")
        percentages = {'date':today} # list of dict: {site:<>, per: <>} #TODO: change this
        if not domain == 'all':
            if not site == 'all':
                #get corresponding site_alias from site_link
                for k,v in sites.items():
                    if v == site:
                        alias = k
                # graph calc for this site
                cursor.execute(f'SELECT count(*) as count FROM data WHERE source="{site}" and domains like "%{domain}%" and published_date like "%{today}%"')
                items = cursor.fetchone()['count']
                cursor.execute(f'SELECT count(*) as count FROM data WHERE source="{site}" and published_date like "%{today}%"')
                total_items = cursor.fetchone()['count']
                if not total_items == 0:
                    percentages[alias] =  round(float(items/(total_items*(len(sites)-1)))*100, 2)
            else:
                # graph calc for all sites
                for site_alias, site_link in sites.items():
                    cursor.execute(f'SELECT count(*) as count FROM data WHERE source="{site_link}" and domains like "%{domain}%" and published_date like "%{today}%"')
                    items = cursor.fetchone()['count']
                    cursor.execute(f'SELECT count(*) as count FROM data WHERE source="{site_link}" and published_date like "%{today}%"')
                    total_items = cursor.fetchone()['count']
                    if not total_items == 0:
                        percentages[site_alias] =  round(float(items/(total_items*(len(sites)-1)))*100, 2)
            graph_data.append(percentages)
        day_cnt -= 1

    print(">>>> graph_data: {}".format(graph_data))

    if not site == 'all':
        site_aliases = [alias,'all']
    else:
        site_aliases = [k for k,v in sites.items()]
    print(">>>> site_aliases: {}".format(site_aliases))

    return render_template(
        'filter.html', 
        data=data, 
        next_page=page + 1,
        domains=domains,
        sites=sites,
        active_domain=domain,
        active_site=site,
        site_aliases=site_aliases,
        graph_data=graph_data
    )

# @app.route('/cynical-reader/from')
# def from_source():
#     '''
#         URL: /cynical-reader/from?site=stackoverflow.com&page=1
#     '''
#     site = request.args.get('site', '')
#     page = request.args.get('page', 1)
#     try:
#         page = int(page)
#     except:
#         page = 1

#     if page < 1:
#         page = 1

#     limit = 30
#     offset = (page - 1) * limit

#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute(f'SELECT * FROM data WHERE source="{site}" ORDER BY published_date DESC LIMIT {offset}, {limit}')
#     data = cursor.fetchall()  # list of dict
#     return render_template(
#         'site.html', 
#         data=data, 
#         next_page=page + 1, 
#         site=site,
#         sites=sites,
#         domains=domains
#     )


@app.route('/')
def home():
    return '<div align="center"><h1 align="center" style="margin-top:200px;">Lets Get Cynical!</h1> <br><br> <a href="/cynical-reader" style="text-decoration: none;color: #959494;"> Enter</a> </div>'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
