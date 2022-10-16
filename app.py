from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from random import choice
from uuid import uuid4
from var import *
import sqlite3



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY']='LongAndRandomSecretKey'
app.secret_key='LongAndRandomSecretKey'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


#form when user gets the default bridge page
class BridgeForm(FlaskForm):
    username = StringField(label=('What is your name?'),
        validators=[DataRequired(), 
        Length(min=3, max=64, message='Name length must be between %(min)d and %(max)dcharacters') ])
    quest = StringField(label=('What is your Quest?'), 
        validators=[DataRequired(), Length(max=120)])
    favourite_color = StringField(label=('What is your favourite color?'), 
        validators=[Length(max=30)])
    submit = SubmitField(label=('Submit'))

#form when user gets the arthur bridge page
class ArthurForm(FlaskForm):
    username = StringField(label=('What is your name?'),
        validators=[DataRequired(), 
        Length(min=3, max=64, message='Name length must be between %(min)d and %(max)dcharacters') ])
    quest = StringField(label=('What is your Quest?'), 
        validators=[DataRequired(), Length(max=120)])
    swallow = StringField(label=('What is the air speed velocity of an unladen swallow?'), 
        validators=[Length(max=30)])
    submit = SubmitField(label=('Submit'))

#class for database
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=True)
    quest = db.Column(db.String(120), nullable=True)
    content = db.Column(db.String(1000), nullable=True)
    color = db.Column(db.String(30))
    date_created = db.Column(db.DateTime, default=datetime.now)
    sessionid = db.Column(db.String(400), nullable=True)
    ip = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return '<quote %r>' % self.id
#first page upon going to the website       
@app.route('/', methods=['POST', 'GET'])    
def landing():
    #bridge_choices = ['/bridge','/bridgerobin']
    #bridge_choice = choice(bridge_choices)
        return render_template('landing.html')

@app.route('/gorge', methods=['POST', 'GET'])    
def gorgeofeternalperil():
        return render_template('gorgeofeternalperil.html')

#when user asnwers the bridgekeeper
@app.route('/bridge', methods=['POST', 'GET'])
def bridge():
    form = BridgeForm()
    if request.method == 'POST': 
        if form.validate_on_submit():
            session["id"] = str(uuid4())
            session["name"] = form.username.data
            session["quest"] = form.quest.data
            session["color"] = form.favourite_color.data.lower()
            
            
            if "no" in session["color"]:
                session["color"] = ""
                return redirect('/gorge')
            return redirect('/bridge/index')
    elif request.method == 'GET':
        return render_template('bridge.html', form=form)

@app.route('/bridgearthur', methods=['POST', 'GET'])
def bridgearthur():
    form = ArthurForm()
    if request.method == 'POST': 
        if form.validate_on_submit():
            session["id"] = str(uuid4())
            session["name"] = form.username.data
            session["quest"] = form.quest.data
            session["color"] = ""
            
            if "african or european" in form.swallow.data.lower():
                session["color"] = ""
                return redirect('/bridge/index')
            return redirect('/gorge')
    elif request.method == 'GET':
        return render_template('bridgearthur.html', form=form)

@app.route('/bridgerobin', methods=['POST', 'GET'])    
def bridgerobin():
    form = ArthurForm()
    return render_template('bridgerobin.html', form=form)

@app.route('/bridge/index', methods=['POST', 'GET'])
def index():
#when user submits quote
    form = BridgeForm()
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr) 
    if "id" in session:
        if request.method == 'POST':
            new_quote = Entry(content=request.form['content'], username=session["name"], quest=session["quest"], color=session["color"], sessionid=session["id"], ip=ip_addr)

            try:
                db.session.add(new_quote)
                db.session.commit()
                return redirect('/bridge/index')
            except:
                return "There was an error adding your quote"
    
    #when no submission
        elif request.method == 'GET':
            quotes = Entry.query.order_by(Entry.date_created.desc()).all()
            return render_template('index.html', quotes = quotes)

    else:
        return redirect('/halt')

#delete quote
@app.route('/bridge/index/delete/<int:id>')
def delete(id):
    # executing SQL syntax
    # connecting to the database
    connection = sqlite3.connect("test.db")
    # cursor
    crsr = connection.cursor() 
    # SQL command to get the session id of the quote
    sql_command = f"SELECT sessionid FROM entry WHERE id = {id};"
    # execute the statement
    crsr.execute(sql_command)
    # store all the fetched data in the ans variable
    ans = str(crsr.fetchall()[0])
    ans = ans.strip("('")
    ans = ans.rstrip("',)")
    # close the connection
    connection.close()
    #End of SQL

    #backdoor for admin rights to delete any post
    admin = False
    if session["name"] == "Zoot" and session["quest"] == "get a spanking" and session["color"] == "grey":
        admin = True

    #only can delete from the same session
    if session["id"] != ans:
        if admin == False:
            return redirect('/whodidit')

    quote_to_delete = Entry.query.get_or_404(id)

    try:
        db.session.delete(quote_to_delete)
        db.session.commit()
        return redirect('/bridge/index')
    except:
        return 'there was a problem deleting the quote'

#update quote
@app.route('/bridge/index/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    # executing SQL syntax
    # connecting to the database
    connection = sqlite3.connect("test.db")
    # cursor
    crsr = connection.cursor() 
    # SQL command to get the session id of the quote
    sql_command = f"SELECT sessionid FROM entry WHERE id = {id};"
    # execute the statement
    crsr.execute(sql_command)
    # store all the fetched data in the ans variable
    ans = str(crsr.fetchall()[0])
    ans = ans.strip("('")
    ans = ans.rstrip("',)")
    # close the connection
    connection.close()
    #End of SQL

    if session["id"] != ans:
        return redirect('/whodidit')

    quote = Entry.query.get_or_404(id)

    if request.method == 'POST':
        quote.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/bridge/index')
        except:
            return 'there was a problem updating the quote'

    elif request.method == 'GET':
        return render_template('update.html', quote = quote)

@app.route('/halt', methods=['POST', 'GET'])    
def halt():
        return render_template('halt.html')

@app.route('/whodidit', methods=['POST', 'GET'])    
def whodidit():
        return render_template('whodidit.html')


if __name__ == "__main__":
    app.run(debug=True)