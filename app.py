from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db
from myqueue import Line

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
CORS(app)
Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

_line = Line()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/new', methods=['POST'])
def new_element():
   
    if not request.json.get('name') or request.json.get('name') == '':
        return jsonify({'msg':'You need to enter a valid user name'}),404
    if not request.json.get('phone') or len(request.json.get('phone')) < 8:
        return jsonify({'msg':'Insert a valid phone number'}), 404
    person={
        "name": request.json.get('name'),
        "phone": request.json.get('phone')
    }
    _line.enqueue(person)
    return jsonify({"msg":"A message has been sent to your phone number, we will let you know when it's your turn"}),200

@app.route('/next')
def next_element():
    line = _line.dequeue()
    return jsonify({"msg":"You are next"}),200

@app.route('/all')
def all_elements():
    
    line = _line.get_queue()
    return jsonify(line), 200

if __name__=='__main__':
    manager.run()

