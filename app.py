from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Quote %r>' % self.id

@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        quote_content = request.form['content']
        new_quote = Todo(content=quote_content)

        try:
            db.session.add(new_quote)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your quote"

    elif request.method == 'GET':
        quotes = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', quotes = quotes)

@app.route('/delete/<int:id>')
def delete(id):
    quote_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(quote_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was a problem deleting the quote'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    quote = Todo.query.get_or_404(id)

    if request.method == 'POST':
        quote.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was a problem updating the quote'

    elif request.method == 'GET':
        return render_template('update.html', quote = quote)


if __name__ == "__main__":
    app.run(debug=True)