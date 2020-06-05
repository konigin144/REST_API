from flask import render_template, flash, redirect, session, url_for, request, jsonify, make_response
from flask_wtf import form
from app import app
from app.forms import SubjectForm

from flask_table import Table

import yaml
from yaml import load, dump, Loader
import json

import wtforms_json
import random

path = 'app/db/test.yaml'
db = None
stream = None
url = 'http://192.168.1.12:5000/'

def Load():
    global db,stream
    stream = open(path, 'r')
    db=yaml.load(stream, Loader=yaml.FullLoader)
    stream.close()

def Save():
    global db,stream
    stream = open(path, 'w')
    stream.write(yaml.dump(db,default_flow_style=False,sort_keys=False))
    stream.close()

@app.route('/')
@app.route('/index')
def index():
    Load()
    return make_response(render_template('index.html', title='Table', db=db), 200)

@app.route('/events/json', methods=['GET'])
def get_events():
    Load()
    return make_response(db,200)

@app.route('/events/table', methods=['GET'])
def get_events_table():
    Load()
    return make_response(render_template('table.html', title='Table', db=db), 200)

@app.route('/event/<string:eventID>', methods=['GET'])
def get_event(eventID):
    Load()
    return make_response(jsonify({eventID : json.dumps(db['events'][eventID])}),200)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = SubjectForm()
    if form.validate_on_submit():
        date = form.date.data
        month = date.month
        day = date.day
        year = date.year
        date_str = date.strftime('%Y-%m-%d')

        time = form.time.data
        time_str = ''
        if(form.time.data is not None): 
            hour = time.hour
            minute = time.minute
            time_str = time.strftime('%H:%M')

        jform = {
                "subject": form.subject.data,
                "type": form.type.data,
                "date": date_str,
                "time": time_str,
                "other": form.other.data
        }

        global db
        Load()

        eventID = ''
        x = 0
        while(True):
            x = random.randint(1,100)
            eventID = str(x)
            if(eventID not in db):
                break

        tmp = dict(**{'events': {eventID: jform}})
        tmps = db

        for i in tmp['events']:
            tmps['events'].update({i:tmp['events'][i]})

        db = tmps
        Save()


        flash('Dodano {} - {}!'.format(
            form.subject.data, form.type.data))
        return redirect('/')
    return make_response(render_template('add.html', title='Add', form=form), 201)

@app.route('/add', methods=['PUT'])
def put_event():
    global db
    Load()

    eventID = ''
    x = 0
    while(True):
        x = random.randint(1,100)
        eventID = str(x)
        if(eventID not in db):
            break

    tmp = dict(**{'events': {eventID: request.json}})
    tmps = db

    for i in tmp['events']:
        tmps['events'].update({i:tmp['events'][i]})

    db = tmps
    Save()
    return make_response(jsonify({'url': url+'event/'+eventID}), 201)

@app.route('/event/<string:eventID>', methods=['DELETE'])
def delete_event(eventID):
    Load()
    del db ['events'][eventID]
    Save()
    return make_response(jsonify({'url': url}), 204)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)

@app.errorhandler(409)
def conflict(error):
    return make_response(jsonify({'error': 'Conflict'}), 409)